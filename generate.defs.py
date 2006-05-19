#!/usr/bin/python

for i in range(1, 34):
    if i < 10:
	j = '0' + str(i)
    else:
	j = str(i)
    
    outf = open('lamb-host.prot' + j + '.def', mode = 'w')
    for m in range(i, 34):
	if m != 31 and m != 33 and m != 32 and m != 14 and m != 15 :
	    outf.write('192.168.2.' + str(m) + ' cpu=2 \n') 
    if i > 1:
	for m in range(1, i):
	    if m != 31 and m != 33 and m != 32 and m != 14 and m != 15 :
		outf.write('192.168.2.' + str(m) + ' cpu=2 \n') 
    outf.close()
