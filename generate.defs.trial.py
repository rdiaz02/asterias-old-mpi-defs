#!/usr/bin/python

for i in [23, 24, 25, 26, 29]:
    j = str(i)
    outf = open('lamb-host.prot' + j + '.def', mode = 'w')
    for m in [23, 24, 25, 26, 29, 1]:
	outf.write('192.168.2.' + str(m) + ' cpu=2 \n') 
    outf.close()
