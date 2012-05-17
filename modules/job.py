"""
Python class to represent a batch job

This class is used in the simple submission tool to represent the
job. It contains methods for distributing parallel tasks optimally
and running consistency checks.
"""
__author__ = "Andrew Turner, EPCC"

import re
import math
import error

class Job(object):
    """This class represents a batch job."""
    def __init__(self):
        """The default constructor. Setup an empty job object."""
        self.__name = None
        self.__wallTime = None
        self.__queueName = None
        self.__isParallel = False
        self.__pTasks = 0
        self.__pTasksPerNode = 0
        self.__pTasksPerDie = 0
        self.__threads = 0
        self.__runLine = None
        self.__batchOptions = None
        self.__scriptPreamble = None
        self.__scriptPostamble = None
        self.__jobCommand = None
        self.__accountID = None

    #======================================================================
    # Propertiesgetters and setters
    @property
    def name(self):
        """str The job name"""
        return self.__name
    def setName(self, name):
        """Set the job name

           Arguments:
             str nameThe name
        """
        self.__name = name
    @property
    def wallTime(self):
        """float The maximum runtime for the job in hours."""
        return self.__wallTime
    def setWallTime(self, time):
        """Set the maximum runtime. Checks that the walltime is specified
           either as hh:mm:ss or integer number of hours. If not the
           correct format then print an error and exit.

           Arguments:
             str timeThe maximum walltime (hh:mm:ss or hours)
        """
        # Check we have a compatible time format
        if re.search("^[0-9]+:[0-9]+:[0-9]+$", str(time)) is not None:
            # hh:mm:ss, convert to hours
            hms = time.split(":")
            self.__wallTime = float(hms[0]) + float(hms[1])/60 + \
                              float(hms[2])/3600
        elif re.search("^[0-9]+\.[0-9]+$", str(time)) is not None:
            # Just hours
            self.__wallTime = float(time)
        elif re.search("^[0-9]+$", str(time)) is not None:
            # Just hours
            self.__wallTime = float(time)
        else:
            # Something elsethrow an error
           error.handleError("Time specified ({0}) is not in format hh:mm:ss.\n".format(time), 1)
    def getWallTime(self, resource):
        """Get the maximum runtime of the job in the correct format for the
           specified resource, either 'hms', 'hours', or 'seconds'. The time
           is stored internally as hours.

           Arguments:
             Resource  resource The resource to use for the time format
                                   option.

           Returns:
             str       time     The time in the correct format for the 
                                   specified resource.
        """
        timeFormat = ""
        time = ""
        if self.isParallel:
            timeFormat = resource.parallelTimeFormat
        else:
            timeFormat = resource.serialTimeFormat

        if timeFormat == 'hms':
            t = float(self.__wallTime)
            h = int(t)
            secs = (t - float(h))*3600
            m = int(secs/60)
            s = int(secs - m*60)
            time = "{0}:{1}:{2}".format(h,m,s)
        elif timeFormat == 'hours':
            time = str(int(math.ceil(float(self.__wallTime))))
        elif timeFormat == 'seconds':
            time = str(int(float(self.__wallTime)*3600))
        else:
            error.handleError("Unknown time format specified ({0}) for resource {1}.\n".format(timeFormat, resource.name), 1)
        return time
    @property
    def queueName(self):
            """str The queue name to use for the job."""
            return self.__queueName
    def setQueue(self, q):
            """Set the queue name.

               Arguments:
                 str qThe queue name to use
            """
            self.__queueName = q
    @property
    def isParallel(self):
        """boolean True = parallel job; false = serial job."""
        return self.__isParallel
    def setIsParallel(self, p):
        """Set whether or not this is a parallel job.

           Arguments:
              boolean  p True = parallel job; False = serial job
        """
        self.__isParallel = p
    @property
    def pTasks(self):
        """int The number of parallel tasks for the job."""
        return self.__pTasks
    def setTasks(self, tasks):
        """Set the number of parallel tasks. Checks that an integer
           number of tasks are requested and exits with an error if
           not.

           Arguments:
             str tasksThe number of parallel tasks
        """
        # Check we have an integer number of tasks
        if re.search("^[0-9]+$", str(tasks)) is not None:
            self.__pTasks = int(tasks)
        else:
            # Something elsethrow an error
           error.handleError("Non-numeric number of tasks specified ({0}).\n".format(tasks), 1)
    @property
    def pTasksPerNode(self):
        """int The number of parallel tasks per node to use."""
        return self.__pTasksPerNode
    def setTasksPerNode(self, tasks):
        """Set the number of parallel tasks per node. Checks that an integer
           number of tasks per node are requested and exits with an error if
           not.
         
           Arguments:
             str tasksThe number of parallel tasks per node
        """
        # Check we have an integer number of tasks
        if re.search("^[0-9]+$", str(tasks)) is not None:
            self.__pTasksPerNode = int(tasks)
        else:
            # Something elsethrow an error
           error.handleError("Non-numeric number of tasks per node specified ({0}).\n".format(tasks))
    @property
    def pTasksPerDie(self):
         """int The number of parallel tasks per die to use. 
                   A die is equivalent to a NUMA region on a processor."""
         return self.__pTasksPerDie
    @property
    def threads(self):
        """int Set the number of threads per task. Currently
                  unused as shared-memory jobs are not supported."""
        return self.__threads
    @property
    def runLine(self):
        """str The command used to launch the application. For example,
                  'mpiexec'"""
        return self.__runLine
    def setParallelRunLine(self, resource):
        """This method distributes the tasks optimally for the specified
           resource. If any errors are encountered then an error message
           is printed and the program stops.

           Arguments:
              Resource resourceThe resource to use for the task
                                  distribution
        """

        # Most basic is just the parallel command and number of tasks
        option = resource.parallelTaskOption
        if option == (None or ""):
            error.handleError("The parallel task option is not set.\n", 1)
        elif self.pTasks == 0:
            error.handleError("The number of parallel tasks has not been set.\n", 1)
        runline = "{0} {1} {2}".format(resource.parallelJobLauncher, option, self.pTasks)

        # Can we control the nodes used?
        option = resource.nodesOption
        if (option != "") and (option is not None) and (self.pTasksPerNode > 0):
            # Number of nodes needed for this job
            nodesUsed = self.pTasks / self.pTasksPerNode
            if (self.pTasks % self.pTasksPerNode) > 0:
                nodesUsed += 1
            runline = "{0} {1} {2}".format(runline, option, nodesUsed)

        # Can we control the number of tasks per node?
        option = resource.taskPerNodeOption
        if (option != "") and (option is not None) and (self.pTasksPerNode > 0):
            runline = "{0} {1} {2}".format(runline, option, self.pTasksPerNode)

        # Can we control the number of tasks per die?
        option = resource.taskPerDieOption
        coresPerDie = 1
        if (option != "") and (option is not None) and (self.pTasksPerNode > 1):
            if (self.pTasksPerNode % resource.diesPerSocket) == 0:
                coresPerDie = self.pTasksPerNode / (resource.socketsPerNode*resource.diesPerSocket)
                runline = "{0} {1} {2}".format(runline, option, coresPerDie)
                
        # Can we control the stride
        option = resource.taskStrideOption
        if option != (None or ""):
            if coresPerDie == 1:
                runline = "{0} {1} {2}".format(runline, option, 1)
            elif (resource.coresPerDie / coresPerDie) >= resource.preferredStride:
                runline = "{0} {1} {2}".format(runline, option, resource.preferredStride)
            else:
                runline = "{0} {1} {2}".format(runline, option, 1)
            
        self.__runLine = runline

    @property
    def scriptPreamble(self):
        """str Any script commands that need to be run before the
                  application is launched"""
        return self.__scriptPreamble
    @property
    def scriptPostamble(self):
        """str Any script commands that need to be run after the
                  application is complete"""
        return self.__scriptPostamble
    @property
    def jobCommand(self):
        """str The name of the executable (or possibly script) to run"""
        return self.__jobCommand
    def setJobCommand(self, command):
        """Set the name of the executable to use.

           Arguments:
             str commandThe executable to use
        """
        self.__jobCommand = command
    @property
    def accountID(self):
        """str The account ID to use for the job."""
        return self.__accountID
    def setAccountID(self, account):
        """Set the account ID for the job.

           Arguments:
             str accountThe account ID
        """
        self.__accountID = account

    #======================================================================
    # Verification methodscheck the consistency of the job
    def checkTasks(self, resource):
        """Check that the tasks requested are consistent with the selected
           resource. If errors are found then an error is printed and the
           program exits.

           Arguments:
             Resource  resource The selected resource to use for the
                                   consistency check
        """

        # Check we do not have more tasks per node than tasks
        if self.pTasksPerNode > self.pTasks:
            tpn = min(self.pTasks, resource.numCoresPerNode())
            error.printWarning("Number of specified parallel tasks per node ({0}) is greater than the number of specified parallel tasks ({1}). Reducing tasks per node to {2}.".format(self.pTasksPerNode, self.pTasks, tpn))
            self.setTasksPerNode(tpn)

        # Check the number of tasks per node
        if self.pTasksPerNode > resource.numCoresPerNode():
            tpn = resource.numCoresPerNode()
            error.printWarning("Number of specified parallel tasks per node ({0}) is greater than number available for resource {1} ({2}). Reducing tasks per node to {3}.".format(self.pTasksPerNode, resource.name, resource.numCoresPerNode(), tpn))
            self.setTasksPerNode(resource.numCoresPerNode())

        # Check the total number of tasks
        # Number of nodes needed for this job
        nodesUsed = self.pTasks / self.pTasksPerNode
        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1
        pUnits = nodesUsed * resource.numCoresPerNode()
        if pUnits > resource.maxTasks:
            error.handleError("Specified parallel tasks required ({0}) is greater than number available for resource {1} ({2}).".format(pUnits, resource.name, resource.maxTasks))
        if pUnits < resource.minTasks:
            error.handleError("Specified parallel tasks required ({0}) is less than minimum required for resource {1} ({2}).".format(pUnits, resource.name, resource.minTasks))

    def checkTime(self, resource):
        """Check that the time requested is consistent with the selected
           resource. If an error is found then a message is printed and
           the program exits.

           Arguments:
             Resource  resource The selected resource for the
                                   time-consistency check
        """

        # Check of we have requested too long
        if self.wallTime > float(resource.maxJobTime):
           error.handleError("Requested walltime ({0}) longer than maximum allowed on resource {1} ({2} hours).".format(self.wallTime, resource.name, resource.maxJobTime))

    #======================================================================
    # Writing methodswrite out the job
    def writeParallelJob(self, batch, resource, scriptFile):
        """This function writes out a parallel job script for the specified
           resource. If errors are encountered then an error message is
           printed and the program exits.

           Arguments:
              Batch    batch     Batch system to use
              Resource resource  Resource to use
              str      scriptFileThe name of the script file to write
        """

        # Useful variables
        batchPre = batch.optionID

        # Does the specified resource allow parallel jobs?
        if not resource.parallelJobs:
            error.handleError("Resource: {0} does not support parallel jobs.".format(resource.name))

        # The shell line
        text = resource.shell + "\n"
        scriptFile.write(text)

        # Information lines
        scriptFile.write("#\n# Parallel script produced by bolt\n")
        scriptFile.write("#        Resource: {0} ({1})\n".format(resource.name, resource.arch))
        scriptFile.write("#    Batch system: {0}\n#\n".format(batch.name))
        scriptFile.write("# bolt is written by EPCC (http://www.epcc.ed.ac.uk)\n#\n")

        # Compute number of pUnits (either tasks or nodes)
        pUnits = 0
        # Number of nodes needed for this job
        nodesUsed = self.pTasks / self.pTasksPerNode
        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1
        # Set the units
        if resource.parallelBatchUnit == "tasks":
            # Job allocated by tasks
            # Do we have exclusive node access or not
            if resource.nodeExclusive:
                # Yes, we need number of tasks corresponding to full nodes
                pUnits = nodesUsed * resource.numCoresPerNode()
            else:
                # No, we just need number of parallel tasks
                pUnits = self.pTasks
        elif resource.parallelBatchUnit == "nodes":
            # Job allocated by nodes
            pUnits = nodesUsed
        else:
            error.handleError("Unit of resource: {0} is not defined (use 'tasks' or 'nodes') in resource configuration file for resource: {1}.\n".format(resource.parallelBatchUnit, resource.name))
            
        # Get the batch options
        text = batch.getParallelOptionLines(self.name, self.queueName, \
                                            resource.parallelEnvOption, pUnits, \
                                            self.getWallTime(resource), self.accountID)
        scriptFile.write(text)

        # Get any further options from resource configuration
        scriptFile.write(resource.jobOptions)

        # Script preambles: resource -> batch -> job
        if resource.parallelScriptPreamble != ("" or None):
            scriptFile.write(resource.parallelScriptPreamble + "\n")
        if batch.parallelScriptPreamble != ("" or None):
            scriptFile.write(batch.parallelScriptPreamble + "\n")
        if self.scriptPreamble != ("" or None):
            scriptFile.write(self.scriptPreamble + "\n")

        # Parallel run line
        if self.runLine is None:
            error.handleError("Run line has not yet been set.\n")
        else:
            scriptFile.write("# Run the parallel program\n")
            scriptFile.write(self.runLine + " " + self.jobCommand + "\n")

        # Script postambles: job -> batch -> resource
        if self.scriptPostamble != ("" or None):
            scriptFile.write(self.scriptPostamble + "\n")
        if batch.parallelScriptPostamble != ("" or None):
            scriptFile.write(batch.parallelScriptPostamble + "\n")
        if resource.parallelScriptPostamble != ("" or None):
            scriptFile.write(resource.parallelScriptPostamble + "\n")
        
    def writeSerialJob(self, batch, resource, scriptFile):
        """This function writes out a serial job script for the specified
           resource. If errors are encountered then an error message is
           printed and the program exits.

           Arguments:
              Batch    batch     Batch system to use
              Resource resource  Resource to use
              str      scriptFileThe name of the script file to write
        """

        # Useful variables
        batchPre = batch.optionID

        # Does the specified resource allow serial jobs?
        if not resource.serialJobs:
            error.handleError("Resource: {0} does not support serial jobs.".format(resource.name))

        # The shell line
        text = resource.shell + "\n"
        scriptFile.write(text)

        scriptFile.write("#\n# Serial script produced by bolt\n")
        scriptFile.write("#        Resource: {0} ({1})\n".format(resource.name, resource.arch))
        scriptFile.write("#    Batch system: {0}\n#\n".format(batch.name))
        scriptFile.write("# bolt is written by EPCC (http://www.epcc.ed.ac.uk)\n#\n")

        # Get the batch options
        text = batch.getSerialOptionLines(self.name, self.queueName, \
                                          self.getWallTime(resource), self.accountID)
        scriptFile.write(text)

        # Get any further options from resource configuration
        scriptFile.write(resource.jobOptions)

        # Script preambles: resource -> batch -> job
        if resource.parallelScriptPreamble != ("" or None):
            scriptFile.write(resource.parallelScriptPreamble + "\n")
        if batch.parallelScriptPreamble != ("" or None):
            scriptFile.write(batch.parallelScriptPreamble + "\n")
        if self.scriptPreamble != ("" or None):
            scriptFile.write(self.scriptPreamble + "\n")

        # Serial run line
        scriptFile.write("# Run the serial program\n")
        scriptFile.write(self.jobCommand + "\n")

        # Script postambles: job -> batch -> resource
        if self.scriptPostamble != ("" or None):
            scriptFile.write(self.scriptPostamble + "\n")
        if batch.parallelScriptPostamble != ("" or None):
            scriptFile.write(batch.parallelScriptPostamble + "\n")
        if resource.parallelScriptPostamble != ("" or None):
            scriptFile.write(resource.parallelScriptPostamble + "\n")
        
