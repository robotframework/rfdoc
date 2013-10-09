# Django settings for RFDoc project acceptance tests.

import sys
from os.path import dirname, join

sys.path.append(join(dirname(__file__), '..', 'src', 'rfdoc'))
import settings
from settings import *

from django.core.management import setup_environ
setup_environ(settings)


DEBUG = True

TIME_ZONE = 'Europe/Helsinki'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(dirname(__file__), 'results', 'rfdoc.db')
    }
}
