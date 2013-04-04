#!/bin/bash
#
# Run the PyUnit tests
#
# This must be set to the path for the bolt top-level directory
export BOLT_DIR=..
export PYTHONPATH=$BOLT_DIR/modules
python testJob.py
python testDistribution.py
