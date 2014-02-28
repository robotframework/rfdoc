# Django settings for RFDoc project.
#
# Local configuration should be done in `rfdocsettings.py` file as explained
# in `rfdocsettings_defaults.py`.

from os.path import dirname, join

import rfdocsettings_defaults
try:
    import rfdocsettings
except ImportError:
    rfdocsettings = None


# Helper method to get settings either from `rfdocsettings.py`
# or `rfdocsettings_defaults.py`.
def localsetting(name):
    try:
        return getattr(rfdocsettings, name)
    except AttributeError:
        return getattr(rfdocsettings_defaults, name)

## The following settings can be overridden in own settings

PRODUCTION = localsetting('PRODUCTION')
DEBUG = localsetting('DEBUG')
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = localsetting('TIME_ZONE')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': localsetting('DATABASE_NAME')
    }
}
ALLOWED_HOSTS = localsetting('ALLOWED_HOSTS')

### The following settings are not overridable

_PROJECT_DIR = dirname(__file__)
SITE_ID = 1
USE_I18N = False
SECRET_KEY = 'pmst_958#g=ks#i+(ci!pnf5=1b73@nf(c%h8)p&sc7wongki6'
ROOT_URLCONF = 'rfdoc.urls'
STATIC_URL = '/static/'
STATIC_ROOT = join(_PROJECT_DIR, 'rfdocapp', 'static')
TEMPLATE_DIRS = (
    join(_PROJECT_DIR, 'rfdocapp', 'templates').replace('\\', '/')
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rfdoc.rfdocapp'
)

# CSRF removed from the defaults due to src/rfdoc/upload.py
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)
