RFDoc
=====

Introduction
------------

RFDoc (http://code.google.com/p/rfdoc) is a web application for storing
and searching Robot Framework (http://robotframework.org) test library and
resource file documentations.

RFDoc is implemented using Django web framework (http://djangoproject.com).


License
-------

SSHLibrary is licensed under Apache License 2.0.

See LICENSE.txt for details.


Running RFDoc
-------------

For getting RFDoc to run locally, see
https://code.google.com/p/rfdoc/wiki/DevelopmentEnvironment

For setting up a public production server, see
https://code.google.com/p/rfdoc/wiki/ProductionEnvironment


Directory Layout
----------------

atest/
    Acceptance tests. Naturally using Robot Framework.

src/
    RFDoc source code.

tools/
    Utilities to use as part of the CI pipeline or as SCM hooks.


Running the Acceptance Tests
----------------------------

Acceptance tests are run using `atest/run_atests.py`

Run the script without any arguments for help.
