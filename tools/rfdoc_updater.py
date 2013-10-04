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
from urlparse import urlparse

from robot.errors import DataError
from robot.libdocpkg import LibraryDocumentation


class RFDocUpdater(object):

    def __init__(self):
        self._options = CommandlineUI()
        self._uploader = XmlUploader(self._options.target_host)

    def run(self):
        try:
            for lib_file in self._options.libraries:
                xml_doc = StringIO()
                # LibraryDocumentation().save() calls close() for the underlying
                # file, which in case of StringIO object means that its data is
                # discarded. This is why close() is overridden.
                xml_doc.original_close = xml_doc.close
                xml_doc.close = lambda: None
                try:
                    lib_doc = LibraryDocumentation(lib_file)
                    lib_doc.save(xml_doc, 'xml')
                    xml_doc.name = lib_doc.name + '.xml'
                    self._uploader.upload_file(xml_doc)
                finally:
                    xml_doc.original_close()
                sys.stdout.write("Updated documentation for '%s'.\n"
                                 % lib_doc.name)
        except DataError, message:
            sys.stderr.write('%s: error: %s\n' % (os.path.basename(__file__),
                                                  message))
            exit(1)


class CommandlineUI(object):
    default_url = 'localhost:8000'
    help_text = """usage: %prog [options] PATH ...'

This script regenerates documentation at Robot Framework RFDoc server.

PATH is either path to a library file or path to a directory containing several
libraries. Directory is traversed and traversing recurses into subdirectories.
Multiple PATHS can be given.

The script can be used as part of the CI pipeline or as a SCM post-change hook
to update the documentation automatically."""

    def __init__(self):
        self._parser = OptionParser(self.help_text)
        self._add_commandline_options()
        self._options = self._get_validated_options()

    @property
    def target_host(self):
        return self._options.target_host

    @property
    def libraries(self):
        return self._options.libraries

    def _add_commandline_options(self):
         self._parser.add_option(
             '-u', '--url',
             dest='target_host',
             default=self.default_url,
             help="""Target RFDoc host to update, e.g. 'my.server.com' or
'192.168.1.100:8000'. If this option is not given, '%s' is assumed
as target.""" % self.default_url
         )

    def _get_validated_options(self):
        if len(sys.argv) < 2:
            self._exit_with_help()
        options, paths = self._parser.parse_args()
        options.libraries = self._traverse_path_for_libraries(paths)
        options.target_host = self._host_from_url(options.target_host)
        return options

    def _traverse_path_for_libraries(self, paths):
        for path in paths:
            if not os.path.exists(path):
                self._parser.error('file or directory %s not exists' % path)
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    paths += self._add_library_files(root, files)
                paths.remove(path)
        return paths

    def _add_library_files(self, root, files):
        return [os.path.join(root, filename) for filename in files
                if self._is_library_file(filename)]

    def _is_library_file(self, filename):
        return filename.endswith('.py') or filename.endswith('.java')

    def _host_from_url(self, url):
        if not match(r'http(s?)\:', url):
            valid_url = 'http://' + url
        return urlparse(valid_url).netloc

    def _exit_with_help(self):
        self._parser.print_help()
        exit(1)


class XmlUploader(object):
    default_endpoint = '/upload'
    body_template = """--%(boundary)s
Content-Disposition: form-data; name="override"

on
--%(boundary)s
Content-Disposition: form-data; name="file"; filename="%(filename)s"
Content-Type: text/xml

%(content)s
--%(boundary)s--
"""

    def __init__(self, target_host):
        self.target_host = target_host

    def upload_file(self, xml_doc):
        with closing(HTTPConnection(self.target_host)) as connection:
            try:
                response = self._post_multipart(connection, xml_doc)
            except Exception, message:
                if 'Connection refused' in message:
                    message = "Connection refused to '%s'. " % self.target_host
                    message += 'Check that the host responds and is reachable.'
                raise DataError(message)
        self._validate_success(response)

    def _post_multipart(self, connection, xml_doc):
        connection.connect()
        content_type, body = self._encode_multipart_formdata(xml_doc)
        headers = {'User-Agent': 'RFDoc updater', 'Content-Type': content_type}
        connection.request('POST', self.default_endpoint, body, headers)
        return connection.getresponse()

    def _encode_multipart_formdata(self, xml_doc):
        boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
        body = self.body_template % {
            'boundary': boundary,
            'filename': xml_doc.name,
            'content': xml_doc.getvalue()
        }
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
    RFDocUpdater().run()
