#!/usr/bin/python

## BEWARE: all of this has to run as www-data!!!!

import os
import time
import glob
import socket

BASE_IP = '192.168.7.'
RANGE_IPS = range(1, 32)

lamDefs = glob.glob('lamb-host.*.def')

machinesAll = [BASE_IP + str(i) for i in RANGE_IPS]


log_mpi = open('/http/mpi.defs/secondMPImech.log', mode = 'a')


def test_node_ok(machine):
    """ Test the node: ping and writeable"""
    dead = os.system('ping -q -c1 ' + machine)
    if dead:
        return 0
    else:
        writeable = not(os.system("ssh " + machine +\
                                  " 'touch /var/www/trytouch' "))
        return writeable


def machines_check(machinesAll, lamDefs):
    """ lamhalt, lamwipe, checks each machine, and fresh lamboot ."""
       
    for machine in machinesAll:
        if test_node_ok(machine) == 1:
            log_mpi.write('check: machine ' + machine + ' UP\n')
            for lamdef in lamDefs:
                os.system("sed -i 's/#*" + machine + " /" +
                          machine + " /' " + lamdef)
        elif test_node_ok(machine) == 0:
            log_mpi.write('check: machine ' + machine + ' DOWN\n')
            for lamdef in lamDefs:
                os.system("sed -i 's/" + machine + " /#" + 
                          machine + " /' " + lamdef)
                os.system("sed -i 's/#*" + machine + " /#" +
                          machine + " /' " + lamdef)
        else:
            raise AssertionError, 'test_node_ok should only return 0 or 1'
        
    

def header_log():
    log_mpi.write('\n\n')
    log_mpi.write('##############################\n\n')
    log_mpi.write(socket.gethostname())
    log_mpi.write('\n')
    log_mpi.write(time.strftime('%d %b %Y %H:%M:%S'))
    log_mpi.write('\n\n')



header_log()
machines_check(machinesAll, lamDefs)
log_mpi.flush()
log_mpi.close()



