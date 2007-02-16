#!/usr/bin/python
''' Generate the lamb-host.def files.'''


#BASE_NAME = 'karl'
BASE_NAME = '192.168.7.'
BASE_IP = '192.168.7.'
N_CPUS  = '4'

for i in range(1, 32):
    j = str(i)
    outf = open('lamb-host.' + BASE_NAME + j + '.def', mode = 'w')
    for m in range(i, 32):
    	if m != 110:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n') 
    for m in range(1, i):
    	if m != 110:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n') 
    outf.close()
