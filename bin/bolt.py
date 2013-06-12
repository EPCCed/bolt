#!/usr/bin/python
#
#===============================================================
# bolt - Simple Job Submission Tool
#
# Submit jobs to different compute resource batch systems using
# a common interface. Tries to optimally distribute parallel
# tasks across nodes.
#===============================================================
#
#===============================================================
# v0.5 - Added support for hybrid jobs and ability to define
#        simulation codes
# v0.4 - Added option to distribute tasks using batch system
# v0.3 - Added GPL
#===============================================================
#
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
#
"""Produce job submission scripts using a common interface.

This tool produces job submission scripts for a variety of compute
resources and batch systems. It attempts to partition the work in a
pseudo-optimal way and select sensible options. It will also include
compulsory options required on particular resources.

OPTIONS

-A,--account <account>   Specify the account to charge the job to. If
                         not specified then it is not included in the
                         output.
                         
-b,--batch <batch>       Specify the batch system to create job submission
                         script for. Default is specified by the resource
                         configuration. Use the '-l' option to list valid
                         values.

-c,--code <code>         Specify a simulation code to generate a batch
                         script for. Use the '-l' option to list valid 
                         values and details on the arguments that should
                         be provided.

-d,--threads <n>         The number of shared-memory threads per parallel
                         task. Default is 1.
                         
-h,--help                Show this help.

-i,--info                Display the program licence and warranty.

-j,--job-name            The job name. Defaults to the name of the 
                         specified executable.

-l,--list                List the resources and batch systems available.

-n,--tasks <n>           Number of parallel tasks. Defaults to 1. If
                         number of parallel tasks is 1 then the tool
                         will try to produce a serial job submission
                         script (unless the '-p' option is specified).

-N,--tasks-per-node <n>  Number of parallel tasks per node. Defaults to
                         the minimum of the number of tasks or the number
                         of cores per node for the specified resource.

-o,--output <filename>   The output filename to use. The default is
                         "a.bolt".

-p,--force-parallel      Force the tool to create a parallel job even if
                         the number of tasks is 1.

-q,--queue <queue>       Specify the queue to submit the job to. This 
                         will usually be set correctly by default.

-r,--resource <resource> Specify the resource to create a job submission
                         script for. Default is set by the install system.
                         Use the '-l' option to list valid values.

-s,--submit              Submit the created job submission script to the
             batch system. Default is not to submit job.
             
-t,--job-time <hh:mm:ss> Specify the wallclock limit for the job.
"""
__author__ = 'Andrew Turner, EPCC, The University of Edinburgh'
__version__ = '0.5'

from resource import Resource
from batch import Batch
from job import Job
from code import Code
import error
import sys
import os
import fnmatch
import getopt
import subprocess
import ConfigParser
import grp

def main(argv):

    #=======================================================
    # Print out the banner
    #=======================================================
    sys.stderr.write("===========================================================================\n")
    sys.stderr.write("bolt " + __version__ + "\n")
    sys.stderr.write("---------------------------------------------------------------------------\n")
    sys.stderr.write("Copyright 2012  EPCC, The University of Edinburgh \n")
    sys.stderr.write("This program comes with ABSOLUTELY NO WARRANTY; for details type `bolt -i'.\n")
    sys.stderr.write("This is free software, and you are welcome to redistribute it\n")
    sys.stderr.write("under certain conditions; type `bolt -i' for details.\n")
    sys.stderr.write("===========================================================================\n")

    #=======================================================
    # Global configuration section
    #=======================================================
    # Read the tool configuration file here
    #  - Location of other configuration files
    #  - Default resource
    rootDir = os.environ['BOLT_DIR']
    globalConfig = {}
    globalConfig = readGlobalConfig(rootDir + "/configuration/global.config")
    defaultResource = globalConfig['defaultResource']

    #=======================================================
    # Read the defined resources and batch systems
    #=======================================================
    # Get a list of all the defined batch system.
    batchConfigDir = rootDir + '/configuration/batch'
    batches = []
    nBatch = 0
    # We also need to create a dictionary of batch systems here
    batchDict = {}
    for file in os.listdir(batchConfigDir):
        if fnmatch.fnmatch(file, '*.batch'):
            nBatch += 1
            batch = Batch()
            batch.readConfig(batchConfigDir + '/' + file) 
            batches.append(batch)
            batchDict[batch.name] = nBatch - 1

#    sys.stdout.write("It is batch system: " + batch.name + "\n")    
    if nBatch == 0:
        error.handleError("No batch systems defined in {0}.\n".format(batchConfigDir))

    # Get a list of all the defined resources. If a user does not specify a 
    # resource then we will use resources[0] as the default
    resourceConfigDir = rootDir + '/configuration/resources'
    resources = []
    nResource = 0
    # We also need to create a dictionary of resources here
    resourceDict = {}
    for file in os.listdir(resourceConfigDir):
        if fnmatch.fnmatch(file, '*.resource'):
            nResource += 1
            resource = Resource()
            resource.readConfig(resourceConfigDir + '/' + file)
            resources.append(resource)
            resourceDict[resource.name] = nResource - 1
            #sys.stdout.write ("Resources: " + resources.values())
            # Check we have a description of the batch system
            name = resource.batch
            try:
                index = batchDict[name]
            except KeyError:
                error.handleError("Batch system not found: {0}. Known systems are {1}\n".format(name, batchDict.keys()))

    if nResource == 0:
        error.handleError("No resources defined in {0}.\n".format(resourceConfigDir))

        # Check that the default resource has been defined
    if defaultResource not in resourceDict:
        error.handleError("Default resource not found: {0}. Known resources are {1}\n".format(defaultResource, resourceDict.keys()))
        exit(1)
                
    #=======================================================
    # Read any code definitions
    #=======================================================
    codeConfigDir = rootDir + '/configuration/codes'
    codes = []
    nCode = 0
    # We also need to create a dictionary of resources here
    codeDict = {}
    for file in os.listdir(codeConfigDir):
        if fnmatch.fnmatch(file, '*.code'):
            nCode += 1
            code = Code()   
            code.readConfig(codeConfigDir + '/' + file)
            codes.append(code)
            codeDict[code.name] = nCode - 1

    #=======================================================
    # Create the job object
    #=======================================================
    job = Job()

    #=======================================================
    # Command line options
    #=======================================================
    # Read the command-line options
    try:
        opts, args = getopt.getopt(argv, "n:N:d:A:t:o:r:b:q:j:c:plshi", \
                      ["tasks=", "tasks-per-node=", "threads=", "account=", \
                      "job-time=", "output-file=", "resource=", "batch=", "queue=", \
                      "job-name=", "code=", "force-parallel", "list", "submit", \
                      "help", "info"])
    except getopt.GetoptError:
        error.handleError("Could not parse command line options\n")

    # Set the initial values
    taskPerNodeSpecified = False
    forceParallel = False
    submitJob = False
    outputFileName = None
    outputFile = None
    selectedResource = None
    selectedBatch = None
    selectedCode = None

    # Parse the command-line options
    for opt, arg in opts:
        if opt in ("-n", "--tasks"):
            job.setTasks(arg)
        if opt in ("-N", "--tasks-per-node"):
            job.setTasksPerNode(arg)
            taskPerNodeSpecified = True
        if opt in ("-d", "--threads"):
            job.setThreads(arg)
            # If we have more than one thread this is a parallel job
            if job.threads > 1: forceParallel = True
        if opt in ("-j", "--job-name"):
            job.setName(arg)
        if opt in ("-A", "--account"):
            job.setAccountID(arg)
        if opt in ("-t", "--job-time"):
            job.setWallTime(arg)
        if opt in ("-o", "--output-file"):
            outputFileName = arg
        if opt in ("-q", "--queue"):
            job.setQueue(arg)
        if opt in ("-p", "--force-parallel"):
            forceParallel = True
        if opt in ("-r", "--resource"):
            selectedResource = arg
            # Test if we know the specified resource
            if selectedResource not in resourceDict:
                error.handleError("Resource not found: {0}. Known resources are {1}\n".format(selectedResource, resourceDict.keys()))
        if opt in ("-c", "--code"):
            selectedCode = arg
            if nCode == 0:
                error.handleError("Code not found: {0}. No codes currently defined. Use 'bolt -h' to display usage information.\n".format(selectedCode))
            # Test if we know the specified code
            if selectedCode not in codeDict:
                error.handleError("Code not found: {0}. Known codes are {1}\n".format(selectedCode, codeDict.keys()))
        if opt in ("-s", "--submit"):
            submitJob = True
        if opt in ("-b", "--batch"):
            selectedBatch = arg
            # Test if we know the specified batch system
            if selectedBatch not in batchDict:
                error.handleError("Batch system not found: {0}. Known systems are {1}\n".format(selectedBatch, batchDict.keys()))
        if opt in ("-l", "--list"):
            listResources(resources, defaultResource)
            listBatch(batches, resources[resourceDict[defaultResource]].batch)
            listCodes(codes)
            exit(0)
        if opt in ("-h", "--help"):
            printHelp(rootDir)
            exit(0)
        if opt in ("-i", "--info"):
            printLicence(rootDir)
            exit(0)

    # Check that we have an executable name to use
    if selectedCode is None:
        if len(args) < 1:
            error.handleError("You must specify an executable name to use. Use 'bolt -h' to show correct usage.")
    else:
        if len(args) != codes[codeDict[selectedCode]].nargs:
            error.handleError("You have not specified the correct number of command line arguments for code {0} ({1}).".format(selectedCode, codes[codeDict[selectedCode]].nargs))

    # Is this a parallel job or not
    job.setIsParallel((job.pTasks > 1) or (forceParallel))

    #=======================================================
    # Set default job options
    #=======================================================
    # If output file name is specified then write to it - otherwise
    # use "a.bolt"
    if outputFileName is None: 
        error.printWarning("Using default output file name: a.bolt")
        outputFileName = "a.bolt"

    # Try to open the output file
    try:
        outputFile = open(outputFileName, "w")
    except IOError as (errno, strerror):
        error.handleError("Opening output file: {0}; {1}".format(outputFileName, strerror), errno)

    # If no resource or batch systems are specified then use the defaults
    if selectedResource is None: selectedResource = resources[resourceDict[defaultResource]].name
    if selectedBatch is None: selectedBatch = resources[resourceDict[selectedResource]].batch

    # For convenience, set the selected resource, batch system and code
    resource = resources[resourceDict[selectedResource]]
    batch = batches[batchDict[selectedBatch]]
    code = None
    if selectedCode is not None: code = codes[codeDict[selectedCode]]

    # Default job name is the name of the executable
    if job.name is None:
        if job.isParallel:
            error.printWarning("Setting job name to: bolt_par_job")
            job.setName("bolt_par_job")
        else:
            error.printWarning("Setting job name to: bolt_ser_job")
            job.setName("bolt_ser_job")

    # Default wall time is 5 minutes
    if job.wallTime is None: 
        error.printWarning("Using default job walltime of 5 mins")
        job.setWallTime("0:5:0")

    # Default number of tasks is 1
    if job.pTasks == 0:
        error.printWarning("Setting number of parallel tasks to 1")
        job.setTasks(1)

    # Default cores per node comes from the resource
    if job.pTasksPerNode == 0:
        if job.threads <= resource.numCoresPerNode():
            defaultCPN = resource.numCoresPerNode()
        else:
            defaultCPN = resource.numLogicalCoresPerNode()
        # We need to account for the number of threads if > 1
        if job.threads > resource.numLogicalCoresPerNode():
#            sys.stdout.write("numLogicalCoresPerNode in bolt.py :" +str(resource.numLogicalCoresPerNode())+"\n")
            error.handleError("Number of my threads requested ({0}) is greater than number of cores per node on resource {1} ({2}).".format(job.threads, resource.name, resource.numLogicalCoresPerNode()))
        if job.threads > 1: defaultCPN = defaultCPN / job.threads
        # Catch the case where there are less than a nodes-worth of tasks
        defaultCPN = min(job.pTasks * job.threads, defaultCPN)
        job.setTasksPerNode(defaultCPN)
        error.printWarning("Setting number of tasks per node to " + str(defaultCPN))


# <<<<<<< HEAD
        
# =======

# >>>>>>> dev-unittests
    if (job.accountID == "") or (job.accountID is None) and (resource.accountRequired):
        if resource.defaultAccount == "group":
            # Get account from *nix group
            grpinfo = grp.getgrgid(os.getgid())
            job.setAccountID(grpinfo[0])
            error.printWarning("Setting accounting code to " + grpinfo[0])
        elif (resource.defaultAccount != "") or (resource.defaultAccount is not None):
            job.setAccountID(resource.defaultAccount)
            error.printWarning("Setting accounting code to " + resource.defaultAccount)

    # Default queues if needed
    if job.isParallel:
        if (job.queueName == "") or (job.queueName is None):
            job.setQueue(resource.parallelQueue)
    else:
        if (job.queueName == "") or (job.queueName is None):
            job.setQueue(resource.serialQueue)

    # Is this a distributed-memory job or shared-memory or hybrid                               
    job.setIsDistrib((job.pTasks > 1) and (job.threads == 1))
    job.setIsShared((job.pTasks == 1) and (job.threads > 1))
    job.setIsHybrid((job.pTasks > 1) and (job.threads > 1))


    #=======================================================
    # Consistency checks
    #=======================================================
    # If we have selected the number of tasks per node we need to see if this
    # option is supported on the specified resource
    if taskPerNodeSpecified:
        if resource.useBatchParallelOpts:
            if (batch.taskPerNodeOption == "") or (batch.taskPerNodeOption is None):
                error.printWarning("Tasks per node specified ({0}) but option is not supported on resource {1}. {2} will be used.".format(job.pTasksPerNode, resource.name, min(job.pTasks, resource.numCoresPerNode())))
                job.setTasksPerNode(min(job.pTasks, resource.numCoresPerNode()))
        else:
            if ((resource.taskPerNodeOption == "") or (resource.taskPerNodeOption == None)) and \
                           ((resource.nodesOption == "") or (resource.nodesOption == None)):
                error.printWarning("Tasks per node specified ({0}) but option is not supported on resource {1}. {2} will be used.".format(job.pTasksPerNode, resource.name, min(job.pTasks, resource.numCoresPerNode())))

                job.setTasksPerNode(min(job.pTasks, resource.numCoresPerNode()))

    # Check that we have specified a sensible number of tasks for a parallel job
    if job.isParallel:
        job.checkTasks(resource, code)

    # Check that we have specified a sensible job time
    job.checkTime(resource)
    #sys.stdout.write("It is batch system: " + batch.name + "\n")

    # Check that we have an account (if required)
    if resource.accountRequired:
        if (job.accountID == "") or (job.accountID is None):
            error.handleError("Account ID not specified (-A option) but resource {0} requires an account ID to be specified.".format(resource.name))

    #=======================================================
    # Write out the job script
    #=======================================================

    # Is this a serial or parallel job
    if job.isParallel:
        sys.stdout.write("This is a PARALLEL job.\n")

        # For parallel jobs we need to compute the pseudo-optimal distribution of
        # tasks and set the parallel job launcher command
        # Write the parallel job script

        if job.isDistrib:
            sys.stdout.write("This is an MPI job. \n")

# Set the job command                                                                       
            if code is None:
            # No code specified, job command is the remaining arguments                             
                job.setJobCommand(resource.distribExecJobOptions+ " " +' '.join(args))
            else:
            # Print the message for the specified code                                              
                if code.message is not None: sys.stdout.write("Note:\n" + code.message + "\n\n")
                # Get the executable from the code description                                          
                # Are we running parallel or hybrid job                                                 
                if job.threads > 1:
                    if len(code.hybrid) == 0:
                        error.handleError("Shared-memory threads specified but not supported by code {0\
}.".format(code.name))
                    else:
                        job.setJobCommand(code.hybrid + " " + code.argFormat.format(*args))
                elif job.threads == 1:
                    if len(code.parallel) == 0:
                        error.handleError("Parallel job specified but not supported by code {0}.".format(code.name))
                    else:
                        job.setJobCommand(code.parallel +  " " + code.argFormat.format(*args))



            job.setParallelJobLauncher(resource.distribJobLauncher)
            job.setParallelScriptPreamble(resource.distribScriptPreamble)
            job.setParallelScriptPostamble(resource.distribScriptPostamble)
            job.setJobOptions(resource.distribJobOptions)            

        if job.isShared:
            sys.stdout.write("This is an OpenMP job.\n") 

    # Set the job command                                                                       
            if code is None:
                # No code specified, job command is the remaining arguments                             
                job.setJobCommand(resource.sharedExecJobOptions+ " " +' '.join(args))
            else:
                # Print the message for the specified code                                              
                if code.message is not None: sys.stdout.write("Note:\n" + code.message + "\n\n")
                # Get the executable from the code description                                          
                # Are we running parallel or hybrid job                                                 
                if job.threads > 1:
                    if len(code.hybrid) == 0:
                        error.handleError("Shared-memory threads specified but not supported by code {0}.".format(code.name))
                    else:
                        job.setJobCommand(code.hybrid + " " + code.argFormat.format(*args))
                elif job.threads == 1:
                    if len(code.parallel) == 0:
                        error.handleError("Parallel job specified but not supported by code {0}.".format(code.name))
                    else:
                        job.setJobCommand(code.parallel +  " " + code.argFormat.format(*args))



            job.setParallelJobLauncher(resource.sharedJobLauncher)
            job.setParallelScriptPreamble(resource.sharedScriptPreamble)
            job.setParallelScriptPostamble(resource.sharedScriptPostamble)
            job.setJobOptions(resource.sharedJobOptions)


        if job.isHybrid:
            sys.stdout.write("This is a hybrid job.\n")

# Set the job command                                                                       
            if code is None:
                # No code specified, job command is the remaining arguments                             
                job.setJobCommand(resource.hybridExecJobOptions+ " " +' '.join(args))
            else:
                # Print the message for the specified code                                              
                if code.message is not None: sys.stdout.write("Note:\n" + code.message + "\n\n")
                # Get the executable from the code description                                          
                # Are we running parallel or hybrid job                                                 
                if job.threads > 1:
                    if len(code.hybrid) == 0:
                        error.handleError("Shared-memory threads specified but not supported by code {0}.".format(code.name))
                    else:
                        job.setJobCommand(code.hybrid + " " + code.argFormat.format(*args))
                elif job.threads == 1:
                    if len(code.parallel) == 0:
                        error.handleError("Parallel job specified but not supported by code {0}.".format(code.name))
                    else:
                        job.setJobCommand(code.parallel +  " " + code.argFormat.format(*args))


            job.setParallelJobLauncher(resource.hybridJobLauncher)
            job.setParallelScriptPreamble(resource.hybridScriptPreamble)
            job.setParallelScriptPostamble(resource.hybridScriptPostamble)
            job.setJobOptions(resource.hybridJobOptions)

        job.setParallelDistribution(resource, batch)
        job.writeParallelJob(batch, resource, code, outputFile)


    else:
                
#Serial job
                sys.stdout.write("This is a SERIAL job.\n")
                if code is None:
                    # Job command is the remaining arguments
                    job.setJobCommand(' '.join(args))
                else:
                    # Print the message for the specified code
                    if code.message is not None: sys.stdout.write("Note:\n" + code.message + "\n\n")
                    if len(code.serial) == 0:
                        error.handleError("Serial job specified but not supported by code {0}.".format(code.name))
                    else:
                        job.setJobCommand(code.serial + " " + code.argFormat.format(*args))
                        
                # Write the serial job script
                job.writeSerialJob(batch, resource, code, outputFile)
                        
    # Close the file if we need to
    if outputFileName is not None: outputFile.close()
    
    #=======================================================
    # Submit the job if required
    #=======================================================
    if submitJob:
        sys.stderr.write("Submitting job...\n")
        subprocess.call([batch.submitCommand, outputFileName])

    # Finish nicely
    sys.stderr.write("\n")
    exit(0)

def readGlobalConfig(fileName):
    """Read the global configuration options from the specified file.

           Arguments:
              str fileName - Name of the config file
        """
    config = ConfigParser.SafeConfigParser()
    config.read(fileName)

    globalConfig = {}
    globalConfig['defaultResource'] = config.get("global options", "default resource")

    return globalConfig

def listResources(resources, defaultResource):
    """List the defined compute resources and indicate the default.

           Arguments:
              dict resources       - Dictionary of defined resources
              str  defaultResource - Name of the default resource
        """
    sys.stdout.write("\nDefined resources (* = default):\n")
    for resource in resources:
        summary = resource.summaryString()
        if resource.name == defaultResource:
            sys.stdout.write("* " + summary + " *\n")
        else:
            sys.stdout.write("  " + summary + "  \n")
    sys.stdout.write("\n")


def listBatch(batches, defaultBatch):
    """List the defined batch systems and indicate the default.

           Arguments:
              dict batches      - Dictionary of defined batch systems
              str  defaultBatch - Name of the default batch system
        """
    sys.stdout.write("\nDefined batch systems (* = default):\n")
    for batch in batches:
        summary = batch.summaryString()
        if batch.name == defaultBatch:
            sys.stdout.write("* " + summary + " *\n")
        else:
            sys.stdout.write("  " + summary + "  \n")
    sys.stdout.write("\n")

def listCodes(codes):
    """List the defined simulation codes.

           Arguments:
              array codes      - Array of defined codes
        """
    if len(codes) < 1:
        sys.stdout.write("\nNo simulation codes defined.\n")
    else:    
        sys.stdout.write("\nDefined simulation codes:\n\n")
        for code in codes:
            sys.stdout.write("-------------------------------------------------\n")
            summary = code.summaryString()
            sys.stdout.write(summary + "\n")
        sys.stdout.write("\n")

def printHelp(rootDir):
    """Print help for the tool.
           
           Arguments:
              str rootDir - The root install directory of the tool.
        """
    subprocess.call(["pydoc", rootDir + "/bin/bolt"])

def printLicence(rootDir):
    """Print licence for the tool.
           
           Arguments:
              str rootDir - The root install directory of the tool.
        """
    subprocess.call(["cat", rootDir + "/COPYING"])

if __name__ == "__main__":
    main(sys.argv[1:])

