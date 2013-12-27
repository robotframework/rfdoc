"""
WSGI config for RFDoc.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

THIS_PATH = os.path.join(os.path.dirname(__file__))
sys.path.append(THIS_PATH)
sys.path.append(os.path.join(THIS_PATH, '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfdoc.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
