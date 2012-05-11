#
# Configuration file for Curie fat nodes
#
[system info]
system name:        Curie-Fat
system description: S6010 bullx nodes, 128 GB Mem
job script shell:   #!/bin/bash --login
batch system:       SLURM_Bull
total nodes:        360
account code required: no
default account code:


[node info]
sockets per node:      4
dies per socket:       1
cores per die:         8
exclusive node access: yes
accelerator type:

[parallel jobs]
parallel jobs:              True
maximum tasks:              11520
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

