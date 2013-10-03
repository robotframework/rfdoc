# Django settings for RFDoc project.
#
# Local configuration should be done in `rfdocsettings.py` file as explained
# in `rfdocsettings_defaults.py`. More settings can be made configurable that
# way if there is a need.

import os

import rfdocsettings_defaults
try:
    import rfdocsettings
except ImportError:
    rfdocsettings = None


# Path to the directory containing this file. Don't edit!
_BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Helper method to get local settings either from `rfdocsettings.py`
# or `rfdocsettings_defaults.py`.
def localsetting(name):
    try:
        return getattr(rfdocsettings, name)
    except AttributeError:
        return getattr(rfdocsettings_defaults, name)


DEBUG = localsetting('DEBUG')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3' 
DATABASE_NAME = localsetting('DATABASE_NAME')
TIME_ZONE = localsetting('TIME_ZONE')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pmst_958#g=ks#i+(ci!pnf5=1b73@nf(c%h8)p&sc7wongki6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'rfdoc.urls'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
    os.path.join(_BASEDIR, 'rfdocapp', 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'rfdoc.rfdocapp'
)
