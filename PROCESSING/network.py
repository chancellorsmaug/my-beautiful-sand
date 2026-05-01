import networkx as nx
import matplotlib.pyplot as plt
import re, math, os
from general import get_wall_ids

# test this on a small case!! 

gr2gr=re.compile('gr2gr')

def add_edge_to_graph(G, e1, e2, w):
    G.add_edge(e1, e2, weight=w)

def extract_connections(vlocrloc: str): 
    string = re.compile('RBDY2\b*')
    ctacts = []
    with open(vlocrloc, 'rt') as file:
        for line in file: 
            if gr2gr.search(line) != None: # only inter grain contacts
                if string.search(line) != None: 
                    split = re.split(string, line)
                    if len(split) != 3: 
                        print('Incorrect pull! Check file: ', vlocrloc, ' line ', line)
                    else: 
                        ctacts.append((split[1][:7], split[2][:7]))
    ctacts0 = [(int(a), int(b)) for (a, b) in ctacts]
    return ctacts0

def extract_force(vlocrloc: str): 
    string = re.compile('rln/H')
    weights = []
    with open(vlocrloc, 'rt') as file: 
        lines = file.readlines()
        for i, line in enumerate(lines):
            if gr2gr.search(line) != None:
                if string.search(lines[i+1]) != None: 
                    split = re.split(string, lines[i+1])
                    if len(split) != 2: 
                        print('Incorrect pull! Check file: ', vlocrloc, ' line ', lines[i+1])
                    else: 
                        weights.append(float(split[1][:14].replace('D', 'e'))) # first 14 char. 
                else: 
                    print('Could not find force in line', lines[i+1])
    return weights

def extract_disp(dof: str): 
    #for this, need to extract the BODY NUMBER from rbdy2, and the corresponding coords X(1), X(2).
    bdy = re.compile('RBDY2\b*')
    node = re.compile('X...=')
    keys=[]
    points = []
    with open(dof, 'rt') as file: 
        lines = file.readlines()
        for i, line in enumerate(lines): 
            if bdy.search(line) != None: 
                bdy_num = re.split(bdy, line)
                if len(bdy_num) != 2: 
                    print('Incorrect pull! check file ', dof, ' line ', line)
                else: 
                    keys.append(int(bdy_num[-1]))
                if node.search(lines[i+2]) != None: 
                    xyz = re.split(node, lines[i+2])
                    if len(xyz) != 4: 
                        print('Incorrect pull! check file ', dof, ' line ', lines[i+2])
                    else: 
                        x = xyz[1][:14].replace('D', 'e')
                        y = xyz[2][:14].replace('D', 'e')
                        points.append((float(x), float(y)))
                else:
                    print('Could not find coordinates in line', lines[i+2])
    coords = {key: point for key, point in zip(keys, points)}
    return coords

def extract_init_coords(bodies:str): 
    bdy = re.compile('RBDY2\b*')
    node = re.compile('coo.=')
    keys=[]
    points = []
    with open(bodies, 'rt') as file: 
        lines = file.readlines()
        for i, line in enumerate(lines): 
            if bdy.search(line) != None: 
                bdy_num = re.split(bdy, line)
                if len(bdy_num) != 2: 
                    print('Incorrect pull! check file ', bodies, ' line ', line)
                else: 
                    keys.append(int(bdy_num[-1]))
                if node.search(lines[i+4]) != None: 
                    xyz = re.split(node, lines[i+4])
                    if len(xyz) != 4: 
                        print('Incorrect pull! check file ', bodies, ' line ', lines[i+4])
                    else: 
                        x = xyz[1][:14].replace('D', 'e')
                        y = xyz[2][:14].replace('D', 'e')
                        points.append((float(x), float(y)))
                else:
                    print('Could not find coordinates in line',i+4, lines[i+4])
    coords = {key: point for key, point in zip(keys, points)}
    return coords

import order
from pylmgc90 import pre

def get_graph(iter:int, name:str):

    G = nx.Graph()

    vlocrloc = f"OUTBOX/Vloc_Rloc.OUT.{iter}"
    dof=f"OUTBOX/DOF.OUT.{iter}"
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=iter)

    pre.readState(bodies, f"{name}/OUTBOX", iter)

    edges = extract_connections(name+'/'+vlocrloc)
    weights = extract_force(name+'/'+vlocrloc)
    # change = extract_disp(name+'/'+dof)
    # init = extract_init_coords(name+'/'+bodies)
    
    coords, num = order.get_coor(bodies)
    # print(init)

    walls, num_walls = get_wall_ids(name=name, step=iter)

    # coords={}
    # for key in change: 
    #     coords[key] = (change[key][0] + init[key][0], change[key][1] + init[key][1])

    

    nodes = [key for key in coords]
    if len(nodes) != num: 
        print('somethign suspicious!')
    # print(coords)
    draw_nodes = []
    for node in nodes: 
        if node not in walls: 
            draw_nodes.append(node)
        else: 
            print('excluded', node)

    G.add_nodes_from(nodes)

    # if len(weights) != 0: 
    #     average_force = sum(weights) / len(weights)
    # else: 
    #     average_force = 0. 
    
    # if average_force == 0.: 
    #     magnitude = 0
    # else:
    #     magnitude = math.floor(math.log10(average_force))

    if len(weights) != 0: 
        # max_force = max(weights)
        average_force = sum(weights) / len(weights)
        if average_force != 0.:
            magnitude = math.floor(math.log10(average_force))
        else: 
            magnitude = 0.
    else: 
        average_force = 0.
        magnitude = 0.

    scaled = [0.5*weight*10**(-magnitude) for weight in weights]
    colour = ['r' if weight>=average_force else 'g' for weight in weights]
    for i in range(len(edges)):
        G.add_edge(nodes[edges[i][0]-1], nodes[edges[i][1]-1], weight=scaled[i], colour=colour[i]) # note -1, since indexing counts from 0 not 1
        

    print(G.number_of_nodes())
    print(G.number_of_edges())

    # print(scaled[0], scaled[len(scaled)//2], scaled[-1])
    # print(colour[0], colour[len(colour)//2], colour[-1])
    print(average_force)
    print(magnitude)
    print(len(weights), len(scaled), len(colour))


    # # add axis
    fig, ax = plt.subplots()
    forces = nx.get_edge_attributes(G, 'weight').values()
    split = nx.get_edge_attributes(G, 'colour').values()
    # nx.draw(G, pos=coords, ax=ax, width=list(forces), edge_color=list(split), node_size=1.)

    nx.draw_networkx_nodes(G, pos=coords, ax=ax, nodelist=draw_nodes, node_size=1.)
    nx.draw_networkx_edges(G, pos=coords, width=list(forces), edge_color=list(split))

    ax.set_xlabel(f"Average force: {average_force}")

    plt.axis("on")
    # ax.set_xlim(0, 11)
    # ax.set_ylim(0,11)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.savefig(f"{name}/networks/graph_{iter}.png")

    path = f"{name}/forces_{iter}.txt"
    with open(path, 'a') as forces: 
        for i, w in enumerate(weights): 
            forces.write(f"{i}, {w}\n")

    # plt.show()

# fix to draw only nodes that arent walls (draw nodes fn?)