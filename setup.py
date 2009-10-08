#!/usr/bin/env python

from distutils.core import setup


VERSION = 'devel'
DESCRIPTION = 'A web based system for storing and searching Robot Framework ' \
              'test library and resource file documentations'


def main():
    setup(
        name         = 'rfdoc',
        version      = VERSION,
        description  = DESCRIPTION,
        author       = 'Robot Framework Developers',
        author_email = 'robotframework-devel@googlegroups.com',
        url          = 'http://code.google.com/p/rfdoc/',
        license      = 'Apache License 2.0',
        package_dir  = {'rfdoc': 'src/rfdoc'},
        packages     = ['rfdoc', 'rfdoc.rfdocapp', 'rfdoc.rfdocapp.views',
                        'rfdoc.rfdocapp.templatetags', 'rfdoc.rfdocapp.utils'],
        package_data = {'rfdoc': ['*.tmpl', 'rfdocapp/templates/*.html']}
        )


if __name__ == "__main__":
    main()
