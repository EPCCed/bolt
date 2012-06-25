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

#------------------------------------------------------------------
# System description
#
# This section sets system wide configurations for the 
# resource
#------------------------------------------------------------------
[system info]

# The name of the system and a short description of the 
# compute architecture (only used for information 
# purposes)
system name:           Huygens
system description:    IBM SMP Power6 Linux x64

# Specify the shell definition line that will be placed
# at the top of every job submission script
job script shell:      #!/bin/bash

# Specify the batch system name - the name must correcpond
# to the name of a system defined in the corresponding batch
# system configuration files
batch system:          LL_PPC64

# Total number of compute nodes on the system (currently used
# to calculate the number of cores available for information
# purposes only)
total nodes:           109

# Are job submission scripts required to set an account ID option
# (usually for charging purposes). 
account code required: no

# If no account code is specified what is the default value
# (if any). If the string 'group' is used then the tool will
# set the account code as the user's *nix group name. Any
# other string will be used as the default. If this option is
# not specified then there will be no default. Users 
# can override the default by using the appropriate command
# line option.
default account code:  

#------------------------------------------------------------------
# Node definition
#
# This section specifies the hardware layout of the nodes in 
# terms of number of sockets, dies (NUMA regions) per socket
# and cores per die.
#
# Cores per node = sockets * dies per socket * cores per die
#------------------------------------------------------------------
[node info]

# The number of physical processor sockets per node
sockets per node:      1

# The number of dies (or NUMA regoins) per socket
dies per socket:       4

# The number of cores per die
cores per die:         8

# Does each job have exclusive access to a compute node (even
# if it uses less than the total number of cores per node) or
# can different jobs share compute nodes
exclusive node access: no

# Specify the type of accelerator cards (if any) on the node
# (not currently used)
accelerator type:

#------------------------------------------------------------------
# Settings for parallel jobs
#
# This section specifies all the options for parallel jobs on
# the compute resource.
#------------------------------------------------------------------
[parallel jobs]

# Specify whether or not parallel jobs are available
parallel jobs:              yes

# The maximum number of parallel tasks allowed for a single job
maximum tasks:              5120

# The minimum number of parallel tasks needed for a single job
minimum tasks:              1

# The maximum job duration (in whole hours) allowed for parallel jobs
maximum job duration:       120

# The format that the parallel job time will be printed in in
# the job submission script. Valid values are:
#   + hms = hh:mm:ss
#   + hours
#   + seconds
parallel time format:       hms

# The preferred spacing between parallel task placement on a node
# (if the number of tasks per node specified allows this 
# flexibility and the job launcher supports task placement at
# this level).
preferred task stride:      1

# Define how parallel resources are rquested in a batch script. Valid
# values are:
#  + 'tasks' - Number of tasks is used
#  + 'nodes' - Number of nodes is used
parallel reservation unit:  nodes    ; can be 'tasks' or 'nodes'

# The parallel job launcher command (for example, 'mpiexec' or 'aprun')
# If this is unset then we assume that the batch system automatically
# launches the parallel job.
parallel job launcher:      

# The command line option to the job launcher command that specifies
# the number of parallel tasks
number of tasks option:     

# The command line option to the job launcher command that specifies
# the number of nodes to use
number of nodes option:

# The command line option to the job launcher command that specifies
# the number of tasks per node (if blank, tool assumes that this 
# functionality is not supported).
tasks per node option:      

# The command line option to the job launcher command that specifies
# the number of tasks per die (if blank, tool assumes that this 
# functionality is not supported).
tasks per die option:      

# The command line option to the job launcher command that specifies
# the stride between parallel tasks (if blank, tool assumes that this 
# functionality is not supported).
tasks stride option:       

# The queue name to use for parallel jobs (if blank, it is assumed that
# no queue name is needed)
queue name:

# Do we want to use the batch system to specify the distribution of
# tasks? This is only usually needed if your system does not have 
# an explicit parallel job launcher command and the batch system 
# launches the parallel job instead (for example, LoadLeveller on
# some IBM Power systems)
use batch parallel options: True

# Any addtional batch submission options to add to parallel
# jobs (without the option ID).
additional job options:

# Any script lines to include in parallel jobs before the
# application is launched
script preamble commands:

# Any script lines to include in parallel jobs after the
# application has finished
script postamble commands:

#------------------------------------------------------------------
# Settings for serial jobs
#
# This section specifies all the options for serial jobs on
# the compute resource.
#------------------------------------------------------------------
[serial jobs]

# Specify whether or not serial jobs are available
serial jobs:               yes

# The maximum job duration (in whole hours) allowed for serial jobs
maximum job duration:      120

# The format that the parallel job time will be printed in in
# the job submission script. Valid values are:
#   + hms = hh:mm:ss
#   + hours
#   + seconds
serial time format:       hms

# The queue name to use for serial jobs (if blank, it is assumed that
# no queue name is needed)
queue name:                

# Any addtional batch submission options to add to serial
# jobs (without the option ID).
additional job options:

# Any script lines to include in parallel jobs before the
# application is launched
script preamble commands:   # Switch to current working directory
                            # cd $PBS_O_WORKDIR

# Any script lines to include in parallel jobs after the
# application has finished
script postamble commands:

