#
# Configuration file for Jugene BG/P
#
[system info]
system name:        Jugene
system description: BlueGene/P
job script shell:   #!/bin/bash
batch system:       LL_BGP
total nodes:        73728
account code required: no
default account code:


[node info]
sockets per node:      32
dies per socket:       1
cores per die:         4
exclusive node access: yes
accelerator type:

[parallel jobs]
parallel jobs:              True
maximum tasks:              294912
minimum tasks:              4096
maximum job duration:       12
parallel time format:       hms
preferred task stride:      1
parallel reservation unit:  nodes
parallel job launcher:      mpirun
number of tasks option:     -np
number of nodes option:
tasks per node option:
tasks per die option:
tasks stride option:
queue name:                 bluegene
parallel allocation option:
additional job options:
script preamble commands:
script postamble commands:

[serial jobs]
serial jobs:               True
maximum job duration:      12
serial time format:        hms
queue name:                serial
additional job options:
script preamble commands:
script postamble commands:

