#!/bin/bash

ATEST_DIR=`cd $(dirname "${BASH_SOURCE}") && pwd`

xvfb-run $ATEST_DIR/run_atests.py ci
