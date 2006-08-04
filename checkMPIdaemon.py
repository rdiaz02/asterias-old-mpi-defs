#!/usr/bin/python2.4

## Changes (August, 2006): the logic is changed. We no longer keep a
## machinesUp list, since that would then not be able to pick changes made
## on the defs (e.g., adding defs) after the daemon is started. We alsays
## verify all the machines, and only update the machinesDown list.

## BEWARE: if the actual machines are changed, you need to restart the
## script. But there is rarely any need to change this. And it does not
## matter if you actually examine machines that are not there (except for
## the ssh time).




## Next four are to be substituted by installation script
EMAIL_LOGIN    = "AsteriasMail@gmail.com"
EMAIL_PASSWORD = "5 Cavallitos de Mar"
EMAIL_RECEIVERS = ('rdiaz02@gmail.com', 'aalibes@gmail.com', 'acanada@gmail.com')
MPI_DEFS_DIR = '/http/mpi.defs/'


import os
import time
import glob
import sys
## Next are for email sending
from smtplib import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def send_from_gmail(email, body, subject):
    server = SMTP('smtp.gmail.com',587)
## server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject']=subject
    outer['To']= email
    outer['From']= EMAIL_LOGIN
    outer.preamble = '\n'
    # To guarantee the message ends with a newline
    outer.epilogue =''
    # Note: we should handle calculating the charset
    msg = MIMEText(body)
    # Message body
    outer.attach(msg)
    text = outer.as_string()
    server.sendmail(outer['From'], outer['To'], text)
    # SSL error because of bad comunication closing
    try:
        server.quit()
    except:
        pass

## Next is to allow demonizing
DAEMON = True

## From Python Cookbook, p. 388. Beware: this probably WILL NOT
## work under Windows
def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """This forks the current process into a daemon.
    The stdin, stdout, and stderr arguments are file names that
    will be opened and be used to replace the standard file descriptors
    in sys.stdin, sys.stdout, and sys.stderr.
    These arguments are optional and default to /dev/null.
    Note that stderr is opened unbuffered, so
    if it shares a file with stdout then interleaved output
    may not appear in the order that you expect.
    """
    # Do first fork.
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0) # Exit first parent.
    except OSError, e: 
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
        
    # Decouple from parent environment.
    os.chdir("/") 
    os.umask(0) 
    os.setsid() 
    
    # Do second fork.
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0) # Exit second parent.
    except OSError, e: 
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
        
    # Now I am a daemon!
    
    # Redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())




## We only change a line when there has been a change in
## the status of a machine. When a machine goes from being
## up to being down, or viceversa.


def Up_is_Down(machinesAll, machinesDown, lamDefs):
    """ Uses ping to verify if machines are up.
    If up, check the file sistem is writable.
    If they are not, add a '#' to the corresponding
    line in the lamb-host.hostname.def."""
    for machine in machinesAll:
        dead = os.system('ping -q -c1 ' + machine)
	writeable = False
	if not dead:
	    writeable = not(os.system("ssh " + machine + " 'touch /tmp/trytouch' "))
	if dead or (not (writeable)):
            machinesDown.append(machine)
##	    machinesUp.remove(machine)
            for receiver in EMAIL_RECEIVERS:
                send_from_gmail(receiver,
                                '[CLUSTER] Machine failure: ' + machine,
                                '[CLUSTER] Machine failure: ' + machine)
            for lamdef in lamDefs:
                os.system("sed -i 's/" + machine + " /#" + 
                    machine + " /' " + lamdef)
                os.system("sed -i 's/#*" + machine + " /#" +
                    machine + " /' " + lamdef)
    return machinesDown

def Down_is_Up(machinesDown, lamDefs):
    for machine in machinesDown[:]:
        dead = os.system('ping -q -c1 ' + machine)
	writeable = False
	if not dead:
	    writeable = not(os.system("ssh " + machine + " 'touch /tmp/trytouch' "))
        if (not dead) and writeable:
##            machinesUp.append(machine)
	    machinesDown.remove(machine)
            for lamdef in lamDefs:
                os.system("sed -i 's/#*" + machine + " /" +
                    machine + " /' " + lamdef)
    return machinesDown

if DAEMON:
    daemonize()


machinesAll = ['192.168.2.' + str(i) for i in range(1, 31)]    
machinesDown =[]

while True:
    lamDefs = glob.glob(MPI_DEFS_DIR + 'lamb-host.*.def')
    machinesDown = Up_is_Down(machinesAll, machinesDown, lamDefs)
    machinesDown = Down_is_Up(machinesDown, lamDefs)
    time.sleep(30)
 
