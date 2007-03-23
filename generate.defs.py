#!/usr/bin/python
''' Generate the lamb-host.def files.'''


BASE_NAME = 'karl'
BASE_IP = '192.168.7.'
N_CPUS  = '4'
N_CPUS4  = '4'
N_CPUS2  = '2'
N_CPUS1  = '1'

for i in range(1, 32):
    if i < 10:
	j = '0' + str(i)
    else:
	j = str(i)
    outf = open('lamb-host.' + BASE_NAME + j + '.def', mode = 'w')
    outf2 = open('lamb-host.' + BASE_NAME + j + '.2cpu.def', mode = 'w')
    outf1 = open('lamb-host.' + BASE_NAME + j + '.1cpu.def', mode = 'w')
    outf4 = open('lamb-host.' + BASE_NAME + j + '.4cpu.def', mode = 'w')

    for m in range(i, 32):
    	if m != 21:  #and m != 27 and m != 31:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n')
            outf2.write(BASE_IP + str(m) + ' cpu=' + N_CPUS2 + '\n') 
            outf1.write(BASE_IP + str(m) + ' cpu=' + N_CPUS1 + '\n') 
            outf4.write(BASE_IP + str(m) + ' cpu=' + N_CPUS4 + '\n') 
    for m in range(1, i):
    	if m != 21: # and m != 27 and m != 31:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n')
            outf2.write(BASE_IP + str(m) + ' cpu=' + N_CPUS2 + '\n')             
            outf1.write(BASE_IP + str(m) + ' cpu=' + N_CPUS1 + '\n')             
            outf4.write(BASE_IP + str(m) + ' cpu=' + N_CPUS4 + '\n')             
    outf.close()


