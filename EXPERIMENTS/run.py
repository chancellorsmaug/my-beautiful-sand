import os, math
from experiment import gen_sample_settling
import network, dundunduhhh.processing.coord_num as coord_num, general, command
from compression_shear import gen_sample_compression, gen_sample_shear


experiment_name = "clean/no_magnets"
size = [2.5, 3.]

def build_folders(experiment_name, adj):
    if os.path.isdir('./'+experiment_name+'/'):
        print("directory found")
    else:
        os.mkdir('./'+experiment_name+'/')
    
    if os.path.isdir('./'+experiment_name+adj+'/'):
        print("directory found")
    else:
        os.mkdir('./'+experiment_name+adj+'/')
        

    if os.path.isdir('./'+experiment_name+adj+'_compression/'):
        print("directory found")
    else:
        os.mkdir('./'+experiment_name+adj+'_compression/')
        # os.mkdir('./'+experiment_name+'_compression/'+adj+'/')

    if os.path.isdir('./'+experiment_name+adj+'_shearing/'):
        print("directory found")
    
    else:
        os.mkdir('./'+experiment_name+adj+'_shearing/')
        # os.mkdir('./'+experiment_name+'_shearing/'+adj+'/')

def write_log(name, msg): 
    with open('log.txt', 'a') as f: 
        f.write(f"{name}: {msg}\n")

def get_info(iter, name:str): 
    network.get_graph(iter=iter, name=f"{name}")
    coord_num.get_coord_num(bodies=f"{name}/DATBOX/BODIES.DAT", iter=iter, grain_colour='grain', experiment=name, wall_colour='walls')
    general.get_approx_packing_frac(name=name, step=iter)


def run_experiment(exp, shape, verts, prop, fric, num, field):
    gen_sample_settling(name=exp, numgrains=num, shape=shape, size_range=size, 
                       proportion=prop, vertices=verts, ly=200, fric=fric)
    # on teste la presence de DATBOX
    if os.path.isdir('./'+exp+'/DATBOX'): # just checking
        print("datbox found")
    command.write_bulk_behav_MAG(name=exp, b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
    try:
        command.command(name=exp, time=5., num_files=40)
        write_log(name=exp, msg='success')
    except:
        write_log(name=exp, msg='fail')
        pass

    # 
    total_grain_volume = general.get_grains_volume(name=exp, step=1)
    with open(f"{exp}/init_grain_vol", 'w') as ini: 
        ini.write(str(total_grain_volume))

    # compression 
    write_log(f"compression", msg='start')
    gen_sample_compression(name=exp, size_range=size, step=40) # step = num_files
    command.write_bulk_behav_MAG(name=exp+'_compression', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
    try:
        command.command(name=exp+'_compression', time=8., num_files=80)
        write_log(name=exp+'_compression', msg='success')
    except:
        write_log(name=exp+'_compression', msg='fail')
        pass
    # on teste la presence de DATBOX
    if os.path.isdir('./'+exp+'_compression/DATBOX'):
        print("compression datbox found")
    
    # # shearing
    # write_log(f"shear", msg='start')
    # gen_sample_shear(name=exp, step=40) # step = num_files
    # command.write_bulk_behav_MAG(name=exp+'_shearing', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
    # try:
    #     command.command(name=exp+'_shearing', time=8., num_files=80)
    #     write_log(name=exp+'_shearing', msg='success')
    # except:
    #     write_log(name=exp+'_shearing', msg='success')
    #     pass
    # # on teste la presence de DATBOX
    # if os.path.isdir('./'+exp+'_shearing/DATBOX'):
    #     print("shearing datbox found")


shapes = [7,6,5,4,3,0]
# shapes.remove(1)
# shapes.remove(2)
# shapes.remove(0)

get = [2, 8, 15, 27, 38, 45, 57, 68, 75]
# get = [27]

disk = math.pi

polyg = [0.5*vert*math.sin(2*math.pi/vert) for vert in shapes if vert != 0]

ratio = [p/disk for p in polyg] + [1]

num = [int(300//r) for r in ratio]

# total_grain_volume = general.get_grains_volume(name="basic_polygonsdisk0", step=1)
# with open("basic_polygonsdisk0/init_grain_vol", 'w') as ini: 
#         ini.write(str(total_grain_volume))

# shapes = [0]

fric = [ .5, 0. ]
prop = [ .5, 0. ]

print(num)

# run_experiment(exp="no_magnets_polyg7/fric4_prop5",shape='polyg', verts=7, prop=0.5, fric=0.4, num=num[0],
#                            field=[' 0.0000000e+00', ' 0.0000000e+00'])


# for i, s in enumerate(shapes): 
#     name = 'disk' if s==0 else 'polyg'
#     write_log(name=f"{name}{s}", msg='start')
#     for f in fric: 
#         for p in prop: 
#             adj = f"/fric{int(f*10)}_prop{int(p*10)}"
#             write_log(f"{adj}", msg='start')
#             build_folders(experiment_name+f"_{name}{s}",adj)
#             run_experiment(exp=experiment_name+f"_{name}{s}"+adj, shape=name, verts=s, prop=p, fric=f, num=num[i],
#                            field=[' 0.0000000e+00', ' 0.0000000e+00'])
#             for g in get: 
#                 if os.path.isdir(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
#                     get_info(iter=g, name=experiment_name+f"_{name}{s}"+adj)
#                 if os.path.isdir(experiment_name+f"_{name}{s}"+adj+f"_compression/OUTBOX/Vloc_Rloc.OUT.{g}"):
#                     get_info(iter=g, name=experiment_name+f"_{name}{s}"+adj+"_compression")
#                 # if os.path.isdir(experiment_name+f"_{name}{s}"+adj+f"_shearing/OUTBOX/Vloc_Rloc.OUT.{g}"):
#                 #     get_info(iter=g, name=experiment_name+f"_{name}{s}"+adj+"_shearing")

                

# get_info(31, "no_magnets_polyg7/fric4_prop5_shearing")


def run_normal(exp, shape, verts, prop, fric, num, field):
    
    # on teste la presence de DATBOX
    if os.path.isdir('./'+exp+'/DATBOX'): # just checking
        
        print("datbox found")
        write_log(exp, 'skipped, datbox found')
    else:
        gen_sample_settling(name=exp, numgrains=num, shape=shape, size_range=size, 
                       proportion=prop, vertices=verts, ly=200, fric=fric)
        command.write_bulk_behav_MAG(name=exp, b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
        try:
            command.command(name=exp, time=5., num_files=40)
            write_log(name=exp, msg='success')
        except:
            write_log(name=exp, msg='fail')
            pass

    # 
        total_grain_volume = general.get_grains_volume(name=exp, step=1)
        with open(f"{exp}/init_grain_vol", 'w') as ini: 
            ini.write(str(total_grain_volume))



# # compression 
# def run_comp(exp,  field):
#     write_log(f"compression", msg='start')
#     if os.path.isdir('./'+exp+'/DATBOX'): # just checking
#         print("datbox found")
#     gen_sample_compression(name=exp, size_range=size, step=40) # step = num_files
#     command.write_bulk_behav_MAG(name=exp+'_compression', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
#     try:
#         command.command(name=exp+'_compression', time=8., num_files=80)
#         write_log(name=exp+'_compression', msg='success')
#     except:
#         write_log(name=exp+'_compression', msg='fail')
#         pass
#     # on teste la presence de DATBOX
#     if os.path.isdir('./'+exp+'_compression/DATBOX'):
#         print("compression datbox found")

def run_comp(exp,  field):
    write_log(f"compression", msg='start')
    if os.path.isdir('./'+exp+'_compression/DATBOX'):
        write_log(exp, 'skipped, datbox found')
    else:
        gen_sample_compression(name=exp, size_range=size, step=40) # step = num_files
        command.write_bulk_behav_MAG(name=exp+'_compression', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
        try:
            command.command(name=exp+'_compression', time=8., num_files=80)
            write_log(name=exp+'_compression', msg='success')
        except:
            write_log(name=exp+'_compression', msg='fail')
            pass
    # # on teste la presence de DATBOX
    # if os.path.isdir('./'+exp+'/DATBOX'):
    #     print("compression datbox found")

    # shearing
def run_shear(exp, field):
    write_log(f"shear", msg='start')
    if os.path.isdir('./'+exp+'_shearing/DATBOX'):
        write_log(exp, 'skipped, datbox found')
    else:
        # right_grain = general.get_right(name=exp, step=40)
        gen_sample_shear(name=exp, step=40) # step = num_files
        command.write_bulk_behav_MAG(name=exp+'_shearing', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
        try:
            command.command(name=exp+'_shearing', time=8., num_files=80)
            write_log(name=exp+'_shearing', msg='success')
        except:
            write_log(name=exp+'_shearing', msg='success')
            pass
    # on teste la presence de DATBOX
    # if os.path.isdir('./'+exp+'/DATBOX'):
    #     print("shearing datbox found")


# for i,s in enumerate(shapes): 
#     name = 'disk' if s==0 else 'polyg'
#     if s in [4,3,0]:
#         write_log(name=f"{name}{s}", msg='start')
#         for f in fric: 
#             if s==3 or s==0 or (s==4 and f==.2):
#                 for p in prop: 
#                     adj = f"/fric{int(f*10)}_prop{int(p*10)}"
#                     write_log(f"{adj}", msg='start')
#                     build_folders(experiment_name+f"_{name}{s}",adj)
#                     run_normal(exp=experiment_name+f"_{name}{s}"+adj, shape=name, verts=s, prop=p, fric=f, num=num[i],
#                                 field=[' 0.0000000e+00', ' 0.0000000e+00'])
#                     for g in get: 
#                         if os.path.isdir(experiment_name+f"_{name}{s}"+adj+f"/OUTBOX/Vloc_Rloc.OUT.{g}"):
#                             get_info(iter=g, name=experiment_name+f"_{name}{s}"+adj)



for i,s in enumerate(shapes): 
    name = 'disk' if s==0 else 'polyg'
    write_log(name=f"{name}{s}", msg='start')
    for f in fric: 
        for p in prop: 
            adj = f"/fric{int(f*10)}_prop{int(p*10)}"
            build_folders(experiment_name+f"_{name}{s}",adj)
            write_log(f"{adj}", msg='start')
            # if s == 0: 
            # write_log(name=f"{name}{s}", msg='re-run')
            run_normal(exp=experiment_name+f"_{name}{s}"+adj, shape=name, verts=s, prop=p, fric=f, num=num[i],
                        field=[' 0.0000000e+00', ' 0.0000000e+00'])
            run_comp(exp=experiment_name+f"_{name}{s}"+adj, 
                           field=[' 0.0000000e+00', ' 0.0000000e+00'])
            # write_log(name=f"{name}{s} shearing", msg='start')
            # run_shear(exp=experiment_name+f"_{name}{s}"+adj, 
            #                field=[' 0.0000000e+00', ' 0.0000000e+05'])



