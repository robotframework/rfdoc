import os
from subprocess import call, PIPE

SHELL = os.name == 'nt'
ADMIN = 'django-admin.py'
try:
    call(ADMIN, stderr=PIPE, shell=SHELL)
except OSError:
    ADMIN = 'django-admin'  # No extension in linux 
    try:
        call(ADMIN, stderr=PIPE, shell=SHELL)
    except OSError:
        raise RuntimeError('Could not find django-admin from PATH')


def clear_rfdoc_database():
    rc = call([ADMIN, 'reset', '--noinput', 'rfdocapp'], shell=SHELL)
    if rc != 0:
        raise AssertionError('Clearing RFDoc database failed')

