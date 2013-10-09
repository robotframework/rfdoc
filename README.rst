RFDoc
=====

Introduction
------------

RFDoc (http://code.google.com/p/rfdoc) is a web-based application for storing
and searching Robot Framework (http://robotframework.org) test library and
resource file documentations.

RFdoc is implemented using Django web framework (http://djangoproject.com).


License
-------

SSHLibrary is licensed under Apache License 2.0.

See LICENSE.txt for details.


Setup
-----

For instructions, see
https://code.google.com/p/rfdoc/wiki/InstallationInstructions.


Directory Layout
----------------

atest/
    Acceptance tests. Naturally using Robot Framework.

db/
    The default location for database.

src/
    RFDoc source code.

tools/
    Scripts to use as part of CI pipeline or as SCM repository hooks.


Running the Acceptance Tests
----------------------------

Acceptance tests are run using `atest/run_atests.py`

Run the script without any arguments for help.
