#
# Configuration file for Curie GPU nodes
#
[system info]
system name:        Curie-GPU
system description: bullx B chassis
job script shell:   #!/bin/bash --login
batch system:       SLURM_Bull
total nodes:        144
account code required: no
default account code:


[node info]
sockets per node:      2
dies per socket:       1
cores per die:         8
exclusive node access: yes
accelerator type:      NVidia M2090

[parallel jobs]
parallel jobs:              True
maximum tasks:              288
minimum tasks:              1
maximum job duration:       12
parallel time format:       seconds
preferred task stride:      1
parallel reservation unit:  tasks
parallel job launcher:      ccc_mprun
number of tasks option:     -n
number of nodes option:     -N
tasks per node option:
tasks per die option:
tasks stride option:
queue name:
parallel allocation option:
additional job options:
script preamble commands:
script postamble commands:

[serial jobs]
serial jobs:               True
maximum job duration:      12
serial time format:        seconds
queue name:
additional job options:
script preamble commands:
script postamble commands:

