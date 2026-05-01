# import network, coord_num, general, order
from dundunduhhh.PROCESSING import distributions as dist
import numpy as np 
import os

def write_log(name, msg): 
    with open('update_log.txt', 'a') as f: 
        f.write(f"{name}: {msg}\n")

# experiment_name = "clean/no_magnets"
# shapes = [7,6,5,4,3,0]
# fric = [.5, 0.] # , .2, .7, 0.
# prop = [0.5, 0.]
# get = np.arange(26, 80, 5).tolist()

# for s in shapes: 
#     name = 'disk' if s==0 else 'polyg'
#     write_log(name=f"{name}{s}", msg='get data start')
#     if s==0: 
#         d=6.
#     else: 
#         d = 6.*np.sin(np.pi / s)
#     for f in fric: 
#         for p in prop: 
#             adj = f"/fric{int(f*10)}_prop{int(p*10)}_compression"
#             # build(n=experiment_name+f"_{name}{s}", a= adj) # should all exist 
#             for g in get: 
#                 # print('getting...', g)
#                 # print(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}")
#                 if os.path.isfile(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
#                     # print('found!')
#                     # order.get_q6(name=experiment_name+f"_{name}{s}"+adj, step=g)
#                     # general.get_approx_packing_frac(name=experiment_name+f"_{name}{s}"+adj, step=g)
#                     # dists, num_grains = order.get_dists(name=experiment_name+f"_{name}{s}"+adj, step=g)
#                     # print(dists)
#                     # dist.get_rdf_graph2(path=experiment_name+f"_{name}{s}"+adj, step=g, d=d, bin=0.5, dists2=dists, num_grains=num_grains)
#                     # network.get_graph(iter = g, name = experiment_name+f"_{name}{s}"+adj)
#                     dist.get_force_graph(path=experiment_name+f"_{name}{s}"+adj, step=g)
#                 else:
#                     write_log(name = f"{s},{f},{p},{g}", msg='not found :(')
#     write_log(name=f"{name}{s}", msg='got data!')



exp = 'last_magnetic'

shapes = {'disk': 0, 'triangle': 3, 'square': 4, 'needle': 6}

fric = 0.5
prop = 0.
size_range = [5., 10.]

num_grains = {'disk':50, 'triangle':75,'square': 65,'needle': 70}

qm = [ 1e+4, 5e+4, 4e+4, 6e+4, 7e+4, 8e+4]
field = [' 0.0000000e+00',' 0.0000000e+00']

get = np.arange(26, 80, 5).tolist()

for shape in shapes: 
    verts = shapes[shape]
    if shape != 'square':
        sq = None
    else: 
        sq = 'bar' # or 'alt'
    for q in qm:    
        adj =  f"/{shape}{int(q)}_magnetic"
        # build_folders(experiment_name=exp, adj=adj)
        if os.path.isdir('./'+exp+adj+'/DATBOX'): # just checking
            print("datbox found")
            # write_log(adj, 'skipped, datbox found')
        # else:
        for g in get: 
#                 # print('getting...', g)
#                 # print(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}")
            if os.path.isfile(exp+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
#             
                dist.alignment_graph(exp+adj, step=g)
                # gen_sample_settling(name=exp+adj, numgrains=num_grains[shape], shape=shape, size_range=size_range, 
                                    # proportion=prop, vertices=verts, ly=110., fric=fric, type=sq, qm=q)
                write_log(adj, 'made')
                # command.write_bulk_behav_MAG(name=exp+adj, b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
                # command.command(name=exp+adj, time=2., num_files=40)
                # add_magnets(exp+adj, step=40, qm=q)
                # command.write_bulk_behav_MAG(name=exp+adj+'_magnetic', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
                # command.command(name=exp+adj+'_magnetic', time=4., num_files=40)
                # write_log(name=adj, msg='success')
                # write_log(name=exp, msg='fail')
