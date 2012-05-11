# This is the test configuration file for the HECToR 
# resource.

[system info]
system name:        HECToR-GPU
system description: Intel + NVidia Tesla
job script shell:   #!/bin/bash --login
batch system:       SGE
total nodes:        4
account code required: yes  ; Do we have to define a account code?
default account code:  group  ; 'group', actual value or empty for no default


[node info]
sockets per node:      1
dies per socket:       1
cores per die:         4
exclusive node access: no
accelerator type:      NVidia

[parallel jobs]
parallel jobs:              True
maximum tasks:              12    ; cores
minimum tasks:              1    ; cores
maximum job duration:       12    ; hours
parallel time format:       hms
preferred task stride:      1    ; cores
parallel reservation unit:  tasks    ; can be 'tasks' or 'nodes'
parallel job launcher:      mpiexec
number of tasks option:     -n
number of nodes option:
tasks per node option:
tasks per die option:
tasks stride option:
queue name:
parallel allocation option: mpich 
additional job options:
script preamble commands:
script postamble commands:

[serial jobs]
serial jobs:               True
maximum job duration:      12    ; hours
serial time format:       hms
queue name:
additional job options:
script preamble commands:
script postamble commands:

