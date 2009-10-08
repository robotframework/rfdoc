#!/usr/bin/env python

"""Runner for RFDoc acceptance tests.

Usage:  python run_atests.py mode [options]

This script executes RFDoc's acceptance tests using Robot Framework and
SeleniumLibrary. Valid values for `mode` are (case-insensitively):

REGR    Run acceptance tests so that both RFDoc and Selenium server are
        started before the execution and closed afterwards.
DEVEL   Same as REGR but RFDoc and Selenium server are not started nor
        stopped. They must thus be running before executing this script.
        Another precondition is that RFDoc is started as described below.
        Set `atest` directory to PYTHONPATH and start RFDoc with command:         
        django-admin runserver --settings atest_settings (linux, mac)
        django-admin.py runserver --settings atest_settings (windows)
CI      Only to be used for continuous integration.

Accepted `options` are same as accepted by Robot Framework and they are passed
to it directly. Options can be used, for example, to select tests or suites
to be executed (by default the whole `atest/rfdoc` directory is executed), and
to specify the browser to be used (the default is Firefox).

All outputs are written `atests/results` directory. In addition to the normal
logs and reports they include also logs from the Selenium server and the
server where RFDoc is running.

Running tests requires Django, Robot Framework (2.1 or newer), SeleniumLibrary
(2.2 or newer), Python (2.4-2.6) and Java (1.5 or newer).

Examples:
  $ python run_atests.py regr
  $ python run_atests.py devel --variable BROWSER:IE --suite upload
"""

import os
from os.path import abspath, basename, dirname, exists, join
import sys
import time
from shutil import rmtree, copyfile
from subprocess import Popen, call, STDOUT, PIPE

import SeleniumLibrary


ATEST = dirname(__file__)
RESULTS = join(ATEST, 'results')
SHELL = os.name == 'nt'
ADMIN = 'django-admin.py'
try:
    call(ADMIN, stderr=PIPE, shell=SHELL)
except OSError:
    ADMIN = 'django-admin' # No extension in linux
    try:
        call(ADMIN, stderr=PIPE, shell=SHELL)
    except OSError:
        raise RuntimeError('Could not find django-admin from PATH')

if exists(RESULTS):
    rmtree(RESULTS)
os.mkdir(RESULTS)

# Make sure atest/atest_settings.py is used
os.environ['PYTHONPATH'] = ATEST + os.pathsep + os.getenv('PYTHONPATH', '')
os.environ['DJANGO_SETTINGS_MODULE'] = 'atest_settings'


class DevelRunner:

    def __init__(self):
        copyfile(join(ATEST, 'testdata', 'libraries.db'),
                 join(RESULTS, 'rfdoc.db'))

    def run_tests(self, options):
        lib, data = join(ATEST, 'lib'), join(ATEST, 'rfdoc')
        pipe = Popen(['pybot', '--OutputDir', RESULTS, '--SuiteStatLevel', '2',
                      '--TagStatCombine', '*NOTNotReady:Regression_Tests', 
                      '--NonCritical', 'NotReady', '--PythonPath', lib] + options + [data],
                     shell=SHELL)
        return pipe.wait()

    def finalize(self):
        pass
    

class RegressionRunner(DevelRunner):

    def __init__(self):
        DevelRunner.__init__(self)
        self._start_selenium()
        self._start_rfdoc()

    def run_tests(self, options):
        regr_opts = ['--variable', 'RFDOC_PORT:8001',
                     '--variable', 'SELENIUM_PORT:4445']
        DevelRunner.run_tests(self, regr_opts + options)

    def finalize(self):
        DevelRunner.finalize(self)
        self._stop_selenium()
        self._stop_rfdoc()

    def _start_selenium(self):
        self._selenium_log = open(join(RESULTS, 'selenium.log'), 'w')
        selenium_jar = join(dirname(SeleniumLibrary.__file__), 'lib',
                            'selenium-server.jar')
        process = Popen(['java', '-jar', selenium_jar, '-port', '4445'],
                        stdout=self._selenium_log, stderr=STDOUT)
        
    def _start_rfdoc(self): 
        self._rfdoc_log = open(join(RESULTS, 'rfdoc.log'), 'w')
        process = Popen([ADMIN, 'runserver', '8001'], shell=SHELL,
                        stdout=self._rfdoc_log, stderr=STDOUT)
        self._rfdoc_pid = process.pid

    def _stop_selenium(self):
        SeleniumLibrary.shut_down_selenium_server(port=4445)
        self._selenium_log.close()
    
    def _stop_rfdoc(self):
        if os.name == 'nt':
            self._kill_rfdoc_on_windows()
        else:
            self._kill_rfdoc_on_posix()
        self._rfdoc_log.close()

    def _kill_rfdoc_on_windows(self):
        call('TASKKILL /PID %d /T /F' % self._rfdoc_pid, stdout=PIPE)

    def _kill_rfdoc_on_posix(self):
        # We couldn't figure out other way to kill all RFDoc related processes
        # ('manage.py runserver' starts one child process) than sending
        # KeyboardInterrupt to the whole process group and ignoring it here
        # TODO: Isn't "os.getpgid(self._rfdoc_pid) == os.getpid()"?
        try:
            os.killpg(os.getpgid(self._rfdoc_pid), 2)
        except KeyboardInterrupt:
            pass


class CiRunner(RegressionRunner):

    def run_tests(self, options):
        RegressionRunner.run_tests(self, ['--monitorcolors', 'off'] + options)

    def _kill_rfdoc_on_posix(self):
        os.system('pkill -9 -P %d' % self._rfdoc_pid)


class StartUpError(Exception):
    pass


if __name__ == '__main__':
    runners = {'devel': DevelRunner, 'regr': RegressionRunner, 'ci': CiRunner}
    try:
        runner = runners[sys.argv[1].lower()]()
    except (KeyError, IndexError):
        print __doc__
        sys.exit(-1)
    except StartUpError, err:
        print 'ERROR:', err
        sys.exit(-1)
    rc = runner.run_tests(sys.argv[2:])
    runner.finalize()
    sys.exit(rc)
