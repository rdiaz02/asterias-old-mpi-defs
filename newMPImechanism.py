#!/usr/bin/python

## BEWARE: all of this has to run as www-data!!!!

import os
import time
import glob

BASE_IP = '192.168.7.'
RANGE_IPS = range(1, 32)

lamDefs = glob.glob('lamb-host.*.def')

machinesAll = [BASE_IP + str(i) for i in RANGE_IPS]


def lamboot(machine):
    'Boot a lam universe'
    os.system('lamboot -H /http/mpi.defs/lamb-host.' + machine + '.def')

def lamgrow(machine, cpu = 4):
    'Add a machine to a lam universe'
    os.system('lamgrow -cpu ' + str(cpu) + ' ' + machine)

def lamnodes():
    'List of nodes in a lam universe'
    lnodes = os.popen('lamnodes -i -n -c').readlines()
    lnc = []
    for node in lnodes:
        lnc = lnc + node.split()
    return lnc


def test_node_ok(machine):
    """ Test the node: ping and writeable"""
    dead = os.system('ping -q -c1 ' + machine)
    if dead:
        return 0
    else:
        writeable = not(os.system("ssh " + machine +\
                                  " 'touch /var/www/trytouch' "))
        return writeable

    
def maybe_add_nodes(all_nodes, current_nodes):
    """ If an OK node not part of current
    universe, add it."""
    if len(all_nodes) < len(current_nodes):
        raise AssertionError, 'len(all_nodes) < len(current_nodes)'
    if len(all_nodes) == len(current_nodes):
        pass
    else:
        for one_anode in all_nodes:
            if one_anode not in current_nodes:
                if test_node_ok(one_anode) == 1:
                    lamgrow(one_anode)
                
        
def check_tping(tsleep = 5, nc = 5):
    """ Use tping to verify LAM universe OK.
    tsleep is how long we wait before checking output of tping."""
    
    tmp2 = os.system('tping C N -c' + str(nc) + ' > /http/mpi.defs/tping.out & ')
    time.sleep(tsleep)
    tmp = int(os.popen('wc /http/mpi.defs/tping.out').readline().split()[0])
    if tmp == 0:
        return 0
    elif tmp > 0:
        return 1
    else:
        return 0

def machines_check_and_lamboot(machinesAll, lamDefs, tw = 5):
    """ lamhalt, lamwipe, checks each machine, and fresh lamboot ."""

    os.system('lamhalt &')
    time.sleep(tw)
    os.system('lamwipe &')
    time.sleep(tw)
       
    machinesUp = []
    for machine in machinesAll:
        if test_node_ok(machine) == 1:
            machinesUp.append(machine)
            for lamdef in lamDefs:
                os.system("sed -i 's/#*" + machine + " /" +
                          machine + " /' " + lamdef)
        elif test_node_ok(machine) == 0:
            for lamdef in lamDefs:
                os.system("sed -i 's/" + machine + " /#" + 
                          machine + " /' " + lamdef)
                os.system("sed -i 's/#*" + machine + " /#" +
                          machine + " /' " + lamdef)
        else:
            raise AssertionError, 'test_node_ok should only return 0 or 1'
        
    lamboot(machinesUp[0])
    


os.system('/http/mpi.defs/generate.defs2.py')
lam_ok = check_tping()
if lam_ok == 1:
    current_nodes_lam = lamnodes()
    maybe_add_nodes(machinesAll, current_nodes_lam)
else:
    machines_check_and_lamboot(machinesAll, lamDefs)




# no longer any sense
# def lamcheck(machine):
#     'Do a lamnodes, check we get the right count of nodes. O.w., lamboot'
#     lf1 = int(os.popen('wc /http/mpi.defs/lamb-host.' + machine + '.def').readline().split()[0])
#     lf2 = int(os.popen('grep "#" /http/mpi.defs/lamb-host.' + machine + '.def | wc').readline().split()[0])
#     L_NODES = lf1 - lf2
#     if (int(os.popen('lamnodes | wc').readline().split()[0]) < L_NODES):
#         ## zz
#         os.system('lamboot -H /http/mpi.defs/lamb-host.' + machine + '.def')

