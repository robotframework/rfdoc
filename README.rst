RFDoc
=====

Introduction
------------

RFDoc is a web application for storing and searching `Robot Framework
<http://robotframework.org>` test library and resource file documentations.

RFDoc is implemented using `Django web framework <http://djangoproject.com>` version 4.0 or higher.

**Note:** This project is currently not actively maintained.

License
-------

RFDoc is licensed under Apache License 2.0.

See LICENSE.txt for details.

Running RFDoc
-------------

For getting RFDoc to run locally, see
https://github.com/robotframework/rfdoc/blob/wiki/DevelopmentEnvironment.md

**Note:** In section 'Set up the database' replace

```
python -m rfdoc.manage syncdb
```
with
```
python -m rfdoc.manage migrate --run-syncdb
```

For setting up a public production server, see
https://github.com/robotframework/rfdoc/blob/wiki/ProductionEnvironment.md

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

Acceptance tests are run using ``atest/run_atests.py``.

Run the script without any arguments for help.
