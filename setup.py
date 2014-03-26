#!/usr/bin/env python

try:
    from setuptools import setup
    requires = {
        'install_requires': ['django >= 1.5, < 1.7'],
    }
except ImportError:
    from distutils.core import setup
    requires = {}

from os.path import abspath, dirname, join

execfile(join(dirname(abspath(__file__)), 'src', 'rfdoc', 'version.py'))

# Maximum width in Windows installer seems to be 70 characters -------|
DESCRIPTION = """
RFDoc is a web application for storing and searching Robot Framework
test library and resource file documentations.

Required packages:
    django >= 1.5
"""[1:-1]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(
    name             = 'robotframework-rfdoc',
    version          = VERSION,
    description      = 'Web-based Robot Framework library documentation server',
    long_description = DESCRIPTION,
    author           = 'Robot Framework Developers',
    author_email     = 'robotframework-devel@googlegroups.com',
    url              = 'http://code.google.com/p/rfdoc/',
    license          = 'Apache License 2.0',
    keywords         = 'robotframework testing testautomation documentation',
    platforms        = 'any',
    classifiers      = CLASSIFIERS.splitlines(),
    package_dir      = {'rfdoc': 'src/rfdoc'},
    packages         = ['rfdoc', 'rfdoc.rfdocapp', 'rfdoc.rfdocapp.views',
                        'rfdoc.rfdocapp.templatetags', 'rfdoc.rfdocapp.utils'],
    package_data     = {'rfdoc': ['*.tmpl', 'rfdocapp/templates/*.html',
                                  'rfdocapp/static/*.css',
                                  'rfdocapp/static/*.js']},
    **requires
)
