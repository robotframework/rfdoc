#!/usr/bin/env python

"""Usage: python run_atests.py mode [options]

This script executes RFDoc's acceptance tests using Selenium2Library.

Valid `mode` is one of the following:
    regr    Run acceptance tests so that RFDoc is started before
            the test execution and closed after it.
            RFDoc is started on port 7000.

    devel   Runs acceptance tests so that RFDoc is not started nor stopped.
            The server must be started before executing as following:
            django-admin.py runserver 7000 --pythonpath=atest/ --settings atest_settings

    ci      Used at continuous integration servers.
            Basically same as 'devel' but disables colored test outputs.

Valid `options` are the same as accepted by Robot Framework and they are passed
to it directly.

All outputs are written `atests/results` directory.

Running the acceptance tests requires the following:
- Python (2.6 or newer)
- Django (1.5 or newer)
- Robot Framework (2.6 or newer)
- Selenium2Library (TODO or newer)

Examples:
    $ ./run_atests.py regr
    $ ./run_atests.py devel --variable BROWSER:IE --suite upload
"""

import os
import signal
import sys
from os.path import dirname, exists, join
from shutil import rmtree, copyfile
from subprocess import Popen, PIPE


ATEST_PATH = dirname(__file__)
ATEST_LIB_PATH = join(ATEST_PATH, 'lib')
ATEST_RESULTS_PATH = join(ATEST_PATH, 'results')
SHELL = os.name == 'nt'


class DevelopmentRunner(object):

    def __init__(self):
        self._set_paths()
        self._remove_old_results()
        self._copy_database()

    def _set_paths(self):
        os.environ['PYTHONPATH'] = ATEST_PATH + os.pathsep +\
                                   ATEST_LIB_PATH + os.pathsep +\
                                   os.getenv('PYTHONPATH', '')
        os.environ['DJANGO_SETTINGS_MODULE'] = 'atest_settings'

    def _remove_old_results(self):
        if exists(ATEST_RESULTS_PATH):
            rmtree(ATEST_RESULTS_PATH)
            os.mkdir(ATEST_RESULTS_PATH)

    def _copy_database(self):
        copyfile(join(ATEST_PATH, 'testdata', 'libraries.db'),
                 join(ATEST_RESULTS_PATH, 'rfdoc.db'))

    def run_tests(self, options):
        command = ['pybot', '-o', ATEST_RESULTS_PATH] + options + [ATEST_PATH]
        process = Popen(command, shell=SHELL)
        return process.wait()

    def finalize(self):
        pass


class RegressionRunner(DevelopmentRunner):

    def __init__(self):
        DevelopmentRunner.__init__(self)
        self._rfdoc_pid = self._start_rfdoc()

    def run_tests(self, options):
        DevelopmentRunner.run_tests(self, options)

    def finalize(self):
        DevelopmentRunner.finalize(self)
        self._stop_rfdoc()

    def _start_rfdoc(self):
        command = ['django-admin.py', 'runserver', '7000']
        process = Popen(command, stderr=PIPE, shell=SHELL)
        return process.pid

    def _stop_rfdoc(self):
        if os.name == 'nt':
            self._kill_rfdoc_on_windows()
        else:
            self._kill_rfdoc_on_posix()

    def _kill_rfdoc_on_windows(self):
        Popen('taskkill /t /f /pid %d' % self._rfdoc_pid, stdout=PIPE)

    def _kill_rfdoc_on_posix(self):
        os.killpg(os.getpgrp(), signal.SIGKILL)


class CiRunner(RegressionRunner):

    def run_tests(self, options):
        RegressionRunner.run_tests(self, ['--monitorcolors', 'off'] + options)


if __name__ == '__main__':
    runners = {
        'devel': DevelopmentRunner,
        'regr': RegressionRunner,
        'ci': CiRunner
    }
    try:
        runner = runners[sys.argv[1].lower()]()
    except (IndexError, KeyError):
        sys.stdout.write(__doc__)
        sys.exit(-1)
    except Exception, message:
        sys.stderr.write('error: %s\n' % message)
        sys.exit(-1)
    rc = runner.run_tests(sys.argv[2:])
    runner.finalize()
    sys.exit(rc)
