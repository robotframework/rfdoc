# Django settings for RFDoc project acceptance tests.

import sys
from os.path import abspath, join

sys.path.append(abspath(join('..', 'src', 'rfdoc')))

from django.core.management import setup_environ
import settings
setup_environ(settings)
from rfdoc.settings import *


DEBUG = True

TIME_ZONE = 'Europe/Helsinki'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join('results', 'rfdoc.db')
    }
}
