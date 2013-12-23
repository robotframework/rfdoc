# Django settings for RFDoc project acceptance tests.

import sys
from os.path import dirname, join

sys.path.append(join(dirname(__file__), '..', 'src'))
from rfdoc.settings import *

DEBUG = True
DATABASES['default']['NAME'] = join(dirname(__file__), 'results', 'rfdoc.db')
