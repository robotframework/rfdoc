#!/bin/bash

DJANGO_COMMAND=${1:-runserver}
shift
python src/rfdoc/manage.py $DJANGO_COMMAND $@
