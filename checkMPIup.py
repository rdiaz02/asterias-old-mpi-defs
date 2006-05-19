#!/usr/bin/python

import os
import sys

start_stop = sys.argv[1]

if start_stop == 'start':
    tmp = os.popen('/http/mpi.defs/checkMPIdaemon.py &')
    print 'OK'
elif start_stop == 'stop':
    tmp = os.popen('killall checkMPIdaemon.py')
    print 'OK'
elif start_stop == 'status':
    tmp = os.popen('ps -C checkMPIdaemon.py --no-headers').readline()
    if tmp:
	print 'OK, is running'
    else:
	print 'stopped'



