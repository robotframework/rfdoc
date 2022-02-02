#!/usr/bin/env python

"""Usage: python run_atests.py mode [options]

This script executes RFDoc's acceptance tests using Selenium2Library.

Valid `mode` is one of the following:
    regr    Run acceptance tests so that RFDoc is started before
            the test execution and closed after it.
            RFDoc is started on port 7000.

    devel   Runs acceptance tests so that RFDoc is not started nor stopped.
            The server must be started before executing as following:
            python -m rfdoc.manage runserver --pythonpath=atest/ --settings atest_settings

    ci      Used at continuous integration servers.
            Basically same as 'devel' but disables colored test outputs.

Valid `options` are the same as accepted by Robot Framework and they are passed
to it directly.

All outputs are written `atests/results` directory.

Running the acceptance tests requires the following:
- Python (2.6 or newer)
- Django (1.5 or 1.6)
- Robot Framework (2.6 or newer)
- Selenium2Library

Examples:
    $ ./run_atests.py regr
    $ ./run_atests.py devel --variable BROWSER:IE --suite upload
"""

import os
import signal
import sys
from os.path import dirname, join
from subprocess import call, PIPE, Popen


ATEST_PATH = dirname(__file__)
ATEST_RESULTS_PATH = join(ATEST_PATH, 'results')
DJANGO_ADMIN = join(ATEST_PATH, '..', 'src', 'rfdoc', 'manage.py')
SHELL = os.name == 'nt'

try:
    call([DJANGO_ADMIN], stderr=PIPE, stdout=PIPE, shell=SHELL)
except OSError:
    sys.stderr.write('error: Could not find %s from PATH\n' % DJANGO_ADMIN)
    exit(-1)


class DevelopmentRunner(object):

    def run_tests(self, options):
        command = ['robot', '-d', ATEST_RESULTS_PATH] + options + [ATEST_PATH]
        process = Popen(command, shell=SHELL)
        return process.wait()

    def finalize(self):
        pass


class RegressionRunner(DevelopmentRunner):

    def __init__(self):
        self._rfdoc_pid = self._start_rfdoc()

    def _start_rfdoc(self):
        command = [DJANGO_ADMIN, 'runserver',
                   '--pythonpath', ATEST_PATH,
                   '--settings', 'atest_settings',
                   '7000']
        process = Popen(command, stderr=PIPE, shell=SHELL)
        return process.pid

    def run_tests(self, options):
        super().run_tests(options)

    def finalize(self):
        super().finalize()
        self._stop_rfdoc()

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
    except Exception as message:
        sys.stderr.write('error: %s\n' % message)
        sys.exit(-1)
    rc = runner.run_tests(sys.argv[2:])
    runner.finalize()
    sys.exit(rc)
