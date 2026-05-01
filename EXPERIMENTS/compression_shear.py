from pylmgc90 import pre
import numpy as np
from pathlib import Path

def imposedForce(t):
    if t <=1.:
        f = 1e+5
    elif t > 1. and t<=5. : 
       f = 1e+5*t
    else: 
       f = 5e+5
    return -f
    

def gen_sample_compression(name:str, size_range: list, step: int):
    # pre.setStopMode('pass')
    # datbox = Path(f"{name}_compression/DATBOX")
    datbox = Path(f"{name}_compression/DATBOX")
    datbox.mkdir(exist_ok=True)

    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    # from press2shear example
    ref_coor = [ [ b.getNodeCoor(n.number).tolist() for n in b.nodes ] for b in bodies ]
    bodies.updateReferenceConfig()
    disp_ok = True
    for b in bodies:
        for n in b.nodes:
            disp_ok = np.all( n.dof.disp == 0. )
            if not disp_ok:
                break
        if not disp_ok:
            break
    assert disp_ok, 'After updating reference configuration, there are node with a disp not null'
    new_coor = [ [ b.getNodeCoor(n.number).tolist() for n in b.nodes ] for b in bodies ]
    assert new_coor == ref_coor, 'Different configuration before and after UpdateReferenceConfig'

    wall = mats['walls']
    model = pre.model(name='rigid', physics='MECAx', element='Rxx2D', dimension=2)
    top_grain = max([new_coor[i][0][1] for i in range(len(new_coor))]) # max y coord
    # right_grain = max([new_coor[i][0][0] for i in range(len(new_coor))])
    print(top_grain)

    instants=np.linspace(0,8.,10000)

    
    pre.writeEvolution(f=imposedForce, instants=np.linspace(0,8.,10000), path=f"{name}_compression/DATBOX/", name='Fy.dat')
    lid = pre.smoothWall(center=[50., top_grain + size_range[1] + 5.], theta=0.0, l=1.5*110.,
                         h=5., nb_polyg=12, model=model, material= wall, color='WALLx') 
    lid.imposeDrivenDof(description = 'evolution', component = 2, dofty = 'force', evolutionFile = 'Fy.dat')
    # pre.writeEvolution(f=imposedForce, instants=np.linspace(0,8.,10000), path=f"{name}_compression/DATBOX/", name='Fy.dat')
    lid.imposeDrivenDof(component=1, dofty='vlocy') 
    bodies.addAvatar(lid)

    post = pre.postpro_commands()
    basic = pre.postpro_command(name='SOLVER INFORMATIONS', step=10)
    post.addCommand(basic)

    pre.writeDatbox(dim=2, mats=mats, mods=mods, bodies=bodies, tacts=tacts, sees=svs, post=post, 
                    datbox_path=f"{name}_compression/DATBOX", gravy=[0., 0., 0.]) #no more gravity 

    print('complete')
    # return right_grain

from pylmgc90 import chipy

def gen_sample_shear(name:str, step: int):
    # pre.setStopMode('pass')
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step) # _compression 

    pre.readState(bodies, f"{name}/OUTBOX", step)


    ref_coor = [ [ b.getNodeCoor(n.number).tolist() for n in b.nodes ] for b in bodies ]
    bodies.updateReferenceConfig()
    disp_ok = True
    for b in bodies:
        for n in b.nodes:
            disp_ok = np.all( n.dof.disp == 0. )
            if not disp_ok:
                break
        if not disp_ok:
            break
    assert disp_ok, 'After updating reference configuration, there are node with a disp not null'
    new_coor = [ [ b.getNodeCoor(n.number).tolist() for n in b.nodes ] for b in bodies ]
    assert new_coor == ref_coor, 'Different configuration before and after UpdateReferenceConfig'

    move = bodies[0]

    move.imposeDrivenDof(component=2, dofty='vlocy')  
    move.imposeDrivenDof(component=1, dofty='vlocy', ct = 2.) 
    # bodies.addAvatar(move)
    
    lid = bodies[-1]


    right = bodies[2]
    right.relaxDrivenDof(group='all', component=1)
    right.imposeDrivenDof(component=1, dofty='force', ct = -5e+4)

    # lid.imposeDrivenDof(component=2, dofty='vlocy')

    post = pre.postpro_commands()
    basic = pre.postpro_command(name='SOLVER INFORMATIONS', step=10)
    post.addCommand(basic)

    pre.writeDatbox(dim=2, mats=mats, mods=mods, bodies=bodies, tacts=tacts, sees=svs, post=post, 
                    datbox_path=f"{name}_shearing/DATBOX", gravy=[0., 0., 0.]) # no more gravity 

    print('complete')
