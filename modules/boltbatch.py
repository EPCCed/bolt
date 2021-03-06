#----------------------------------------------------------------------
# Copyright 2012-2020 EPCC, The University of Edinburgh
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

This class is part of the bolt boltjob submission script generation 
tool. The properties of the class are read from a configuration 
file that uses the [ConfigParser] module.
"""
__author__ = "A. R. Turner, EPCC"

class BoltBatch(object):
    def __init__(self):
        """The default constructor - setup an empty batch system"""
        self.__name = ""
        self.__submitCommand = None

        self.__optionID = None
        self.__nameOption = None
        self.__accountOption = None
        self.__queueOption = None
        self.__qosOption = None

        self.__parallelOption = None
        self.__nodesOption = None
        self.__taskPerNodeOption = None
        self.__taskPerDieOption = None
        self.__taskStrideOption = None
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
        """The option used to specify the queue name. For example '-q' for the
        PBS batch system"""
        return self.__queueOption
    @property
    def qosOption(self):
        """The option used to specify the QoS name. For example '--qos=' for the
        Slurm batch system"""
        return self.__qosOption

    # Parallel boltjob options
    @property
    def parallelOption(self):
        """The option used to specify the number of parallel units to use."""
        if (len(self.__parallelOption) == 0): return ""
        if (self.__parallelOption.rfind("=") or self.__parallelOption.rfind(":")) == -1:
           return self.__parallelOption + " "
        else:
           return self.__parallelOption
    @property
    def taskPerNodeOption(self):
        """The option used to specify the number of parallel tasks
        per node.."""
        if (len(self.__taskPerNodeOption) == 0): return ""
        if (self.__taskPerNodeOption.rfind("=") or self.__taskPerNodeOption.rfind(":")) == -1:
           return self.__taskPerNodeOption + " "
        else:
           return self.__taskPerNodeOption
    @property
    def taskPerDieOption(self):
        """The option used to specify the number of parallel tasks
        per die.."""
        if (len(self.__taskPerDieOption) == 0): return ""
        if (self.__taskPerDieOption.rfind("=") or self.__taskPerDieOption.rfind(":")) == -1:
           return self.__taskPerDieOption + " "
        else:
           return self.__taskPerDieOption
    @property
    def taskStrideOption(self):
        """The option used to specify the stride for parallel task."""
        if (len(self.__taskStrideOption) == 0): return ""
        if (self.__taskStrideOption.rfind("=") or self.__taskStrideOption.rfind(":")) == -1:
           return self.__taskStrideOption + " "
        else:
           return self.__taskStrideOption
    @property
    def parallelTimeOption(self):
        """The option used to specify the job time. For example '-l walltime='
        for the PBS batch system"""
        if (len(self.__parallelTimeOption) == 0): return ""
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
        if (len(self.__serialTimeOption) == 0): return ""
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
        self.__qosOption = batchConfig.get("basic options", "qos option")

        # Get the parallel options
        self.__parallelOption = batchConfig.get("parallel options", "parallel option")
        self.__taskPerNodeOption = batchConfig.get("parallel options", "task per node option")
        self.__taskPerDieOption = batchConfig.get("parallel options", "task per die option")
        self.__taskStrideOption = batchConfig.get("parallel options", "task stride option")
        self.__parallelTimeOption = batchConfig.get("parallel options", "time option")
        self.__parallelOptions = batchConfig.get("parallel options", "additional options")
        self.__parallelScriptPreamble = batchConfig.get("parallel options", "script preamble")
        self.__parallelScriptPostamble = batchConfig.get("parallel options", "script postamble")

        # Get the serial options
        self.__serialTimeOption = batchConfig.get("serial options", "time option")
        self.__serialOptions = batchConfig.get("serial options", "additional options")
        self.__serialScriptPreamble = batchConfig.get("serial options", "script preamble")
        self.__serialScriptPostamble = batchConfig.get("serial options", "script postamble")

    def getOptionLines(self, isParallel, jobName, queueName, qosName, runtime, accountID):
        """Generate the batch submission option lines so they can be
           written to a job script
        
           Arguments:
              boolean  isParallel - Is this a parallel job?
              str      jobName    - The name of the job
              str      queueName  - The name of the queue to use
              str      qosName    - The name of the QoS to use
              str      runtime    - The job runtime (hh:mm:ss)
              str      accountID  - The account ID

           Returns:
              str  options    - A string containing the correctly
                                formatted serial job options.
        """

        # Common options
        if (self.nameOption != "") and (self.nameOption is not None) \
           and (jobName != "") and (jobName is not None):
            text = "{0} {1}{2}\n".format(self.optionID, self.nameOption, jobName)
        if (accountID != "") and (accountID is not None):
            text = "{0}{1} {2}{3}\n".format(text, self.optionID, self.accountOption, accountID)
        if (queueName != "") and (queueName is not None):
            text = "{0}{1} {2}{3}\n".format(text, self.optionID, self.queueOption, queueName)
        if (qosName != "") and (qosName is not None):
            text = "{0}{1} {2}{3}\n".format(text, self.optionID, self.qosOption, qosName)

        if isParallel:
            # Parallel options
            if (self.parallelTimeOption != "") and (self.parallelTimeOption is not None) \
               and (runtime != "") and (runtime is not None):
                    text = "{0}{1} {2}{3}\n".format(text, self.optionID, self.parallelTimeOption, runtime)
            if (self.parallelOptions != "") and (self.parallelOptions is not None):
                # Split out the parallel options
                options = self.parallelOptions.split(";")
                for option in options:
                    text = "{0}{1} {2}\n".format(test, self.optionID, option)
        else:
            # Serial options
            if (self.serialTimeOption != "") and (self.serialTimeOption is not None) \
               and (runtime != "") and (runtime is not None):
                    text = "{0}{1} {2}{3}\n".format(text, self.optionID, self.serialTimeOption, runtime)
            if (self.serialOptions != "") and (self.serialOptions is not None):
                # Split out the parallel options
                options = self.serialOptions.split(";")
                for option in options:
                    text = "{0}{1} {2}\n".format(test, self.optionID, option)

        text = text + "\n"
        return text

    def summaryString(self):
        """Return a string summarising the batch system.

           Return:
              str  output  - The string summarising the batch system
        """
        return "| {0:<10} |".format(self.name)
