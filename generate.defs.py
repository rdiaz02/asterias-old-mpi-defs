#!/usr/bin/python
''' Generate the lamb-host.def files.'''


BASE_NAME = 'karl'
BASE_IP = '192.168.7.'
N_CPUS  = '4'
N_CPUS4  = '4'
N_CPUS2  = '2'
N_CPUS1  = '1'

lll = range(1, 32)
##lll = range(1, 3) + range(4, 31)
#lll.append(30)
#lll.append(31)

#lexclude = range(13, 14) + range(25, 26) + range(29, 30) + range(99, 100)
lexclude = range(99, 100)
#lexclude.append(1)

for i in lll:
    if i < 10:
	j = '0' + str(i)
    else:
	j = str(i)
    outf = open('lamb-host.' + BASE_NAME + j + '.def', mode = 'w')
    outf2 = open('lamb-host.' + BASE_NAME + j + '.2cpu.def', mode = 'w')
    outf1 = open('lamb-host.' + BASE_NAME + j + '.1cpu.def', mode = 'w')
    outf4 = open('lamb-host.' + BASE_NAME + j + '.4cpu.def', mode = 'w')

    for m in range(i, lll[len(lll) - 1]):
    	if m != 99  and m not in lexclude:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n')
            outf2.write(BASE_IP + str(m) + ' cpu=' + N_CPUS2 + '\n') 
            outf1.write(BASE_IP + str(m) + ' cpu=' + N_CPUS1 + '\n') 
            outf4.write(BASE_IP + str(m) + ' cpu=' + N_CPUS4 + '\n') 
    for m in range(1, i):
    	if m != 99  and m not in lexclude:
            outf.write(BASE_IP + str(m) + ' cpu=' + N_CPUS + '\n')
            outf2.write(BASE_IP + str(m) + ' cpu=' + N_CPUS2 + '\n')             
            outf1.write(BASE_IP + str(m) + ' cpu=' + N_CPUS1 + '\n')             
            outf4.write(BASE_IP + str(m) + ' cpu=' + N_CPUS4 + '\n')             
    outf.close()


