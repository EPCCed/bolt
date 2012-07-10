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
        self.__message = None
        self.__allowSubmit = False

        self.__parallel = None
        self.__serial = None
        self.__hybrid = None

        self.__maxTasks = 1
        self.__minTasks = 1

        self.__preamble = None
        self.__postamble = None

    # Properties ==============================================================
    # Code info
    @property
    def name(self):
        """The simulation code name"""
        return self.__name
    @property
    def desc(self):
        """A description of the code"""
        return self.__desc
    @property
    def message(self):
        """Any text to display when a user sets up a job for this code"""
        return self.__message
    @property
    def allowSubmit(self):
        """Can bolt submit this type of job directly?"""
        return self.__allowSubmit
    # Job types allowed
    @property
    def parallel(self):
        """Can the code be run as a distributed memory parallel job?"""
        return self.__parallel
    @property
    def serial(self):
        """Can the code be run as a serial job?"""
        return self.__serial
    @property
    def hybrid(self):
        """Can the code be run as a hybrid distributed-/shared-memory job?"""
        return self.__hybrid
    # Task numbers
    @property
    def maxTasks(self):
        """The maximum number of tasks that can be selected for jobs using
           this code."""
        return self.__maxTasks
    @property
    def minTasks(self):
        """The minimum number of tasks that can be selected for jobs using
           this code."""
        return self.__minTasks
    # Script commands
    @property
    def preamble(self):
        """Any commands to be run in the script before the job runs."""
        return self.__preamble
    @property
    def postamble(self):
        """Any commands to be run in the script after the job runs."""
        return self.__postamble

    # Methods ==============================================================
    def readConfig(self, fileName):
        """Read the code properties from a configuration file that uses the 
        ConfigParser module.

        Arguments:
           str  fileName  - The file to read the code configuration from
        """
        import ConfigParser

        # Set up the config for this object
        codeConfig = ConfigParser.SafeConfigParser()
        codeConfig.read(fileName)

        # Get the batch information options
        self.__name = codeConfig.get("code info", "name")
        self.__desc = codeConfig.get("code info", "description")
        self.__message = codeConfig.get("code info", "runtime message")
        self.__allowSubmit = codeConfig.getboolean("code info", "allow direct submission")

        self.__parallel = codeConfig.get("job types", "parallel")
        self.__serial = codeConfig.get("job types", "serial")
        self.__hybrid = codeConfig.get("job types", "hybrid")

        self.__maxTasks = codeConfig.getint("job limits", "maximum tasks")
        self.__minTasks = codeConfig.getint("job limits", "minimum tasks")

        self.__preamble = codeConfig.get("script commands", "preamble")
        self.__postamble = codeConfig.get("script commands", "postamble")

    def summaryString(self):
            """Return a string summarising the code.

               Return:
                  str  output  - The string summarising the code
            """
            return "| {0:<10} |".format(self.name)
