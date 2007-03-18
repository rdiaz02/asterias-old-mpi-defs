#!/usr/bin/python
''' Generate the lamb-host.def files.'''


BASE_NAME = 'karl'
BASE_IP = '192.168.7.'
N_CPUS  = '4'

for i in range(1, 32):
    if i < 10:
	j = '0' + str(i)
    else:
	j = str(i)
    outf = open('lamb-host.' + BASE_NAME + j + '.def', mode = 'w')
    for m in range(i, 32):
    	if m != 21:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n') 
    for m in range(1, i):
    	if m != 21:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n') 
    outf.close()
