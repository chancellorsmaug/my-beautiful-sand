
import math, random
import numpy as np
from pylmgc90 import pre

def disk_grains(bodies, model, material, dradii, coords): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidDisk(r=r, center=c, model=model, material=material, color='grain')
        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)

def disk_grains_mag(bodies, model, material, dradii, coords, dx): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidDisk(r=r, center=c, model=model, material=material, color='grain')
        grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx, 0])
        grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx, 0])
        grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[-dx, 0])
        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)
        
        
def polyg_grains(bodies, vertices, model, material, dradii, coords): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidPolygon(radius=r, nb_vertices=vertices, 
                                 center=c, model=model, material=material, color='grain')
        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)

def triangle_grains_mag(bodies, vertices, model, material, dradii, coords, dx): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidPolygon(radius=r, nb_vertices=vertices, 
                                 center=c, model=model, material=material, color='grain')
        grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx, 0])
        grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[dx*math.cos(math.pi*2/3), -dx*math.sin(math.pi*2/3)])
        grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[dx*math.cos(math.pi*2/3), -dx*math.sin(math.pi*2/3)])
        final = random.random()
        if final >= 0.5: 
            grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[dx*math.cos(-math.pi*2/3), dx*math.sin(-math.pi*2/3)])
            grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[dx*math.cos(-math.pi*2/3), dx*math.sin(-math.pi*2/3)])
        else: 
            grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx*math.cos(-math.pi*2/3), dx*math.sin(-math.pi*2/3)])

        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)

def square_grains_mag(bodies, vertices, model, material, dradii, coords, dx, type): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidPolygon(radius=r, nb_vertices=vertices, 
                                 center=c, model=model, material=material, color='grain')
        if type == 'bar': 
            grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx, 0])
            grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx, 0])
            grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[-dx, 0])
            grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx*math.pi*0.5, 0])
            grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx*math.pi*0.5, 0])
            grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[-dx*math.pi*0.5, 0])
        if type == 'alt': 
            grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx, 0])
            grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[-dx, 0])
            grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[dx*math.pi*0.5, 0])
            grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[dx*math.pi*0.5, 0])
            grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx*math.pi*0.5, 0])
            grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[-dx*math.pi*0.5, 0])

        final = random.random()
        if final >= 0.5: 
            grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx*math.cos(-math.pi*2/3), dx*math.sin(-math.pi*2/3)])
        else: 
            grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[-dx*math.cos(-math.pi*2/3), dx*math.sin(-math.pi*2/3)])

        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)



def needle_grains(bodies, vertices, model, material, dradii, coords): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidOvoidPolygon(ra=r, rb=0.4*r, nb_vertices=vertices,  
                                      center=c, model=model, material=material, color='grain')
        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)

def needle_grains_mag(bodies, vertices, model, material, dradii, coords, dx): 
    for r,c in zip(dradii, coords):
        grain = pre.rigidOvoidPolygon(ra=r, rb=0.3*r, nb_vertices=vertices,  
                                      center=c, model=model, material=material, color='grain')
        grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx, 0])
        grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx, 0])
        grain.addContactors(shape='DISKx', color='NULLx', byrd=0.07*r, shift=[-dx, 0])
        grain.rotate(description='axis', alpha=math.pi*random.random(), axis=[0., 0., 1.], center=c)
        bodies.addAvatar(grain)


def get_grains_volume(name: str, step: int):

    vol = 0

    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    for b in bodies: 
        if b.contactors[0].color == 'grain':
            vol += b.contactors[0].area

    return vol

def get_approx_packing_frac(name:str, step:int): 

    box_area = get_box_vol(name=name, step=step)

    if 'compression' in name: # grain vol only calculated once 
        path = name[:-12]
    elif 'shearing' in name: 
        path = name[:-9]
    else: 
        path = name
    
    with open(f"{path}/init_grain_vol", 'r') as ini: 
        grain_vol = float(ini.readline()) # should only be one line 

    phi = grain_vol / box_area

    with open(f"{name}/phi/packing_frac_{step}", 'w') as ini: 
        ini.write(str(phi))
    
    return phi

def get_box_vol(name, step):
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    coor = []
    for b in bodies: 
        if b.contactors[0].color != 'walls':
            for n in b.nodes:
                ref = b.getNodeCoor(n.number) # this already takes the real coord !
                # disp = n.dof.disp
                # new = np.add(ref, disp)
                coor.append(ref)
                if max([c[1] for c in coor]) == ref[1]:
                    best_b = b

    
    top = max([c[1] for c in coor]) # max y coord
    if best_b.contactors[0].shape == 'DISKx': 
        height = top + best_b.contactors[0].byrd
    if best_b.contactors[0].shape == 'POLYG':
        verts = best_b.contactors[0].vertices
        top_vert = max(verts[:,1])
        height = top + top_vert
    
    box_area = 110.*height

    path = f"{name}/box_vol.txt"

    with open(path, 'a') as f: 
        f.write(str(step)+', '+str(box_area) + '\n')

    return box_area




# if vertices%2 == 0: 
#             for i in range(int(vertices/2)): 
#                 grain.addContactors(shape='DISKx', color='NORTH', byrd=0.2*r, shift=[dx, 0])
#                 grain.addContactors(shape='DISKx', color='SOUTH', byrd=0.2*r, shift=[-dx, 0])
#                 grain.rotate(description='axis', alpha=(i+1)*math.pi/(int(vertices/2)), axis=[0., 0., 1.], center=c) # definitely test this -_-
#         else: 
            
def get_wall_ids(name:str, step:int): 
    # bdy = re.compile('RBDY2\b*')
    # matre = re.compile(mat)
    print(f"{name}/OUTBOX", step)
    ids = []
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)
    for b in bodies: 
        if b.contactors[0].color == 'WALLx':
            ids.append(b.number)
            
    print('Num walls:', len(ids))
    print(ids)
    return ids, len(ids)


def get_right(name, step):
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    coor = []
    for b in bodies: 
        if b.contactors[0].color != 'WALLx':
            for n in b.nodes:
                ref = b.getNodeCoor(n.number) # this already takes the real coord !
                # disp = n.dof.disp
                # new = np.add(ref, disp)
                coor.append(ref)
    
    right = max([c[0] for c in coor])
    return right
    