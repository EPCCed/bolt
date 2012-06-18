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
A python class to represent a batch system

This class is part of the bolt job submission script generation 
tool. The properties of the class are read from a configuration 
file that uses the [ConfigParser] module.
"""
__author__ = "A. R. Turner, EPCC"

class Batch(object):
    def __init__(self):
        """The default constructor - setup an empty batch system"""
        self.__name = ""
        self.__submitCommand = None

        self.__optionID = None
        self.__nameOption = None
        self.__accountOption = None
        self.__queueOption = None

        self.__parallelTasksOption = None
        self.__parallelTimeOption = None
        self.__parallelOptions = None
        self.__parallelScriptPreamble = None
        self.__parallelScriptPostamble = None

        self.__serialTimeOption = None
        self.__serialOptions = None
        self.__serialScriptPreamble = None
        self.__serialScriptPostamble = None

    # Properties
    # Batch system info
    @property
    def name(self):
        """The batch system name"""
        return self.__name
    # Batch system info
    @property
    def submitCommand(self):
        """The command used to submit a batch job"""
        return self.__submitCommand

    # Batch system options
    @property
    def optionID(self):
        """The tag that identifies batch options in a job submission script.
        For example '#PBS' for the PBS batch system."""
        return self.__optionID
    @property
    def nameOption(self):
        """The option used to specify the job name. For example '-N' for the
        PBS batch system"""
        return self.__nameOption
    @property
    def accountOption(self):
        """The option used to specify the account name. For example '-A' for the
        PBS batch system"""
        return self.__accountOption
    @property
    def queueOption(self):
        """The option used to specify the account name. For example '-q' for the
        PBS batch system"""
        return self.__queueOption

    # Parallel job options
    @property
    def parallelTasksOption(self):
        """The option used to specify the account name. For example '-l' for the
        PBS batch system"""
        return self.__parallelTasksOption
    @property
    def parallelTimeOption(self):
        """The option used to specify the job time. For example '-l walltime='
        for the PBS batch system"""
        if (self.__parallelTimeOption.rfind("=") or self.__parallelTimeOption.rfind(":")) == -1:
            return self.__parallelTimeOption + " "
        else:
            return self.__parallelTimeOption
    @property
    def parallelOptions(self):
        """Any additonal batch options for parallel jobs (without tag)"""
        return self.__parallelOptions
    @property
    def parallelScriptPreamble(self):
        """Any script commands to run before a parallel application is launched"""
        return self.__parallelScriptPreamble
    @property
    def parallelScriptPostamble(self):
        """Any script commands to run after a parallel application is finished"""
        return self.__parallelScriptPostamble

    @property
    def serialTimeOption(self):
        """The option used to specify the job time. For example '-l h_rt='
        for the PBS batch system"""
        if (self.__serialTimeOption.rfind("=") or self.__serialTimeOption.rfind(":")) == -1:
            return self.__serialTimeOption + " "
        else:
            return self.__serialTimeOption
    @property
    def serialOptions(self):
        """Any additonal batch options for serial jobs (without tag)"""
        return self.__serialOptions
    @property
    def serialScriptPreamble(self):
        """Any script commands to run before a parallel application is launched"""
        return self.__serialScriptPreamble
    @property
    def serialScriptPostamble(self):
        """Any script commands to run after a parallel application is finished"""
        return self.__serialScriptPostamble

    # Methods
    def readConfig(self, fileName):
        """Read the batch system properties from a config file that uses the 
        ConfigParser module.

        Arguments:
           str  fileName  - The file to read the batch configuration from
        """
        import ConfigParser

        # Set up the config for this object
        batchConfig = ConfigParser.SafeConfigParser()
        batchConfig.read(fileName)

        # Get the batch information options
        self.__name = batchConfig.get("system info", "name")
        self.__submitCommand = batchConfig.get("system info", "submit command")

        # Get the batch options
        self.__optionID = batchConfig.get("basic options", "option identifier")
        self.__nameOption = batchConfig.get("basic options", "job name option")
        self.__accountOption = batchConfig.get("basic options", "account option")
        self.__queueOption = batchConfig.get("basic options", "queue option")

        # Get the parallel options
        self.__parallelTasksOption = batchConfig.get("parallel options", "task option")
        self.__parallelTimeOption = batchConfig.get("parallel options", "time option")
        self.__parallelOptions = batchConfig.get("parallel options", "additional options")
        self.__parallelScriptPreamble = batchConfig.get("parallel options", "script preamble")
        self.__parallelScriptPostamble = batchConfig.get("parallel options", "script postamble")

        # Get the serial options
        self.__serialTimeOption = batchConfig.get("serial options", "time option")
        self.__serialOptions = batchConfig.get("serial options", "additional options")
        self.__serialScriptPreamble = batchConfig.get("serial options", "script preamble")
        self.__serialScriptPostamble = batchConfig.get("serial options", "script postamble")

    def getParallelOptionLines(self, jobName, queueName, envOption, pUnits, runtime, accountID):
            """Generate the parallel batch submission option lines so they can 
               be written to a job submission script
            
               Arguments:
                  str    jobName    - The name of the job
                  str    queueName  - The name of the queue to use
                  str    envOption  - The parallel environment option
                  int    pUnits     - Number of parallel units to request
                  str    runtime    - The job runtime
                  str    accountID  - The account ID

               Returns:
                  str    options    - A string containing the correctly
                                      formatted parallel job options.
            """
            # Job name
            text = self.optionID + " " + self.nameOption + " " + jobName + "\n"
            # Number of parallel tasks
            if (envOption != "") and (envOption is not None):
                # Test if we have an equals, if not add a space
                if (envOption.rfind("=") or envOption.rfind(":")) == -1: envOption = envOption + " "
                text = text + self.optionID + " " + self.parallelTasksOption + " " + \
                       envOption + str(pUnits) + "\n"
            else:
                text = text + self.optionID + " " + self.parallelTasksOption + " " + str(pUnits) + "\n"
            # Job run time
            text = text + self.optionID + " " + self.parallelTimeOption + runtime + "\n"
            # Account for charging
            if (accountID != "") and (accountID is not None):
                text = text + self.optionID + " " + self.accountOption + " " + accountID + "\n"
            # Queue name 
            if (queueName != "") and (queueName is not None):
                    text = text + self.optionID + " " + self.queueOption + " " + queueName + "\n"
            # Any other parallel options
            if (self.parallelOptions != "") and (self.parallelOptions is not None):
                    text = text + self.optionID + " " + self.parallelOptions + "\n"
            text = text + "\n"
            return text

    def getSerialOptionLines(self, jobName, queueName, runtime, accountID):
            """Generate the serial batch submission option lines so they can be
               writen to a job script
            
               Arguments:
                  str  jobName    - The name of the job
                  str  queueName  - The name of the queue to use
                  str  runtime    - The job runtime (hh:mm:ss)
                  str  accountID  - The account ID

               Returns:
                  str  options    - A string containing the correctly
                                    formatted serial job options.
            """
            if (self.nameOption != "") and (self.nameOption is not None) \
               and (jobName != "") and (jobName is not None):
                text = self.optionID + " " + self.nameOption + " " + jobName + "\n"
            if (self.serialTimeOption != "") and (self.serialTimeOption is not None) \
               and (runtime != "") and (runtime is not None):
                text = text + self.optionID + " " + self.serialTimeOption + runtime + "\n"
            if (accountID != "") and (accountID is not None):
                text = text + self.optionID + " " + self.accountOption + " " + accountID + "\n"
            if (queueName != "") and (queueName is not None):
                    text = text + self.optionID + " " + self.queueOption + " " + queueName + "\n"
            if (self.serialOptions != "") and (self.serialOptions is not None):
                    text = text + self.optionID + " " + self.serialOptions + "\n"
            text = text + "\n"
            return text

    def summaryString(self):
            """Return a string summarising the resource.

               Return:
                  str  output  - The string summarising the batch system
            """
            return "| {0:<10} |".format(self.name)
