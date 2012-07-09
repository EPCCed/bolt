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
        self.__threads = 1
        self.__runLine = None
        self.__pBatchOptions = None
        self.__batchOptions = None
        self.__scriptPreamble = None
        self.__scriptPostamble = None
        self.__jobCommand = None
        self.__accountID = None

    #======================================================================
    # Properties getters and setters
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
             str tasks   The number of parallel tasks per node
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
    def setThreads(self, threads):
        """Set the number of shared-memory threads per parallel tasks.
        Checks that an integer number of threads per task are requested
        and exits with an error if not.

        Arguments:
           int threads  The number of threads per parallel task.
        """
        # Check we have an integer number of tasks
        if re.search("^[0-9]+$", str(threads)) is not None:
            self.__threads = int(threads)
        else:
            # Something elsethrow an error
           error.handleError("Non-numeric number of threads per task specified ({0}).\n".format(threads))
    @property
    def runLine(self):
        """str The command used to launch the application. For example,
                  'mpiexec'"""
        return self.__runLine
    @property
    def pBatchOptions(self):
        """str Any parallel batch options needed to run the job."""
        return self.__pBatchOptions

    def setParallelDistribution(self, resource, batch):
        """This method distributes the tasks optimally for the specified
           resource. If any errors are encountered then an error message
           is printed and the program stops.

           Tasks can either be ditributed using options to a parallel job
           launcher (e.g. mpiexec), by the options passed to the batch
           system, or by using both methods.

           Arguments:
              Resource resource   The resource to use for the task
                                  distribution
              Resource batch      The batch system to use for the task
                                  distribution
        """

        # Make sure the job run line is empty
        runLine = ""

        # First compute all the values we might need
        # Number of nodes needed
        nodesUsed = self.pTasks / self.pTasksPerNode
        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1
        # Number of cores used per die
        coresPerDieUsed = min(self.pTasksPerNode, resource.coresPerDie)
        if (self.pTasksPerNode % (resource.diesPerSocket*resource.socketsPerNode)) == 0:
            coresPerDieUsed = self.pTasksPerNode / (resource.socketsPerNode*resource.diesPerSocket)
        else:
            # If we cannot divide this up then we just need to ignore this option
            coresPerDieUsed = 0
        # Task stride - if we have enough spare cores use the preferred stride
        # Also depends if we have specified threads or not - if we have specified 
        # the number of threads then this should be the stride
        strideUsed = 1
        if (self.threads > 1):
            strideUsed = self.threads
            if "csh" in resource.shell:
                runLine = "setenv OMP_NUM_THREADS " + str(self.threads) + "\n"
            else:
                runLine = "export OMP_NUM_THREADS=" + str(self.threads) + "\n"
        elif coresPerDieUsed == 0:
            # This is if we need to ignore the tasks per die option
            if (resource.numCoresPerNode() / self.pTasksPerNode) > resource.preferredStride:
                strideUsed = min(self.pTasksPerNode, resource.preferredStride)
        elif (resource.coresPerDie / coresPerDieUsed) >= resource.preferredStride:
            strideUsed = min(coresPerDieUsed, resource.preferredStride)
            

        # Test to see if we have a parallel run command
        runCommand = resource.parallelJobLauncher
        useRunCommand = True
        if (runCommand == None) or (runCommand == ""):
            useRunCommand = False
            # No job launcher command, are we using batch options instead?
            if not resource.useBatchParallelOpts:
                error.handleError("No parallel run command or batch options to use.\n", 1)

        pBatchOptions = ""

        #-------------------------------------------------------------------------------------------
        # Settings for using parallel job launcher
        if useRunCommand:

            # Most basic is just the parallel command and number of tasks
            option = resource.parallelTaskOption
            if (option is None) or (option == ""):
                error.handleError("The job launcher parallel task option is not set.\n", 1)
            elif self.pTasks == 0:
                error.handleError("The number of parallel tasks has not been set.\n", 1)
            runline = "{0}{1} {2} {3}".format(runLine, resource.parallelJobLauncher, option, self.pTasks)

            # Can we control the nodes used?
            option = resource.nodesOption
            if ((option != "") and (option is not None)) and (self.pTasksPerNode > 0):
                runline = "{0} {1} {2}".format(runline, option, nodesUsed)

            # Can we control the number of tasks per node?
            option = resource.taskPerNodeOption
            if ((option != "") and (option is not None)) and (self.pTasksPerNode > 0):
                runline = "{0} {1} {2}".format(runline, option, self.pTasksPerNode)

            # Can we control the number of tasks per die?
            option = resource.taskPerDieOption
            if ((option != "") and (option is not None)) and (self.pTasksPerNode > 1) and (coresPerDieUsed > 0):
                runline = "{0} {1} {2}".format(runline, option, coresPerDieUsed)
                
            # Can we control the stride
            option = resource.taskStrideOption
            if (option is not None) and (option != ""):
                runline = "{0} {1} {2}".format(runline, option, strideUsed) 
            
            self.__runLine = runline


        #-------------------------------------------------------------------------------------------
        # Settings for using parallel batch options
        # Most basic is just the parallel option and number of tasks/nodes. All jobs use this.
        option = batch.parallelOption
        if (option == None) or (option == ""):
            error.handleError("The batch parallel task option is not set.\n", 1)
        elif self.pTasks == 0:
            error.handleError("The number of parallel tasks has not been set.\n", 1)
        pUnits = self.pTasks
        # How are parallel resources allocated on this resource?
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
        # Set the option
        pBatchOptions = "{0} {1}{2}\n".format(batch.optionID, option, pUnits)

        # Additional options if we need them
        if resource.useBatchParallelOpts:
            # Can we control the number of tasks per node?
            option = batch.taskPerNodeOption
            if (option != "") and (option is not None) and (self.pTasksPerNode > 0):
                pBatchOptions = "{0}{1} {2}{3}\n".format(pBatchOptions, batch.optionID, option, self.pTasksPerNode)

            # Can we control the number of tasks per die?
            option = batch.taskPerDieOption
            if not ((option == "") or (option is None)) and (self.pTasksPerNode > 1) and (coresPerDieUsed > 0):
                pBatchOptions = "{0}{1} {2}{3}".format(pBatchOptions, batch.optionID, option, coresPerDieUsed)
                
            # Can we control the stride
            option = batch.taskStrideOption
            if (option is not None) and (option != ""):
                pBatchOptions = "{0}{1} {2}{3}".format(pBatchOptions, batch.optionID, option, strideUsed) 


        self.__pBatchOptions = pBatchOptions

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
             str command  The executable to use
        """
        self.__jobCommand = command
    @property
    def accountID(self):
        """str The account ID to use for the job."""
        return self.__accountID
    def setAccountID(self, account):
        """Set the account ID for the job.

           Arguments:
             str account  The account ID
        """
        self.__accountID = account

    #======================================================================
    # Verification methods check the consistency of the job
    def checkTasks(self, resource):
        """Check that the tasks requested are consistent with the selected
           resource. If errors are found then an error is printed and the
           program exits.

           Arguments:
             Resource  resource The selected resource to use for the
                                   consistency check
        """

        # Check parallel jobs are supported on this resource
        if not resource.parallelJobs:
            error.handleError("Resource {0} does not support parallel jobs.".format(resource.name))

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

        # Check that we support hybrid jobs if it has been requested
        if (self.threads > 1) and (self.pTasks > 1) and (not resource.hybridJobs):
            error.handleError("Resource {0} does not support hybrid distributed-/shared-memory jobs please only use 1 threads per task.".format(resource.name))

        # Check that the number of shared-memory threads requested 
        # is consistent
        # Do we have enough cores on a node
        coresPerNodeRequired = self.pTasksPerNode * self.threads
        if coresPerNodeRequired > resource.numCoresPerNode():
            error.handleError("Number of cores per node required ({0}) is greater than number available for resource {1} ({2}). Reduce number of threads per task or tasks per node".format(coresPerNodeRequired, resource.name, resource.numCoresPerNode()))
     

        # Check the total number of tasks
        # Number of nodes needed for this job
        nodesUsed = self.pTasks / self.pTasksPerNode
        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1
        pUnits = nodesUsed * resource.numCoresPerNode()
        if pUnits > resource.maxTasks:
            error.handleError("Resources required ({0} cores) is greater than number available for resource {1} ({2}).".format(pUnits, resource.name, resource.maxTasks))
        if pUnits < resource.minTasks:
            error.handleError("Resources required ({0} cores) is less than minimum required for resource {1} ({2}).".format(pUnits, resource.name, resource.minTasks))

    def checkTime(self, resource):
        """Check that the time requested is consistent with the selected
           resource. If an error is found then a message is printed and
           the program exits.

           Arguments:
             Resource  resource The selected resource for the
                                   time-consistency check
        """

        # Number of nodes needed for this job
        nodesUsed = self.pTasks / self.pTasksPerNode
        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1

        # Check of we have requested a consistent job length
        if self.wallTime > float(resource.maxJobTimeByNodes(nodesUsed)):
           error.handleError("Requested walltime ({0} hours) longer than maximum allowed on resource {1} for this number of nodes ({2} hours).".format(self.wallTime, resource.name, resource.maxJobTimeByNodes(nodesUsed)))

    #======================================================================
    # Writing methods write out the job
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

        # Get the parallel batch options
        scriptFile.write(self.pBatchOptions)
            
        # Get the batch options
        text = batch.getOptionLines(True, self.name, self.queueName, \
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
        scriptFile.write("# Run the parallel program\n")
        if self.runLine is None:
            scriptFile.write(self.jobCommand + "\n")
        else:
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
        text = batch.getOptionLines(False, self.name, self.queueName, \
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
        
