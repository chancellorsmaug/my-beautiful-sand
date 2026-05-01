
import re, numpy

def extract_connections_all(vlocrloc: str): 
    string = re.compile('RBDY2\b*')
    ctacts = []
    with open(vlocrloc, 'rt') as file:
        for line in file: 
            if string.search(line) != None: 
                split = re.split(string, line)
                if len(split) != 3: 
                    print('Incorrect pull! Check file: ', vlocrloc, ' line ', line)
                else: 
                    ctacts.append((split[1][:7], split[2][:7]))
    ctacts0 = [(int(a), int(b)) for (a, b) in ctacts]
    return ctacts0


def get_num_grains(bodies: str, mat: str):
    bdy = re.compile('RBDY2\b*')
    matre = re.compile(mat)
    count = 0
    with open(bodies, 'rt') as file:
        lines = file.readlines()
        for i, line in enumerate(lines): 
            if bdy.search(line) != None: 
                bdy_num = re.split(bdy, line)
                if len(bdy_num) != 2: 
                    print('Incorrect pull! check file ', bodies, ' line ', line)
                else: 
                    if matre.search(lines[i+2]) != None: 
                        # print(f"Grain number {bdy_num[-1]}")
                        count += 1
    return count
        
from general import get_wall_ids


def get_coord_num(experiment: str, iter, bodies:str, grain_colour:str, wall_colour:str):
    vlocrloc = f"{experiment}/OUTBOX/Vloc_Rloc.OUT.{iter}"

    connections = extract_connections_all(vlocrloc=vlocrloc)
    num_grains = get_num_grains(bodies, grain_colour)
    wall_ids, num_walls = get_wall_ids(experiment, iter)

    # coord_num = len(connections) / num_grains
    counter = [0 for k in range(num_grains+num_walls)]
    for pair in connections: 
        for i in range(num_grains+num_walls):
            if i+1 in wall_ids:
                counter[i] = 0
            elif pair[0] == i+1: 
                counter[i] += 1
            elif pair[1] == i+1: 
                counter[i] += 1


    av_coord_num = numpy.mean([c for c in counter if c != 0])

    path = f"{experiment}/coord_num/coord_num_{iter}"

    with open(path, 'a') as f:
        overhead = [f"{i+1}, " for i in range(num_grains+num_walls)]
        f.write(str(overhead)+'average\n')
        data = [f"{c}, " for c in counter]
        f.write(str(data)+str(av_coord_num)+'\n')
    
    return av_coord_num