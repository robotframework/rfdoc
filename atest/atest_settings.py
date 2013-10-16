# Django settings for RFDoc project acceptance tests.

import sys
from os.path import dirname, join
from django.core.management import setup_environ

sys.path.append(join(dirname(__file__), '..', 'src', 'rfdoc'))
import settings
from settings import *


setup_environ(settings)

DEBUG = True
DATABASES['default']['NAME'] = join(dirname(__file__), 'results', 'rfdoc.db')
