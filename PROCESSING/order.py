from pylmgc90 import pre
import numpy as np 
import cmath, re
# from general import get_approx_packing_frac

def read_vol(name, step):
    path = f"{name}/box_vol.txt"
    find = re.compile(f"{step}")
    with open(path) as p: 
        for line in p: 
            if find.search(line) != None: 
                vol = float(re.split(',', line)[-1])
    return vol

def get_dists(name, step):  
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    coor, num_grains = get_coor(bodies=bodies)

    print(np.shape(coor[1]))
    dists2 = np.array([])
    for key in coor: 
        dists1 = np.array([np.linalg.norm(coor[key] - coor[j]) for j in coor if j > key] )
        # print(dists1)
        dists2 = np.concatenate((dists2, dists1))    
    
    return dists2, num_grains
    
def get_rdf(name, step, r, bin, dists2, num_grains): 

    # dists2 = get_dists(name=name, step=step)

    equal_r = [1 if dist <= r + 0.5*bin and dist >= r - 0.5*bin else 0 for dist in dists2] # within a range...

    vol = read_vol(name, step)
    rho =  num_grains / vol #read_phi(name=name, step=step) ITS NUMBER DENSITY NOT PACKING FRAC!!!!!!!!
    print(num_grains, rho, r)
    rdf_scale = 1/(num_grains*rho*np.pi*r)

    rdf = sum(equal_r)*rdf_scale
        
    # with open(f"{name}/rdf/rdf_{r}_{step}", 'a') as f: 
    #     f.write('average: ' + str(rdf) + '\n')
        # for i in range(len(dists2)): 
        #     f.write(f"{i+1}: {dists2[i]}\n")  # idk about anything else 


    return rdf 

def get_q6(name, step): 
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    coords, num = get_coor(bodies=bodies) #this should be ordered....
    
    all_inters_coords = np.empty((len(inters),4))
    for k, i in enumerate(inters): 
        all_inters_coords[k] = [i[3], i[7], i[19][0], i[19][1]] # node keys for the two interacting grains, and the coordinates.

    sort= {}
    for k in range(num): 
        sort[k+1]=[]
        for j in range(len(all_inters_coords)): 
            if all_inters_coords[j][0]==k+1:
                sort[k+1] += [all_inters_coords[j][1]]                
            elif all_inters_coords[j][1]==k+1:
                sort[k+1] += [all_inters_coords[j][0]]  # CONTACTORS FOR EACH GRAIN

    angles = {}
    # print(coords[3])
    for key in sort: 
        centre = coords[key]
        angles[key] = []
        for tact in sort[key]: 
            key2 = int(tact)
            # print(coords[key2])
            angles[key] += [angle_between(centre=centre, point=coords[key2])] # for disks this is the same as the ctct coords, for polygs this prevents recounting.

    print(angles[3], sort[3])
    q_j = []
    for key in angles: 
        if len(angles[key]) != 0:
            q = abs(sum([cmath.exp(6j*theta) for theta in angles[key]]) / len(angles[key]))
            q_j += [q]
        else:
            q_j += [0]
    

    if len(q_j) != num: 
        print('something may not be right.... check for 0 ctcs!')

    q6 = sum(q_j) / len(q_j)


    with open(f"{name}/bond_order/bond_order_{step}", 'a') as f: 
        f.write('average: ' + str(q6) + '\n')
        for i in range(len(q_j)): 
            f.write(f"{i+1}: {q_j[i]}\n")

    return q6 # i hope! 


def get_coor(bodies): 
    coor = {}
    num_grains = 0
    for b in bodies: 
        if b.contactors[0].color != 'walls':
            num_grains +=1
            for n in b.nodes:
                ref = b.getNodeCoor(n.number)
                coor[b.number] = ref
    return coor, num_grains


def angle_between(centre, point): 
    v1 = (point[0]-centre[0], point[1]-centre[1])
    v2 = (centre[0]+ np.linalg.norm(v1), centre[1])

    if v1[1] <= v2[1] + 0.0005 and v1[1] >= v2[1] - 0.0005: # angle is 0 or pi
        if centre[0] < point[0]: 
            angle_rad = 0.
        else: 
            angle_rad = np.pi 
    else: 
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))

    return angle_rad


def get_qn(name, step, n): 
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)

    coords, num = get_coor(bodies=bodies) #this should be ordered....
    
    all_inters_coords = np.empty((len(inters),4))
    for k, i in enumerate(inters): 
        all_inters_coords[k] = [i[3], i[7], i[19][0], i[19][1]] # node keys for the two interacting grains, and the coordinates.

    sort= {}
    for k in range(num): 
        sort[k+1]=[]
        for j in range(len(all_inters_coords)): 
            if all_inters_coords[j][0]==k+1:
                sort[k+1] += [all_inters_coords[j][1]]                
            elif all_inters_coords[j][1]==k+1:
                sort[k+1] += [all_inters_coords[j][0]]  # CONTACTORS FOR EACH GRAIN

    angles = {}
    # print(coords[3])
    for key in sort: 
        centre = coords[key]
        angles[key] = []
        for tact in sort[key]: 
            key2 = int(tact)
            # print(coords[key2])
            angles[key] += [angle_between(centre=centre, point=coords[key2])] # for disks this is the same as the ctct coords, for polygs this prevents recounting.

    print(angles[3], sort[3])
    q_j = []
    for key in angles: 
        if len(angles[key]) != 0:
            q = abs(sum([cmath.exp(n*1j*theta) for theta in angles[key]]) / len(angles[key]))
            q_j += [q]
        else:
            q_j += [0]
    
    
    if len(q_j) != num: 
        print('something may not be right.... check for 0 ctcs!')

    q6 = sum(q_j) / len(q_j)


    with open(f"{name}/bond_order_{n}/bond_order_{step}", 'a') as f: 
        f.write('average: ' + str(q6) + '\n')
        for i in range(len(q_j)): 
            f.write(f"{i+1}: {q_j[i]}\n")

    return q6 # i hope! 



def get_alignments(name, step): 
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step)

    pre.readState(bodies, f"{name}/OUTBOX", step)
    
    aligns = []
    for b in bodies: 
        rot = b.nodes[1].dof.rot
        theta = np.arcsin(rot[1][0])
        check = np.arccos(rot[0][0])
        if theta != check and theta != -check: 
            print('uhoh! thats weird.')
        aligns.append(theta)
    
    return aligns


    