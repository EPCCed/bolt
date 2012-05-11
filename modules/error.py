"""
Module for handling errors.

Routines to do something useful with error messages.
"""
__author__ = "A. R. Turner, EPCC"

from textwrap import fill
import sys
def handleError(errMsg, errCode = 1):
        printError(errMsg)
        exit(errCode)

def printError(errMsg):
        sys.stderr.write(fill("**ERROR** " + errMsg) + "\n\n")

def printWarning(warnMsg):
        sys.stderr.write(fill("++Warning++ " + warnMsg) + "\n\n")

