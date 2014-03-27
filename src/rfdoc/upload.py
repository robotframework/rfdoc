#!/usr/bin/env python

#  Copyright 2008-2013 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import with_statement

import os
import sys

from contextlib import closing
from HTMLParser import HTMLParser
from httplib import HTTPConnection
from optparse import OptionParser
from re import match
from StringIO import StringIO
from urlparse import urlsplit

from robot.errors import DataError
from robot.libdocpkg import LibraryDocumentation
from robot.parsing.populators import READERS


class Uploader(object):

    def __init__(self):
        self._options = CommandlineUI()
        self._uploader = XmlUploader(self._options.target_url)

    def run(self):
        failed = []
        for library in self._options.libraries:
            try:
                xml_doc = StringIO()
                # LibraryDocumentation().save() calls close() for the underlying
                # file but closing StringIO object discards its data.
                # This is why close() is overridden below.
                xml_doc.original_close = xml_doc.close
                try:
                    try:
                        if library.endswith('.xml'):
                            with open(library) as xml_file:
                                xml_doc.write(xml_file.read())
                        else:
                            xml_doc.close = lambda: None
                            LibraryDocumentation(library).save(xml_doc, 'xml')
                    except DataError, e:
                        message = "Library not found" if 'ImportError' in e.message else e.message
                        failed.append(library)
                        sys.stderr.write("Skipping '%s' due to an error: %s.\n" %
                            (library, message))
                        continue
                    xml_doc.name = library
                    self._uploader.upload_file(xml_doc, self._options.lib_name, self._options.lib_version)
                    sys.stdout.write("Updated documentation for '%s'.\n" % library)
                finally:
                    xml_doc.original_close()
            except DataError, e:
                failed.append(library)
                sys.stderr.write('%s: Remote error: %s\n' % (os.path.basename(__file__),
                                                      e.message))
        if failed:
            sys.stderr.write('\nERROR: Uploading %d file(s) failed:\n' % len(failed))
            for name in failed:
                sys.stderr.write('* %s\n' % name)
            exit(1)

class ImprovedOptionParser(OptionParser):

    # This prevents newlines from getting discarded from the help text.
    def format_description(self, formatter):
        return self.description

    # This adds "try --help for information" message.
    def error(self, message):
        progname = os.path.basename(sys.argv[0])
        sys.stderr.write('%s: error: %s\n'% (progname, message))
        sys.stderr.write("Try '%s --help' for more information.\n" % progname)
        exit(2)


class CommandlineUI(object):

    valid_lib_exts = tuple(READERS.keys() + ['py', 'java', 'xml'])
    default_url = 'localhost:8000'
    usage_text = 'usage: %prog [options] PATH ...'
    help_text = """
This script updates the documentation at Robot Framework RFDoc server.

PATH is one of the following (multiple can be given, separated by a space):
1) A path to a library source file (e.g. src/libraries/example_lib.py)
2) A path to a resource file (e.g. atest/resources/utils.txt)
3) A path to a library XML, generated using LibDoc (e.g. libdoc/BuiltIn.xml)
4) A path to a directory, in which case it's recursively traversed for any of
   files mentioned in 1-3.
"""[1:]
    epilog_text = """
The script is intended to be used as part of the CI pipeline or as an SCM
post-change hook to update the documentation in RFDoc automatically.
"""[1:]

    def __init__(self):
        self._parser = ImprovedOptionParser(
            usage=self.usage_text,
            description=self.help_text,
            epilog=self.epilog_text
        )
        self._add_commandline_options()
        self._options = self._get_validated_options()

    @property
    def target_url(self):
        return self._options.target_url

    @property
    def libraries(self):
        return self._options.libraries

    @property
    def lib_version(self):
        return self._options.lib_version

    @property
    def lib_name(self):
        return self._options.lib_name

    def _add_commandline_options(self):
        self._parser.add_option(
            '-u', '--url',
            dest='target_url',
            default=self.default_url,
            help="""Target RFDoc URL to update, e.g. '192.168.1.100:8000' or
'my.server.com/rfdoc'. If this option is not given, '%s' is assumed
as target.""" % self.default_url
         )
        self._parser.add_option(
            '-v', '--version',
            dest='lib_version',
            default=None,
            help="""Override library version""")
        self._parser.add_option(
            '-n', '--name',
            dest='lib_name',
            default=None,
            help="""Override library name""")

    def _get_validated_options(self):
        options, targets = self._parser.parse_args()
        if len(targets) < 1:
            self._exit_with_help()
        options.libraries = self._traverse_targets_for_libraries(targets)
        options.target_url = self._host_from_url(options.target_url)
        return options

    def _traverse_targets_for_libraries(self, targets):
        libraries = targets
        for directory in self._only_directories(targets):
            libraries.remove(directory)
            for path, _, filenames in os.walk(directory):
                for filename in self._only_library_files(filenames):
                    libraries.append(os.path.join(path, filename))
        return libraries

    def _only_directories(self, targets):
        for target in targets:
            if os.path.isdir(target):
                yield target

    def _only_library_files(self, filenames):
        for filename in filenames:
            if self._is_library_file(filename):
                yield filename

    def _is_library_file(self, filename):
        return any(filename.endswith(ext) for ext in self.valid_lib_exts)

    def _host_from_url(self, url):
        if not match(r'http(s?)\:', url):
            url = 'http://' + url
        return url

    def _exit_with_help(self):
        self._parser.print_help()
        exit(1)


class XmlUploader(object):
    default_endpoint = 'upload'
    required_content_template = """--%(boundary)s
Content-Disposition: form-data; name="override"

on
--%(boundary)s
Content-Disposition: form-data; name="file"; filename="%(filename)s"
Content-Type: text/xml

%(content)s
"""
    optional_field_template = """--%(boundary)s
Content-Disposition: form-data; name="%(name)s"

%(content)s
"""
    end_boundary_template = '--%(boundary)s--\n'

    def __init__(self, target_url):
        self.url = urlsplit(target_url)

    def upload_file(self, xml_doc, override_name=None, override_version=None):
        with closing(HTTPConnection(self.url.netloc)) as connection:
            try:
                response = self._post_multipart(connection, xml_doc, override_name, override_version)
            except Exception, message:
                if 'Connection refused' in message:
                    message = "connection refused to '%s', " % self.url.netloc
                    message += 'check that the host responds and is reachable.'
                raise DataError(message)
        self._validate_success(response)

    def _post_multipart(self, connection, xml_doc, override_name, override_version):
        connection.connect()
        content_type, body = self._encode_multipart_formdata(xml_doc, override_name, override_version)
        headers = {'User-Agent': 'RFDoc uploader', 'Content-Type': content_type}
        connection.request('POST', self._get_endpoint(), body, headers)
        return connection.getresponse()

    def _get_endpoint(self):
        return self.url.path + '/' + self.default_endpoint

    def _encode_multipart_formdata(self, xml_doc, override_name, override_version):
        boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
        body = self.required_content_template % {
            'boundary': boundary,
            'filename': xml_doc.name,
            'content': xml_doc.getvalue()
        }
        if override_name:
            body += self.optional_field_template % {
                'boundary': boundary,
                'name': 'override_name',
                'content': override_name
            }
        if override_version:
            body += self.optional_field_template % {
                'boundary': boundary,
                'name': 'override_version',
                'content': override_version
            }

        body += self.end_boundary_template % {'boundary': boundary}
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body.replace('\n', '\r\n')

    def _validate_success(self, response):
        if response.status != 200:
            raise DataError(response.reason.strip())
        html = response.read()
        if 'Successfully uploaded library' not in html:
            raise DataError('\n'.join(self._ErrorParser(html).errors))

    class _ErrorParser(HTMLParser):

        def __init__(self, html):
            HTMLParser.__init__(self)
            self._inside_errors = False
            self.errors = []
            self.feed(html)
            self.close()

        def handle_starttag(self, tag, attributes):
            if ('class', 'errorlist') in attributes:
                self._inside_errors = True

        def handle_endtag(self, tag):
            if tag == 'ul':
                self._inside_errors = False

        def handle_data(self, data):
            if self._inside_errors and data.strip():
                self.errors.append(data)


if __name__ == '__main__':
    Uploader().run()
