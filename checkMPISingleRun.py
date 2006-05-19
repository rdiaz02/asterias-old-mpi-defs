#!/usr/bin/python

import os
import time
import glob

lamDefs = glob.glob('lamb-host.*.def')
##machinesUp = ['192.168.2.' + str(i) for i in range(1, 34)]
machinesUp = ['192.168.2.' + str(i) for i in range(1, 31)]
machinesDown =[]

## We only change a line when there has been a change in
## the status of a machine. When a machine goes from being
## up to being down, or viceversa.


def Up_is_Down():
    """ Uses ping to verify if machines are up.
    If they are not, add a '#' to the corresponding
    line in the lamb-host.hostname.def."""
    global machinesDown
    global machinesUp
    for machine in machinesUp:
        dead = os.system('ping -q -c1 ' + machine)
        if dead:
	    print "This is dead" + str(dead)
            machinesDown.append(machine)
	    machinesUp.remove(machine)
            for lamdef in lamDefs:
                os.system("sed 's/" + machine + " /#" + 
                    machine + " /' " + lamdef + 
                    " > tmpdef; mv tmpdef " + lamdef)


def Down_is_Up():
    global machinesUp
    global machinesDown
    for machine in machinesDown:
        dead = os.system('ping -q -c1 ' + machine)
        if not dead:
            machinesUp.append(machine)
	    machinesDown.remove(machine)
            for lamdef in lamDefs:
                os.system("sed 's/#*" + machine + " /" +
                    machine + " /' " + lamdef + 
                    " > tmpdef; mv tmpdef " + lamdef)


Up_is_Down()
Down_is_Up()
 
