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
A python class to represent a simulation code

This class is part of the bolt job submission script generation 
tool. The properties of the class are read from a configuration 
file that uses the [ConfigParser] module.
"""
__author__ = "A. R. Turner, EPCC"

class Code(object):
    def __init__(self):
        """The default constructor - setup an simulation code system"""
        self.__name = None
        self.__desc = None

        self.__parallel = None
        self.__serial = None
        self.__hybrid = None

        self.__maxTasks = 1
        self.__minTasks = 1

        self.__preamble = None
        self.__postamble = None

    # Properties
    # Code info
    @property
    def name(self):
        """The simulation code name"""
        return self.__name
    @property
    def desc(self):
        """A description of the code"""
        return self.__submitCommand

    # Methods
    def readConfig(self, fileName):
        """Read the code properties from a config file that uses the 
        ConfigParser module.

        Arguments:
           str  fileName  - The file to read the code configuration from
        """
        import ConfigParser

        # Set up the config for this object
        codeConfig = ConfigParser.SafeConfigParser()
        codeConfig.read(fileName)

        # Get the batch information options
        self.__name = codeConfig.get("system info", "name")

    def summaryString(self):
            """Return a string summarising the code.

               Return:
                  str  output  - The string summarising the code
            """
            return "| {0:<10} |".format(self.name)
