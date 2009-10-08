# Django settings for RFDoc project acceptance tests.

from os.path import abspath, dirname, join
import sys

_SRCDIR = join(dirname(abspath(__file__)), '..', 'src' )
_RFDOCDIR = join(_SRCDIR, 'rfdoc')
sys.path = [_SRCDIR, _RFDOCDIR] + sys.path

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3' 
DATABASE_NAME = join(dirname(__file__), 'results', 'rfdoc.db')
TIME_ZONE = 'Europe/Helsinki'

SITE_ID = 1

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'rfdoc.urls'

TEMPLATE_DIRS = (
    join(_SRCDIR, 'rfdocapp', 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'rfdoc.rfdocapp'
)
