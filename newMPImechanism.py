#!/usr/bin/python

import os
import time
import glob

BASE_IP = '192.168.7.'
RANGE_IPS = range(1, 32)

lamDefs = glob.glob('lamb-host.*.def')

machinesUp = [BASE_IP + str(i) for i in RANGE_IPS]
machinesAll = machinesUp
machinesDown =[]


## BEWARE: all of this has to run as www-data!!!!


## We only change a line when there has been a change in
## the status of a machine. When a machine goes from being
## up to being down, or viceversa.

def lamcheck(machine):
    'Do a lamnodes, check we get the right count of nodes. O.w., lamboot'
    lf1 = int(os.popen('wc /http/mpi.defs/lamb-host.' + machine + '.def').readline().split()[0])
    lf2 = int(os.popen('grep "#" /http/mpi.defs/lamb-host.' + machine + '.def | wc').readline().split()[0])
    L_NODES = lf1 - lf2
    if (int(os.popen('lamnodes | wc').readline().split()[0]) < L_NODES):
        os.system('lamboot -H /http/mpi.defs/lamb-host.' + machine + '.def')

def lamboot(machine):
    'Boot a lam universe'
    os.system('lamboot -H /http/mpi.defs/lamb-host.' + machine + '.def')

def lamgrow(machine, cpu = 4):
    'Add a machine to a lam universe'
    os.system('lamgrow -cpu ' + str(cpu) + ' ' + machine)


def Up_is_Down(machinesAll, machinesDown, machinesUp, lamDefs):
    """ Uses ping to verify if machines are up.
    If up, check the file sistem is writable.
    If they are not, add a '#' to the corresponding
    line in the lamb-host.hostname.def."""
    oldMachinesDown = machinesDown[:]
    for machine in machinesAll:
        dead = os.system('ping -q -c1 ' + machine)
	writeable = False
	if not dead:
	    writeable = not(os.system("ssh " + machine + " 'touch /var/www/trytouch' "))
	if dead or (not (writeable)):
            machinesDown.append(machine)
	    machinesUp.remove(machine)
            for lamdef in lamDefs:
                os.system("sed -i 's/" + machine + " /#" + 
                    machine + " /' " + lamdef)
                os.system("sed -i 's/#*" + machine + " /#" +
                    machine + " /' " + lamdef)
 
    if machinesDown != oldMachinesDown:
        lamboot(machinesUp[0])

    return machinesDown, machinesUp



def Down_is_Up(machinesDown, machinesUp, lamDefs):
    madd = []
    for machine in machinesDown[:]:
        dead = os.system('ping -q -c1 ' + machine)
	writeable = False
	if not dead:
	    writeable = not(os.system("ssh " + machine + " 'touch /var/www/trytouch' "))
        if (not dead) and writeable:
            machinesUp.append(machine)
	    machinesDown.remove(machine)
            madd = madd + list(machine)
            for lamdef in lamDefs:
                os.system("sed -i 's/#*" + machine + " /" +
                    machine + " /' " + lamdef)
    if len(madd) > 0:
        for mach in madd:
            lamgrow(mach)
    return machinesDown, machinesUp

os.system('/http/mpi.defs/generate.defs2.py')
machinesDown, machinesUp = Up_is_Down(machinesAll, machinesDown, machinesUp, lamDefs)
machinesDown, machinesUp = Down_is_Up(machinesDown, machinesUp, lamDefs)
lamcheck(machinesUp[0])




### change this; run over all machines.
### turn off those that do not answer
### keep track of those that answer
### verify which to add to lam


### but makes no sense to keep track of lists, since run anew.
