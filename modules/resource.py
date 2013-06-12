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
A python class to represent a compute resource

This class is part of the bolt job submission script generation tool.
The properties of the class are read from a configuration file that uses
the [ConfigParser] module.

Note: then no checking for reasonable values is currently performed.
"""
__author__ = "A. R. Turner, EPCC"

import sys

class Resource(object):
    """This class represents an compute resource. Resources are currently
       defined using configuration file via the [ConfigParser] module"""
    def __init__(self):
        """The default constructor - setup an empty resource object. Use
           the readConfig method to set the properties."""
        self.__name = None
        self.__arch = None
        self.__shell = None
        self.__batch = None
        self.__nodes = 0
        self.__accountRequired = False
        self.__defaultAccount = None

        self.__socketsPerNode = 0
        self.__diesPerSocket = 0
        self.__coresPerDie = 0
        self.__nodeExclusive = False
        self.__threadsPerCore = 0
        self.__accelerator = False

        self.__parallelJobs = False
        self.__hybridJobs = False
        self.__minTasks = 0
        self.__maxTasks = 0
        self.__maxJobTime = None
        self.__parallelTimeFormat = None
        self.__preferredStride = 0
        self.__parallelBatchUnit = None
        self.__parallelTaskOption = None
        self.__nodesOption = None
        self.__taskPerNodeOption = None
        self.__taskPerDieOption = None
        self.__taskStrideOption = None
        self.__parallelQueue = None
        self.__useBatchParallelOpts = False

        self.__distribJobLauncher = None
        self.__distribJobOptions = None
        self.__distribScriptPreamble = None
        self.__distribExecJobOptions = None
        self.__distribScriptPostamble = None

        self.__sharedJobLauncher = None
        self.__sharedJobOptions = None
        self.__sharedScriptPreamble = None
        self.__sharedExecJobOptions = None
        self.__sharedScriptPostamble = None

        self.__hybridJobLauncher = None
        self.__hybridJobOptions = None
        self.__hybridScriptPreamble = None
        self.__hybridExecJobOptions = None
        self.__hybridScriptPostamble = None

        self.__serialJobs = False
        self.__maxSerialJobTime = 0
        self.__serialTimeFormat = None
        self.__serialQueue = None
        self.__serialScriptPreamble = None
        self.__serialScriptPostamble = None

    # Properties - getters and setters
    # System info
    @property
    def name(self):
        """The name of the resource"""
        return self.__name
    @property
    def arch(self):
        """A short description of the system architecture"""
        return self.__arch
    @property
    def shell(self):
        """The string used to define the shell at the top of batch scripts"""
        return self.__shell
    @property
    def batch(self):
        """The name of the batch system to use by default for the resource.
        Must be defined in a corresponding batch configuration file."""
        return self.__batch
    @property
    def nodes(self):
        """The maximum number of compute nodes in the resource"""
        return self.__nodes
    @property
    def accountRequired(self):
        """Is an account ID required to run a job on the resource?"""
        return self.__accountRequired
    @property
    def defaultAccount(self):
        """The default account ID to use if none is specified. 'group' 
        indicates that it should be taken from the current *nix group"""
        return self.__defaultAccount
        
    # Node info
    @property
    def socketsPerNode(self):
        """The number of CPU sockets per compute node"""
        return self.__socketsPerNode
    @property
    def diesPerSocket(self):
        """The numebr of dies (or NUMA regions) per socket on a compute node"""
        return self.__diesPerSocket
    @property
    def coresPerDie(self):
        """The number of cores per dies (or NUMA region) on a compute node"""
        return self.__coresPerDie
    @property
    def threadsPerCore(self):
        """The number of threads per core(SMT/hyperthreading) on a compute node"""
        return self.__threadsPerCore
    @property
    def nodeExclusive(self):
        """Do jobs have exclusive access to a compute node?"""
        return self.__nodeExclusive
    @property
    def accelerator(self):
        """The type of accelerator (if any) on a compute node"""
        return self.__accelerator

    # Parallel job settings
    @property
    def parallelJobs(self):
        """Are parallel jobs allowed on the resource?"""
        return self.__parallelJobs
    @property
    def hybridJobs(self):
        """Are hybrid ditributed-/shared-memory jobs allowed on the resource?"""
        return self.__hybridJobs
    @property
    def maxTasks(self):
        """The maximum number of parallel tasks in a job"""
        return self.__maxTasks
    @property
    def minTasks(self):
        """The minimum number of parallel tasks in a job"""
        return self.__minTasks
    @property
    def maxJobTime(self):
        """The maximum job time permitted for parallel jobs"""
        return self.__maxJobTime
    def maxJobTimeByNodes(self, nodes):
        """The maximum job time (in hours) permitted for the specified number of nodes"""
        # Test if we have just the number of hours or not
        if not ":" in self.__maxJobTime: return int(self.__maxJobTime)
        # Split up the string to extract regions
        maxtime = 0
        timebynodes = self.__maxJobTime.split(",")   
        # Loop over specifications
        for specify in timebynodes:
                items = specify.split(":")
                r = items[0]
                mt = items[1]
                range = r.split("-")
                # If the upper range is empty use max cores
                if range[1] == "": range[1] = str(self.__maxTasks)
                # Set the max walltime string if we are in the range
                if (nodes >= int(range[0])) and (nodes <= int(range[1])): maxtime = int(mt)
        # Return the correct number of integer hours
        return maxtime


    @property
    def parallelTimeFormat(self):
        """The format for the parallel time unit. Valid values are: 'hms', 'hours', 'seconds'"""
        return self.__parallelTimeFormat
    @property
    def preferredStride(self):
        """When underpopulating nodes, the preffered stride between tasks.
        This is only relevent if the parallel job launcher can control
        task placement at this level (e.g. Cray aprun)"""
        return self.__preferredStride
    @property
    def parallelBatchUnit(self):
        """The unit to use when requesting batch queue slots. Currently
        either 'tasks' or 'nodes'"""
        return self.__parallelBatchUnit
    @property
    def distribJobLauncher(self):
        """The parallel job launcher command (e.g. 'mpiexec')"""
        return self.__distribJobLauncher
    @property
    def sharedJobLauncher(self):
        """The parallel job launcher command (e.g. 'mpiexec')"""
        return self.__sharedJobLauncher
    @property
    def hybridJobLauncher(self):
        """The parallel job launcher command (e.g. 'mpiexec')"""
        return self.__hybridJobLauncher
    @property
    def parallelTaskOption(self):
        """Command-line option to job launcher command that sets the
        number of parallel tasks"""
        return self.__parallelTaskOption
    @property
    def nodesOption(self):
        """str  - Command-line option to job launcher command that sets the
        number of nodes."""
        return self.__nodesOption
    @property
    def taskPerNodeOption(self):
        """Command-line option to job launcher command that sets the
        number of parallel tasks per node. If not set it indicates that the
        launcher cannot control this"""
        return self.__taskPerNodeOption
    @property
    def taskPerDieOption(self):
        """Command-line option to job launcher command that sets the
        number of parallel tasks per die. If not set it indicates that the
        launcher cannot control this"""
        return self.__taskPerDieOption
    @property
    def taskStrideOption(self):
        """Command-line option to job launcher command that sets the
        stride between parallel tasks. If not set it indicates that the
        launcher cannot control this"""
        return self.__taskStrideOption
    @property
    def parallelQueue(self):
        """The name of the parallel queue on the resource. If not set then
        no queue will be specified in the submission script."""
        return self.__parallelQueue
    @property
    def useBatchParallelOpts(self):
        """Choose whether to use the batch system options to distribute the
        parallel tasks. Usually used when the system has no parallel job
        launcher command."""
        return self.__useBatchParallelOpts
    @property
    def distribJobOptions(self):
        """Any additional job options needed for parallel jobs"""
        return self.__distribJobOptions
    @property
    def sharedJobOptions(self):
        """Any additional job options needed for parallel jobs"""
        return self.__sharedJobOptions
    @property
    def hybridJobOptions(self):
        """Any additional job options needed for parallel jobs"""
        return self.__hybridJobOptions
    @property
    def distribScriptPreamble(self):
        """Commands to be run in the script before the parallel executable
           is launched"""
        return self.__distribScriptPreamble
    @property
    def sharedScriptPreamble(self):
        """Commands to be run in the script before the parallel executable
            is launched"""
        return self.__sharedScriptPreamble
    @property
    def hybridScriptPreamble(self):
        """Commands to be run in the script before the parallel executable
           is launched"""
        return self.__hybridScriptPreamble
    @property
    def distribExecJobOptions(self):
        """Any additional job options before the exectubale needed for distrib-memory jobs"""
        return self.__distribExecJobOptions
    @property
    def sharedExecJobOptions(self):
        """Any additional job options before the exectubale needed for shared-memory jobs"""
        return self.__sharedExecJobOptions
    @property
    def hybridExecJobOptions(self):
        """Any additional job options before the exectubale needed for hybrid jobs"""
        return self.__hybridExecJobOptions
    @property
    def distribScriptPostamble(self):
        """Commands to be run in the script after the parallel executable
           is finished"""
        return self.__distribScriptPostamble
    @property
    def sharedScriptPostamble(self):
        """Commands to be run in the script after the parallel executable                              
           is finished"""
        return self.__sharedScriptPostamble
    @property
    def hybridScriptPostamble(self):
        """Commands to be run in the script after the parallel executable                          
            is finished"""
        return self.__hybridScriptPostamble

    # Serial job settings
    @property
    def serialJobs(self):
        """Are parallel jobs allowed on the resource?"""
        return self.__serialJobs
    @property
    def maxSerialJobTime(self):
        """The maximum job time (in hours) permitted for parallel jobs"""
        return self.__maxSerialJobTime
    @property
    def serialTimeFormat(self):
        """The format for the serial time unit. Valid values are: 'hms', 'hours', 'seconds'"""
        return self.__serialTimeFormat
    @property
    def serialQueue(self):
        """The name of the parallel queue on the resource. If not set then
        no queue will be specified in the submission script."""
        return self.__serialQueue
    @property
    def serialJobOptions(self):
        """Any additional job options needed for serial jobs"""
        return self.__serialJobOptions
    @property
    def serialScriptPreamble(self):
        """Commands to be run in the script before the serial executable
           is launched"""
        return self.__serialScriptPreamble
    @property
    def serialScriptPostamble(self):
        """Commands to be run in the script after the serial executable
           is finished"""
        return self.__serialScriptPostamble

    # Methods
    def readConfig(self, fileName):
        """This method reads the machine configuration from a file. using the 
        [ParseConfig] module.

        Arguments:
           str  fileName  - The file to read the configuration from.
        """
        import ConfigParser

        # Set up the config for this object
        resourceConfig = ConfigParser.SafeConfigParser()
        resourceConfig.read(fileName)

        # Get the system information options
        self.__name = resourceConfig.get("system info", "system name")
        self.__arch = resourceConfig.get("system info", "system description")
        self.__shell = resourceConfig.get("system info", "job script shell")
        self.__batch = resourceConfig.get("system info", "batch system")
        self.__nodes = resourceConfig.getint("system info", "total nodes")
        self.__accountRequired = resourceConfig.getboolean("system info", "account code required")
        self.__defaultAccount = resourceConfig.get("system info", "default account code")

        # Get the node information options
        self.__socketsPerNode = resourceConfig.getint("node info", "sockets per node")
        self.__diesPerSocket = resourceConfig.getint("node info", "dies per socket")
        self.__coresPerDie = resourceConfig.getint("node info", "cores per die")
        self.__threadsPerCore = resourceConfig.getint("node info", "threads per core")
        self.__nodeExclusive = resourceConfig.getboolean("node info", "exclusive node access")
        self.__accelerator = resourceConfig.get("node info", "accelerator type")

        # Get the general parallel jobs options
        self.__parallelJobs = resourceConfig.getboolean("general parallel jobs", "parallel jobs")
        self.__hybridJobs = resourceConfig.getboolean("general parallel jobs", "hybrid jobs")
        self.__maxTasks = resourceConfig.getint("general parallel jobs", "maximum tasks")
        self.__minTasks = resourceConfig.getint("general parallel jobs", "minimum tasks")
        self.__maxJobTime = resourceConfig.get("general parallel jobs", "maximum job duration")
        self.__parallelTimeFormat = resourceConfig.get("general parallel jobs", "parallel time format")
        self.__preferredStride = resourceConfig.getint("general parallel jobs", "preferred task stride")
        self.__parallelBatchUnit = resourceConfig.get("general parallel jobs", "parallel reservation unit")
        self.__parallelTaskOption = resourceConfig.get("general parallel jobs", "number of tasks option")
        self.__nodesOption = resourceConfig.get("general parallel jobs", "number of nodes option")
        self.__taskPerNodeOption = resourceConfig.get("general parallel jobs", "tasks per node option")
        self.__taskPerDieOption = resourceConfig.get("general parallel jobs", "tasks per die option")
        self.__taskStrideOption = resourceConfig.get("general parallel jobs", "tasks stride option")
        self.__parallelQueue = resourceConfig.get("general parallel jobs", "queue name")
        self.__useBatchParallelOpts = resourceConfig.getboolean("general parallel jobs", "use batch parallel options")


        # Get the distributed memory jobs options
        self.__distribJobLauncher = resourceConfig.get("distributed-mem jobs", "parallel job launcher")
        self.__distribJobOptions = resourceConfig.get("distributed-mem jobs", "additional job options")
        self.__distribScriptPreamble = resourceConfig.get("distributed-mem jobs", "script preamble commands")
        self.__distribExecJobOptions = resourceConfig.get("distributed-mem jobs", "executable job options")
        self.__distribScriptPostamble = resourceConfig.get("distributed-mem jobs", "script postamble commands")


        # Get the shared memory jobs options                                                    
        self.__sharedJobLauncher = resourceConfig.get("shared-mem jobs", "parallel job launcher")
        self.__sharedJobOptions = resourceConfig.get("shared-mem jobs", "additional job options")
        self.__sharedScriptPreamble = resourceConfig.get("shared-mem jobs", "script preamble commands")
        self.__sharedExecJobOptions = resourceConfig.get("shared-mem jobs", "executable job options")
        self.__sharedScriptPostamble = resourceConfig.get("shared-mem jobs", "script postamble commands")

        # Get the hybrid memory jobs options                                                        
        self.__hybridJobLauncher = resourceConfig.get("hybrid jobs", "parallel job launcher")
        self.__hybridJobOptions = resourceConfig.get("hybrid jobs", "additional job options")
        self.__hybridScriptPreamble = resourceConfig.get("hybrid jobs", "script preamble commands")
        self.__hybridExecJobOptions = resourceConfig.get("hybrid jobs", "executable job options")
        self.__hybridScriptPostamble = resourceConfig.get("hybrid jobs", "script postamble commands")

        # Get the serial jobs options
        self.__serialJobs = resourceConfig.getboolean("serial jobs", "serial jobs")
        self.__maxSerialJobTime = resourceConfig.getfloat("serial jobs", "maximum job duration")
        self.__serialTimeFormat = resourceConfig.get("serial jobs", "serial time format")
        self.__serialQueue = resourceConfig.get("serial jobs", "queue name")
        self.__serialJobOptions = resourceConfig.get("serial jobs", "additional job options")
        self.__serialScriptPreamble = resourceConfig.get("serial jobs", "script preamble commands")
        self.__serialScriptPostamble = resourceConfig.get("serial jobs", "script postamble commands")

    def numCores(self):
        '''Return the total number of compute cores on this resource.

           Returns:
              int  cores   - Total number of compute cores
        '''
        cores = self.nodes * self.socketsPerNode * self.diesPerSocket * self.coresPerDie
        return cores

    def numCoresPerNode(self):
        '''Return the number of compute cores per node on this resource.
       
           Returns:
              int  cores   - Total number of compute cores per node
        '''
        cores = self.socketsPerNode * self.diesPerSocket * self.coresPerDie
        return cores

    def numLogicalCoresPerNode(self):
        '''Return the number of compute cores per node on this resource, including hyperthreading
           Returns:
              int  cores   - Total number of logical compute cores per node 
        '''
        cores = self.socketsPerNode * self.diesPerSocket * self.coresPerDie * self.threadsPerCore
        return cores


    def summaryString(self):
        """Print a summary of this reource.

           Returns:
              str  output  - a string summarising the compute resource
        """
        output =  '| {0:<10} | {1:<30} | {2:5d} nodes | {3:6d} cores |'.format(self.name, \
                                                                   self.arch, \
                                                                   self.nodes, \
                                                                   self.numCores())
        return output

    def __str__(self):
        """Print a string representing this resource.

           Returns:
              str  output  - a string that describes this compute resource.
        """
        output = "\n" + self.name + ":\n\n"
        output = output + self.arch + "\n"

        return output



