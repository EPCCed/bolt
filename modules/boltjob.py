#----------------------------------------------------------------------
# Copyright 2012, 2014 EPCC, The University of Edinburgh
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
Python class to represent a boltbatch job

This class is used in the simple submission tool to represent the
job. It contains methods for distributing parallel tasks optimally
and running consistency checks.
"""
__author__ = "Andrew Turner, EPCC"

import re
import math
import bolterror
import sys

class BoltJob(object):
    """This class represents a batch job."""
    def __init__(self):
        """The default constructor. Setup an empty job object."""
        self.__name = None
        self.__wallTime = None
        self.__queueName = None
        self.__isParallel = False
        self.__isDistrib = False
        self.__isShared = False
        self.__isHybrid = False
        self.__pTasks = 0
        self.__pTasksPerNode = 0
        self.__pTasksPerDie = 0
        self.__threads = 1
        self.__runLine = None
        self.__pBatchOptions = None
        self.__batchOptions = None
        self.__parallelScriptPreamble = None
        self.__parallelScriptPostamble = None
        self.__jobOptions = None
        self.__execJobOptions = None
        self.__parallelJobLauncher = None 
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
           correct format then print an bolterror and exit.

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
            # Something elsethrow an bolterror
           bolterror.handleError("Time specified ({0}) is not in format hh:mm:ss.\n".format(time), 1)
    def getWallTime(self, resource):
        """Get the maximum runtime of the job in the correct format for the
           specified resource, either 'hms', 'hours', or 'seconds'. The time
           is stored internally as hours.

           Arguments:
             BoltResource  resource The resource to use for the time format
                                    option.

           Returns:
             str           time     The time in the correct format for the 
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
            bolterror.handleError("Unknown time format specified ({0}) for resource {1}.\n".format(timeFormat, resource.name), 1)
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
    def isDistrib(self):
        """boolean True = distributed memory job."""
        return self.__isDistrib
    def setIsDistrib(self, di):
        """Set whether or not this is a distributed memory job.
                  Arguments:
                  boolean  di True = distributed-memory job.
        """
        self.__isDistrib = di
    @property
    def isShared(self):
        """boolean True = shared memory job."""
        return self.__isShared
    def setIsShared(self, sh):
        """Set whether or not this is a shared memory job.
                  Arguments:                
                  boolean  sh True = shared-memory job.
        """
        self.__isShared = sh
    @property
    def isHybrid(self):
        """boolean True = shareded memory job."""
        return self.__isHybrid
    def setIsHybrid(self, hy):
        """Set whether or not this is a hybrid job.                                   
           Arguments:
                  boolean  hy True = hybrid job.
        """
        self.__isHybrid = hy
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
            # Something elsethrow an bolterror
           bolterror.handleError("Non-numeric number of tasks specified ({0}).\n".format(tasks), 1)
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
            # Something elsethrow an bolterror
           bolterror.handleError("Non-numeric number of tasks per node specified ({0}).\n".format(tasks))
    @property
    def pTasksPerDie(self):
         """int The number of parallel tasks per die to use. 
                   A die is equivalent to a NUMA region on a processor."""
         return self.__pTasksPerDie
    @property
    def threads(self):
        """int Set the number of threads per task."""
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
            # Something elsethrow an bolterror
           bolterror.handleError("Non-numeric number of threads per task specified ({0}).\n".format(threads))
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
              Batch    batch      The batch system to use for the task
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
#            sys.stdout.write("We have %i threads \n" % self.threads )
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
        runCommand = self.parallelJobLauncher
        useRunCommand = True
        if (runCommand == None) or (runCommand == ""):
            useRunCommand = False
            # To keep the exporting of OMP-threads
            self.__runLine = runLine
            # No job launcher command, are we using boltbatch options instead?
            if not resource.useBatchParallelOpts:
                bolterror.handleError("No parallel run command or batch options to use.\n", 1)

        pBatchOptions = ""

        #-------------------------------------------------------------------------------------------
        # Settings for using parallel job launcher
        if useRunCommand:

          if batch.name == 'TorqueStokes':
            option = resource.parallelTaskOption
            if (option is None) or (option == ""):
                bolterror.handleError("The job launcher parallel task option is not set.\n", 1)
            elif self.pTasks == 0:
                bolterror.handleError("The number of parallel tasks has not been set.\n", 1)
            runline = "{0}{1} {2} {3}".format(runLine, self.parallelJobLauncher, option, self.pTasks)
            self.__runLine = runline
          else:
            # Most basic is just the parallel command and number of tasks
            option = resource.parallelTaskOption
            if (option is None) or (option == ""):
                bolterror.handleError("The job launcher parallel task option is not set.\n", 1)
            elif self.pTasks == 0:
                bolterror.handleError("The number of parallel tasks has not been set.\n", 1)
            runline = "{0}{1} {2} {3}".format(runLine, self.parallelJobLauncher, option, self.pTasks)
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
        # Settings for using parallel boltbatch options
        # Most basic is just the parallel option and number of tasks/nodes. All jobs use this.
        option = batch.parallelOption
        if (option == None) or (option == ""):
            bolterror.handleError("The batch parallel task option is not set.\n", 1)
        elif self.pTasks == 0:
            bolterror.handleError("The number of parallel tasks has not been set.\n", 1)
        pUnits = self.pTasks
        # How are parallel resources allocated on this boltresource?
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
            bolterror.handleError("Unit of resource: {0} is not defined (use 'tasks' or 'nodes') in resource configuration file for resource: {1}.\n".format(resource.parallelBatchUnit, resource.name))
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
    def parallelJobLauncher(self):
       """ str   """
       return self.__parallelJobLauncher
    def setParallelJobLauncher(self,p):
        """" Set according to type of job, ie. distributed, shared or hybrid.
             Arguments: p """
        self.__parallelJobLauncher = p
    @property
    def jobOptions(self):
        """ str """
        return self.__jobOptions
    def setJobOptions(self,p):
        """ Set according to type of job, ie. distributed, shared or hybrid.
             Arguments: p """
        self.__jobOptions = p
    @property
    def parallelScriptPreamble(self):
        """str Any script commands that need to be run before the
                  application is launched"""
        return self.__parallelScriptPreamble
    def setParallelScriptPreamble(self,p):
        """ Set according to job type, i.e. for distributed, shared or hybrid job.
             Arguments:
             p """
        self.__parallelScriptPreamble = p
    @property
    def execJobOptions(self):
        """ str """
        return self.__execJobOptions
    def setExecJobOptions(self,p):
        """" Set according to type of job, ie. distributed, shared or hybrid.                       
             Arguments: p """
        self.__execJobOptions = p
    @property
    def parallelScriptPostamble(self):
        """str Any script commands that need to be run after the
                  application is complete"""
        return self.__parallelScriptPostamble
    def setParallelScriptPostamble(self,p):
        """ Set according to job type, i.e. for distributed, shared or hybrid job.            
             Arguments:                                                                       
             p """
        self.__parallelScriptPostamble = p 
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
    def checkTasks(self, resource, code):
        """Check that the tasks requested are consistent with the selected
           resource. If errors are found then an error is printed and the
           program exits.

           Arguments:
             Resource  resource The selected resource to use for the
                                consistency check
             Code      code     The code specified (None if no code
                                specified)
        """

        # Check parallel jobs are supported on this boltresource
        if not resource.parallelJobs:
            bolterror.handleError("Resource {0} does not support parallel jobs.".format(resource.name))

        # Check we do not have more tasks per node than tasks
        # EYB
        if self.pTasksPerNode > self.pTasks:
            tpn = min(self.pTasks, resource.numLogicalCoresPerNode())
            bolterror.printWarning("Number of specified parallel tasks per node ({0}) is greater than the number of specified parallel tasks ({1}). Reducing tasks per node to {2}.".format(self.pTasksPerNode, self.pTasks, tpn))
            self.setTasksPerNode(tpn)

        # Check the number of tasks per node
        # EYB
        if self.pTasksPerNode > resource.numLogicalCoresPerNode():
            tpn = resource.numLogicalCoresPerNode()
            bolterror.printWarning("Number of specified parallel tasks per node ({0}) is greater than number available for resource {1} ({2}). Reducing tasks per node to {3}.".format(self.pTasksPerNode, resource.name, resource.numLogicalCoresPerNode(), tpn))
            self.setTasksPerNode(resource.numLogicalCoresPerNode())
        

        # Check that we support hybrid jobs if it has been requested
        if (self.threads > 1) and (self.pTasks > 1) and (not resource.hybridJobs):
            bolterror.handleError("Resource {0} does not support hybrid distributed-/shared-memory jobs please only use 1 threads per task.".format(resource.name))

        # Check that the number of shared-memory threads requested 
        # is consistent
        # Do we have enough cores on a node
        coresPerNodeRequired = self.pTasksPerNode * self.threads
        if coresPerNodeRequired > resource.numLogicalCoresPerNode():
            bolterror.handleError("Number of cores per node required ({0}) is greater than number available for resource {1} ({2}). Reduce number of threads per task or tasks per node".format(coresPerNodeRequired, resource.name, resource.numCoresPerNode()))
     

        # Check the total number of tasks
        # Number of nodes needed for this job
        nodesUsed = self.pTasks / self.pTasksPerNode
        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1
        pUnits = nodesUsed * resource.numCoresPerNode()
        if pUnits > resource.maxTasks:
            bolterror.handleError("Resources required ({0} cores) is greater than number available for resource {1} ({2}).".format(pUnits, resource.name, resource.maxTasks))
        if pUnits < resource.minTasks:
            bolterror.handleError("Resources required ({0} cores) is less than minimum required for resource {1} ({2}).".format(pUnits, resource.name, resource.minTasks))

        # Check against tasks for boltcode
        if code is not None:
            # Test the maximum tasks
            if (code.maxTasks > 0) and (pUnits > code.maxTasks):
                bolterror.handleError("Resources required ({0} cores) is greater than number allowed for code {1} ({2}).".format(pUnits, code.name, code.maxTasks))
            # Test the mimimum tasks
            if (code.minTasks > 0) and (pUnits < code.minTasks):
                bolterror.handleError("Resources required ({0} cores) is less than minimum required for code {1} ({2}).".format(pUnits, code.name, code.minTasks))

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
        if self.isParallel:
            sys.stdout.write(" ")
        else:
            sys.stdout.write(" ")
            if self.wallTime > float(resource.maxSerialJobTime):bolterror.handleError("Requested walltime ({0} hours) longer than maximum allowed on resource {1} for this number of nodes ({2} hours).".format(self.wallTime, resource.name, resource.maxSerialJobTime))

        if (self.pTasks % self.pTasksPerNode) > 0:
            nodesUsed += 1
            
            # Check of we have requested a consistent job length
        if self.wallTime > float(resource.maxJobTimeByNodes(nodesUsed)):
            bolterror.handleError("Requested walltime ({0} hours) longer than maximum allowed on resource {1} for this number of nodes ({2} hours).".format(self.wallTime, resource.name, resource.maxJobTimeByNodes(nodesUsed)))
                
    #======================================================================
    # Writing methods write out the job
    def writeParallelJob(self, batch, resource, code, scriptFile):
        """This function writes out a parallel job script for the specified
           resource. If errors are encountered then an error message is
           printed and the program exits.

           Arguments:
              Batch    batch     Batch system to use
              Resource resource  Resource to use
              Code     code      Code to use
              str      scriptFileThe name of the script file to write
        """

        # Useful variables
        batchPre = batch.optionID

        # Does the specified boltresource allow parallel jobs?
        if not resource.parallelJobs:
            bolterror.handleError("Resource: {0} does not support parallel jobs.".format(resource.name))

        # The shell line
        text = resource.shell + "\n"
        scriptFile.write(text)
       

        # Information lines
        scriptFile.write("#\n# Parallel script produced by bolt\n")
        scriptFile.write("#        Resource: {0} ({1})\n".format(resource.name, resource.arch))
        scriptFile.write("#    Batch system: {0}\n#\n".format(batch.name))
        scriptFile.write("# bolt is written by EPCC (http://www.epcc.ed.ac.uk)\n#\n")
        # Get the parallel boltbatch options
        scriptFile.write(self.pBatchOptions)
            
        # Get the boltbatch options
        text = batch.getOptionLines(True, self.name, self.queueName, \
                                    self.getWallTime(resource), self.accountID)
        scriptFile.write(text)

        # Get any further options from boltresource configuration
        scriptFile.write(self.jobOptions+"\n")

        # Script preambles: boltresource -> boltbatch -> boltcode -> job
        if self.parallelScriptPreamble != ("" or None):
            scriptFile.write(self.parallelScriptPreamble + "\n")
        if batch.parallelScriptPreamble != ("" or None):
            scriptFile.write(batch.parallelScriptPreamble + "\n")
        if code is not None:
            if code.preamble is not None: scriptFile.write(code.preamble + "\n")
#        if self.parallelScriptPreamble != ("" or None):
#            scriptFile.write(self.parallelScriptPreamble + "\n")
        # Parallel run line
        scriptFile.write("# Run the parallel program\n")
        if self.runLine is None:
            scriptFile.write(self.jobCommand + "\n")
        else:
            scriptFile.write(self.runLine + " " + self.jobCommand + "\n")
        # Script postambles: job -> boltcode -> boltbatch -> boltresource
        if self.parallelScriptPostamble != ("" or None):
            scriptFile.write(self.parallelScriptPostamble + "\n")
        if code is not None:
            if code.postamble is not None: scriptFile.write(code.postamble + "\n")
        if batch.parallelScriptPostamble != ("" or None):
            scriptFile.write(batch.parallelScriptPostamble + "\n")
        if self.parallelScriptPostamble != ("" or None):
            scriptFile.write(self.parallelScriptPostamble + "\n")
        
    def writeSerialJob(self, batch, resource, code, scriptFile):
        """This function writes out a serial job script for the specified
           resource. If errors are encountered then an error message is
           printed and the program exits.

           Arguments:
              Batch    batch      Batch system to use
              Resource resource   Resource to use
              Code     code       Code to use
              str      scriptFile The name of the script file to write
        """

        # Useful variables
        batchPre = batch.optionID

        # Does the specified boltresource allow serial jobs?
        if not resource.serialJobs:
            bolterror.handleError("Resource: {0} does not support serial jobs.".format(resource.name))

        # The shell line
        text = resource.shell + "\n"
        scriptFile.write(text)

        scriptFile.write("#\n# Serial script produced by bolt\n")
        scriptFile.write("#        Resource: {0} ({1})\n".format(resource.name, resource.arch))
        scriptFile.write("#    Batch system: {0}\n#\n".format(batch.name))
        scriptFile.write("# bolt is written by EPCC (http://www.epcc.ed.ac.uk)\n#\n")

        # Get the boltbatch options
        text = batch.getOptionLines(False, self.name, self.queueName, \
                                    self.getWallTime(resource), self.accountID)
        scriptFile.write(text)

        # Get any further options from boltresource configuration
        scriptFile.write(resource.serialJobOptions)

        # Script preambles: boltresource -> boltbatch -> boltcode -> job
        if resource.serialScriptPreamble != ("" or None):
            scriptFile.write(resource.serialScriptPreamble + "\n")
        if batch.parallelScriptPreamble != ("" or None):
            scriptFile.write(batch.parallelScriptPreamble + "\n")
        if code is not None:
            if code.preamble is not None: scriptFile.write(code.postamble + "\n")
        if self.parallelScriptPreamble != ("" or None):
            scriptFile.write(self.parallelScriptPreamble + "\n")

        # Serial run line
        scriptFile.write("# Run the serial program\n")
        scriptFile.write(self.jobCommand + "\n")

        # Script postambles: job -> boltcode -> boltbatch -> boltresource
        if self.parallelScriptPostamble != ("" or None):
            scriptFile.write(self.paralleScriptPostamble + "\n")
        if code is not None:
            if code.postamble is not None: scriptFile.write(code.postamble + "\n")
        if batch.parallelScriptPostamble != ("" or None):
            scriptFile.write(batch.parallelScriptPostamble + "\n")
        if resource.serialScriptPostamble != ("" or None):
            scriptFile.write(resource.serialScriptPostamble + "\n")
        
