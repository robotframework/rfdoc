# Local RFDoc configuration file.
#
# Settings are first read from `rfdocsettings.py` and then from
# `rfdocsettings_defaults.py`. Thus `rfdocsettings.py` only needs to have
# the settings that are different to the defaults.
#
# Notice that `rfdocsettings.py` can be anywhere in the file system,
# as long as it is in your PYTHONPATH when running RFDoc.


# If PRODUCTION is True, static assets must be served by a separate web server.
PRODUCTION = False

# If DEBUG is True, stack traces are shown instead of normal 404 and 500 pages.
DEBUG = False

# Path to the SQLite3 database file. The default location is in system temporary
# directory which can be automatically cleared. You should therefore always
# change the path unless using RFDoc for testing purposes.
import os, tempfile
DATABASE_NAME = os.path.join(tempfile.gettempdir(), 'rfdoc.db')

# A list of strings representing the host/domain names that this Django site
# can serve.
#
# If this RFDoc instance is accessible from the public Internet, please set
# this according to your hosts unless you want compromise security.
# For more information, see:
# https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# Local time zone for this installation.
#
# Choices are listed at http://en.wikipedia.org/wiki/List_of_tz_zones_by_name,
# although not all choices may be available on all operating systems.
#
# If running on Windows, this must be set to the same as your system time zone.
TIME_ZONE = 'Europe/Helsinki'


# --- NO NEED TO EDIT BELOW ---
from shutil import copy
if __name__ == "__main__":
    TARGET_FILE = 'rfdocsettings.py'
    if os.path.exists(TARGET_FILE):
        msg = "File '%s' exists. Do you want to override it?" % TARGET_FILE
        if not raw_input('%s (y/n, n default) > ' % msg).lower() == 'y':
            exit('Aborted.\n')
    copy(__file__, TARGET_FILE)
    print "\nCreated a new setting file '%s'. Make sure it is found in your " \
          "PYTHONPATH before running RFDoc. The correct path to append to " \
          "your PYTHONPATH seems to be: %s" % (TARGET_FILE, os.getcwd())
