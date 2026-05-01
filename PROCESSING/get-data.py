
import network, dundunduhhh.processing.coord_num as coord_num, general, order
from dundunduhhh.PROCESSING import distributions as dist
import numpy as np 
import os


def get_info(iter, name:str, d): 
    network.get_graph(iter=iter, name=f"{name}")
    coord_num.get_coord_num(bodies=f"{name}/DATBOX/BODIES.DAT", iter=iter, grain_colour='grain', experiment=name, wall_colour='walls')
    general.get_approx_packing_frac(name=name, step=iter)
    print('first half done')
    order.get_q6( name=name, step=iter)
    order.get_qn( name=name, step=iter, n=4)
    dist.get_force_graph(path=name, step=iter)
    dists, num_grains = order.get_dists(name=name, step=iter)
    print(dists)
    dist.get_rdf_graph2(path=name, step=iter, d=d, bin=0.5, dists2=dists, num_grains=num_grains) # fix this obv

def write_log(name, msg): 
    with open('data_log.txt', 'a') as f: 
        f.write(f"{name}: {msg}\n")


get = np.arange(1, 80, 5).tolist()
print(get[0], get[1], get[5])

shapes = [6,5,4,3,0]
fric = [ .5, 0.]
prop = [0.5, 0.]

experiment_name = "clean/no_magnets"

# get = [1]

def build(n,a):
    d=n+a
    place = ['/networks/', '/coord_num/', '/phi/', '/bond_order/', '/bond_order_4/', '/force_dist/', '/rdf/']
    for i in range(5):
        if not os.path.isdir(d+place[i]):
            os.mkdir(d+place[i])
    if not os.path.isdir('graphs/'+n): 
        os.mkdir('graphs/'+n)
    if not os.path.isdir('graphs/'+d): 
        os.mkdir('graphs/'+d)
    if not os.path.isdir('graphs/'+d+place[5]): 
        os.mkdir('graphs/'+d+place[5])
    if not os.path.isdir('graphs/'+d+place[6]): 
        os.mkdir('graphs/'+d+place[6])
    
# shapes = [4]
# fric=[.7]
# prop=[0]

# for s in shapes: 
#     name = 'disk' if s==0 else 'polyg'
#     write_log(name=f"{name}{s}", msg='get data start')
#     for f in fric: 
#         for p in prop: 
#             adj = f"/fric{int(f*10)}_prop{int(p*10)}"
#             build(n=experiment_name+f"_{name}{s}", a= adj)
#             for g in get: 
#                 # print('getting...', g)
#                 # print(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}")
#                 if os.path.isfile(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
#                     # print('found!')
#                     get_info(iter=g, name=experiment_name+f"_{name}{s}"+adj)
#                 else:
#                     write_log(name = f"{s},{f},{p},{g}", msg='not found :(')
#     write_log(name=f"{name}{s}", msg='got data!')

for s in shapes: 
    name = 'disk' if s==0 else 'polyg'
    write_log(name=f"{name}{s}", msg='get data start')
    if s==0: 
        d=6.
    else: 
        d = 6.*np.sin(np.pi / s)
    for f in fric: 
        for p in prop: 
            adj = f"/fric{int(f*10)}_prop{int(p*10)}"
            build(n=experiment_name+f"_{name}{s}", a= adj)
            for g in get: 
                # print('getting...', g)
                # print(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}")
                if os.path.isfile(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
                    # print('found!')
                    # print(experiment_name+f"_{name}{s}"+adj)
                    get_info(iter=g, name=experiment_name+f"_{name}{s}"+adj, d=d)
                else:
                    write_log(name = f"{s},{f},{p},{g}", msg='not found :(')
            adjcomp = f"/fric{int(f*10)}_prop{int(p*10)}_compression"
            build(n=experiment_name+f"_{name}{s}", a= adjcomp)
            for g in get: 
                if os.path.isfile(experiment_name+f"_{name}{s}"+adjcomp+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
                    get_info(iter=g, name=experiment_name+f"_{name}{s}"+adjcomp, d=d)
                else:
                    write_log(name = f"{s},{f},{p},{g} comp", msg='not found :(')
            adjshear = f"/fric{int(f*10)}_prop{int(p*10)}_shearing"
            build(n=experiment_name+f"_{name}{s}", a= adjshear)
            for g in get: 
                if os.path.isfile(experiment_name+f"_{name}{s}"+adjshear+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
                    get_info(iter=g, name=experiment_name+f"_{name}{s}"+adjshear, d=d)
                else:
                    write_log(name = f"{s},{f},{p},{g} shear", msg='not found :(')
    write_log(name=f"{name}{s}", msg='got data!')
