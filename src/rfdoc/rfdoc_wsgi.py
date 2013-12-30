"""
WSGI config for RFDoc.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import site
import sys

# Site-packages reside inside the virtualenv
SITE_PACKAGES_PATH = os.path.join(os.path.expanduser('~'), 'venv', 'lib',
    'python2.7', 'site-packages')

# Adds site-packages to the PATH
prev_sys_path = list(sys.path)
site.addsitedir(SITE_PACKAGES_PATH)
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# Defines the name of the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfdoc.settings")

# Initializes WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
