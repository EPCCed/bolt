#----------------------------------------------------------------------
# Copyright 2012 EPCC, The University of Edinburgh
#
# This file is part of bolt.
#
# bolt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bolt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bolt.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------
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

