# Django settings for RFDoc project acceptance tests.

import sys
from os.path import abspath, dirname, join


_SRCDIR = join(dirname(abspath(__file__)), '..', 'src' )
_RFDOCDIR = join(_SRCDIR, 'rfdoc')
sys.path = [_SRCDIR, _RFDOCDIR] + sys.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Helsinki'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(dirname(__file__), 'results', 'rfdoc.db')
    }
}

ALLOWED_HOSTS = ['localhost']

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pmst_958#g=ks#i+(ci!pnf5=1b73@nf(c%h8)p&sc7wongki6'

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

TEMPLATE_DIRS = (
    join(_RFDOCDIR, 'rfdocapp', 'templates').replace('\\', '/'),
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
