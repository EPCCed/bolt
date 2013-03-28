#!/bin/bash
#
# Run the PyUnit tests
#
# This must be set to the path for the bolt top-level directory
export BOLT_DIR=..
python testJob.py
python testDistribution.py
