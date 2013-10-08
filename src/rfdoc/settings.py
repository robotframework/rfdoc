# Django settings for RFDoc project.
#
# Local configuration should be done in `rfdocsettings.py` file as explained
# in `rfdocsettings_defaults.py`. More settings can be made configurable that
# way if there is a need.

from os.path import abspath, dirname, join

import rfdocsettings_defaults
try:
    import rfdocsettings
except ImportError:
    rfdocsettings = None


# Helper method to get local settings either from `rfdocsettings.py`
# or `rfdocsettings_defaults.py`.
def localsetting(name):
    try:
        return getattr(rfdocsettings, name)
    except AttributeError:
        return getattr(rfdocsettings_defaults, name)


DEBUG = localsetting('DEBUG')
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = localsetting('TIME_ZONE')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': localsetting('DATABASE_NAME')
    }
}

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# If this is false, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pmst_958#g=ks#i+(ci!pnf5=1b73@nf(c%h8)p&sc7wongki6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'rfdoc.urls'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
    join(dirname(abspath(__file__)), 'rfdocapp', 'templates').replace('\\', '/'),
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
