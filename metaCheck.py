#!/usr/bin/python

## checkMPIup stops after sending way too many messages.
## Thus, this "metascript" checks if it is running, and
## it it isn't it launches it. Should be run from crontab
## every reasonable number of hours, for instance 2 hours.
## its root who runs it.

import os

running = os.popen('/etc/init.d/checkMPIup status').readline() == 'OK, is running\n'

if not running:
    os.system('/etc/init.d/checkMPIup start')


