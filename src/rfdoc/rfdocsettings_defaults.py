# Local RFDoc configuration file used by `settings.py`.
#
# `rfdocsettings_defaults.py` contains the default values to use.
# However, it should not be edited directly, but first copied to
# `rfdocsettings.py`.
#
# Settings are first read from `rfdocsettings.py` and then from
# `rfdocsettings_defaults.py`. Thus `rfdocsettings.py` only needs to have
# the settings that are different to defaults.
#
# Notice that `rfdocsettings.py` can be anywhere in the file system, as long
# it is in PYTHONPATH.

# If PRODUCTION is True, static assets must be served by a separate web server.
PRODUCTION = False

# If DEBUG is True, stack traces are shown instead of normal 404 and 500 pages.
DEBUG = False

# Path to the sqlite3 database file. The default location is in system temporary
# directory which can be automatically cleared. You should therefore change the path
# unless using RFDoc for testing purposes.
import os, tempfile
DATABASE_NAME = os.path.join(tempfile.gettempdir(), 'rfdoc.db')

# A list of strings representing the host/domain names that this Django site
# can serve. If you are in PRODUCTION, please set this according to your hosts.
#
# For more information, see:
# https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

# Local time zone for this installation.
#
# Choices are listed at http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
#
# If running on Windows, this must be set to the same as your system time zone.
TIME_ZONE = 'Europe/Helsinki'
