## when node down: lamhlat and lamboot;
## when node up  : lamgrow

## quitar lamhalt and lamwipe de los checkdone y R


## donde estan los checkMPI de maqs. caton?


## algun lamclean??



## mover todo killOldLAM a killOldR


#############################
## cuando Up_is_Down

##      despues de poner bien el def, hacer lamboot (e.g., nodo 1)


## cuando Down_is_Up:
##      os.system('lamgrow ' + machine)



## Nueva f(): lamcheck()

def lamcheck():
    'Do a lamnodes, check we get the right count of nodes. O.w., lamboot'.
    lf1 = int(os.popen('wc /http/mpi.defs/lamb-host.karl01.def').readline().split()[0])
    lf2 = int(os.popen('grep "#" /http/mpi.defs/lamb-host.karl01.def | wd').readline().split()[0])
    L_NODES = lf1 - lf2
    if (int(os.popen('lamnodes | wc').readline().split()[0]) < L_NODES):
        os.system('lamboot -H /http/mpi.defs/lamb-host.karl01.def')


##order is:Up_is_Down, Down_is_Up, lamcheck.

## OJO!!!! todo esto tiene que correr como www-data!!!!


