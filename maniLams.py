#!/usr/bin/python

import os

for i in range(125):
    os.system('export LAM_MPI_SESSION_SUFFIX="' + str(i) + '"; lamboot /http/mpi.defs/lamb-host.karl01.def')
    
