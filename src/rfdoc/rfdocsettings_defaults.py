# Local RFDoc configuration file used by `settings.py`.
#
# `rfdocsettings_defaults.py` contains the default values to use. It should
# not be edited directly, however, but first copied to `rfdocsettings.py`.
# All values are looked first from `rfdocsettings.py` and then from
# `rfdocsettings_defaults.py`, and thus the former only needs to have
# settings that are different to defaults.
#
# Notice that `rfdocsettings.py` can be anywhere in the file system as long
# it is in the PYTHONPATH.

import os
import tempfile


# If debug is True, stack traces are shown instead of normal 404 and 500 pages.
DEBUG = False

# Path to the database file used by sqlite3
DATABASE_NAME = os.path.join(tempfile.gettempdir(), 'rfdoc.db')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'
