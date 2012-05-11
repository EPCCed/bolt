""" 
A python class to represent a compute resource

This class is part of the bolt job submission script generation tool.
The properties of the class are read from a configuration file that uses
the [ConfigParser] module.

Note: then no checking for reasonable values is currently performed.
"""
__author__ = "A. R. Turner, EPCC"
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
        self.__accelerator = False

        self.__parallelJobs = False
        self.__minTasks = 0
        self.__maxTasks = 0
        self.__maxJobTime = 0
        self.__parallelTimeFormat = None
        self.__preferredStride = 0
        self.__parallelBatchUnit = None
        self.__parallelJobLauncher = None
        self.__parallelTaskOption = None
        self.__nodesOption = None
        self.__taskPerNodeOption = None
        self.__taskPerDieOption = None
        self.__taskStrideOption = None
        self.__parallelQueue = None
        self.__parallelEnvOption = None
        self.__jobOption = None
        self.__parallelScriptPreamble = None
        self.__parallelScriptPostamble = None

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
    def maxTasks(self):
        """The maximum number of parallel tasks in a job"""
        return self.__maxTasks
    @property
    def minTasks(self):
        """The minimum number of parallel tasks in a job"""
        return self.__minTasks
    @property
    def maxJobTime(self):
        """The maximum job time (in hours) permitted for parallel jobs"""
        return self.__maxJobTime
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
    def parallelJobLauncher(self):
        """The parallel job launcher command (e.g. 'mpiexec')"""
        return self.__parallelJobLauncher
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
    def parallelEnvOption(self):
        """The string to use when setting the number of parallel tasks. If
        this ends with '=' then no space will be placed between this and 
        the number of parallel units"""
        return self.__parallelEnvOption
    @property
    def jobOptions(self):
        """Any additional job options needed for parallel jobs"""
        return self.__jobOptions
    @property
    def parallelScriptPreamble(self):
        """Commands to be run in the script before the parallel executable
           is launched"""
        return self.__parallelScriptPreamble
    @property
    def parallelScriptPostamble(self):
        """Commands to be run in the script after the parallel executable
           is finished"""
        return self.__parallelScriptPostamble

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
        self.__nodeExclusive = resourceConfig.getboolean("node info", "exclusive node access")
        self.__accelerator = resourceConfig.get("node info", "accelerator type")

        # Get the parallel jobs options
        self.__parallelJobs = resourceConfig.getboolean("parallel jobs", "parallel jobs")
        self.__maxTasks = resourceConfig.getint("parallel jobs", "maximum tasks")
        self.__minTasks = resourceConfig.getint("parallel jobs", "minimum tasks")
        self.__maxJobTime = resourceConfig.getint("parallel jobs", "maximum job duration")
        self.__parallelTimeFormat = resourceConfig.get("parallel jobs", "parallel time format")
        self.__preferredStride = resourceConfig.getint("parallel jobs", "preferred task stride")
        self.__parallelBatchUnit = resourceConfig.get("parallel jobs", "parallel reservation unit")
        self.__parallelJobLauncher = resourceConfig.get("parallel jobs", "parallel job launcher")
        self.__parallelTaskOption = resourceConfig.get("parallel jobs", "number of tasks option")
        self.__nodesOption = resourceConfig.get("parallel jobs", "number of nodes option")
        self.__taskPerNodeOption = resourceConfig.get("parallel jobs", "tasks per node option")
        self.__taskPerDieOption = resourceConfig.get("parallel jobs", "tasks per die option")
        self.__taskStrideOption = resourceConfig.get("parallel jobs", "tasks stride option")
        self.__parallelQueue = resourceConfig.get("parallel jobs", "queue name")
        self.__parallelEnvOption = resourceConfig.get("parallel jobs", "parallel allocation option")
        self.__jobOptions = resourceConfig.get("parallel jobs", "additional job options")
        self.__parallelScriptPreamble = resourceConfig.get("parallel jobs", "script preamble commands")
        self.__parallelScriptPostamble = resourceConfig.get("parallel jobs", "script postamble commands")

        # Get the serial jobs options
        self.__serialJobs = resourceConfig.getboolean("serial jobs", "serial jobs")
        self.__maxSerialJobTime = resourceConfig.getint("serial jobs", "maximum job duration")
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


