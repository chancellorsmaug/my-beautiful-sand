import math, random, os
import numpy as np 
from pylmgc90 import pre
import general as gr
import command
from compression_shear import gen_sample_shear

def gen_sample_settling(name: str, numgrains: int, shape:str, size_range: list, proportion: float, 
                        vertices:int, ly:float, fric:float, type:str, qm:float):
    # pre.setStopMode('pass')

    bodies = pre.avatars()

    #   * models
    mods = pre.models()
    #   * materials
    mats = pre.materials()
    #   * visibility
    svs  = pre.see_tables()
    #   * contact laws
    tacts = pre.tact_behavs()

    mod = pre.model(name='rigid', physics='MECAx', element='Rxx2D', dimension=2)
    mods.addModel(mod)

    grains = pre.material(name='grain',materialType='RIGID',density=10.)
    wall = pre.material(name='walls', materialType='RIGID', density=300.)
    mats.addMaterial(grains)
    mats.addMaterial(wall)

    # box 

    lx = 110.

    bottom   = pre.smoothWall(center=[25.-2*lx, -5.], theta=0.0, l=6*lx,
                        h=5., nb_polyg=12, model=mod, material=wall, color='WALLx')
    bottom.imposeDrivenDof(component=[1,2,3], dofty='vlocy')
    bodies.addAvatar(bottom)
    left   = pre.smoothWall(center=[-5, 50.], theta=-0.5*np.pi, l=1.5*lx,
                        h=5., nb_polyg=12, model=mod, material=wall, color='WALLx')
    left.imposeDrivenDof(component=[1,2,3], dofty='vlocy')
    # left.imposeDrivenDof(component = 1, dofty = 'force', ct = 5000.)
    bodies.addAvatar(left)
    right   = pre.smoothWall(center=[lx + 5., 50.], theta=0.5*np.pi, l=1.5*lx,
                        h=5., nb_polyg=12, model=mod, material=wall, color='WALLx')
    right.imposeDrivenDof(component=[1,2,3], dofty='vlocy')
    # right.imposeDrivenDof(component = 1, dofty = 'force', ct = 5000.)
    bodies.addAvatar(right)
    lid = pre.smoothWall(center=[50., lx + 5.], theta=0.0, l=1.5*110.,
                         h=5., nb_polyg=12, model=mod, material= wall, color='WALLx') 
    lid.imposeDrivenDof(component=[1,2], dofty='vlocy') 
    bodies.addAvatar(lid)


    # grains

    radii = pre.granulo_TwoSizesNumber(nb=numgrains, r_min=size_range[0], 
                                       r_max=size_range[1], p_min=proportion)
    
    particles_keep, coords, dradii = pre.depositInBox2D(radii, ly=ly, lx=lx)
    if shape == 'disk': 
        gr.disk_grains_mag(bodies=bodies, model=mod, material=grains, 
                    dradii=dradii, coords=coords, dx = 7.)
    elif shape == 'triangle': 
        # if vertices == 3:
            gr.triangle_grains_mag(bodies=bodies, vertices=vertices, model=mod, 
                        material=grains, dradii=dradii, coords=coords, dx = 6.) # worried about narrow corners
    elif shape == 'square': 
            gr.square_grains_mag(bodies=bodies,vertices=vertices, model=mod, material=grains, 
                        dradii=dradii, coords=coords, dx = 7., type=type)
        # else: 
            print(f"Polyg {vertices} not supported for magnets! No grains added.")
    elif shape == 'needle': 
        gr.needle_grains_mag(bodies=bodies, vertices=vertices, model=mod, material=grains, 
                             dradii=dradii, coords=coords, dx = 7.)
    else: 
        print(f"Shape {shape} not supported! No grains added.")

    # interactions

    contact = pre.tact_behav(name='gr2gr', law='IQS_CLB', fric=fric)
    tacts += contact
    wall_contact = pre.tact_behav(name='gr2wl', law='IQS_CLB', fric=0.9)
    tacts += wall_contact

    vis1 = pre.see_table(CorpsCandidat='RBDY2', candidat='POLYG', colorCandidat='grain',
                       CorpsAntagoniste='RBDY2', antagoniste='POLYG', colorAntagoniste='grain',
                       behav = contact, alert = 0.05)
    svs += vis1
    vis2 = pre.see_table(CorpsCandidat='RBDY2', candidat='POLYG', colorCandidat='grain',
                       CorpsAntagoniste='RBDY2', antagoniste='POLYG', colorAntagoniste='WALLx',
                       behav = wall_contact, alert = 0.05)
    svs += vis2
    vis3 = pre.see_table(CorpsCandidat='RBDY2', candidat='DISKx', colorCandidat='grain',
                       CorpsAntagoniste='RBDY2', antagoniste='DISKx', colorAntagoniste='grain',
                       behav = contact, alert = 0.05)
    svs += vis3
    vis4 = pre.see_table(CorpsCandidat='RBDY2', candidat='DISKx', colorCandidat='grain',
                       CorpsAntagoniste='RBDY2', antagoniste='POLYG', colorAntagoniste='WALLx',
                       behav = wall_contact, alert = 0.05)
    svs += vis4

    # BASIC POSTPRO

    post = pre.postpro_commands()
    basic = pre.postpro_command(name='SOLVER INFORMATIONS', step=10)
    post.addCommand(basic)

    pre.writeDatbox(dim=2, mats=mats, mods=mods, bodies=bodies, tacts=tacts, sees=svs, post=post, datbox_path=f"{name}/DATBOX", gravy=[0,0,0])

    print('complete')

def build_folders(experiment_name, adj):
    if os.path.isdir('./'+experiment_name+'/'):
        print("directory found")
    else:
        os.mkdir('./'+experiment_name+'/')
    
    if os.path.isdir('./'+experiment_name+adj+'/'):
        print("directory found")
    else:
        os.mkdir('./'+experiment_name+adj+'/')
        

    if os.path.isdir('./'+experiment_name+adj+'_magnetic/'):
        print("directory found")
    else:
        os.mkdir('./'+experiment_name+adj+'_magnetic/')
        # os.mkdir('./'+experiment_name+'_compression/'+adj+'/')

    if os.path.isdir('./'+experiment_name+adj+'_shearing/'):
        print("directory found")
    
    else:
        os.mkdir('./'+experiment_name+adj+'_shearing/')
        # os.mkdir('./'+experiment_name+'_shearing/'+adj+'/')

def write_log(name, msg): 
    with open('mag_log.txt', 'a') as f: 
        f.write(f"{name}: {msg}\n")

def add_magnets(name, step, qm): 

    
    mats, mods, bodies, tacts, svs, inters = pre.readDatbox(dim=2, datbox_path=f"{name}/OUTBOX", step=step) # _compression 

    pre.readState(bodies, f"{name}/OUTBOX", step)


        # MAGNETIC INTERACTIONS

    offset = 6. # can 'see' only grains nearest itself. 

    attract = pre.tact_behav(name='opose', law='MAGNETIC_MP_ATTRACT', fric=0.3, Qm=qm)
    tacts += attract        

    vis_elem_NS = pre.see_table(CorpsCandidat='RBDY2', candidat='DISKx', colorCandidat='NORTH',
                       CorpsAntagoniste='RBDY2', antagoniste='DISKx', colorAntagoniste='SOUTH',
                       behav = attract, alert = offset) 

    svs += vis_elem_NS

    repell = pre.tact_behav(name='match', law='MAGNETIC_MP_REPELL', fric=0.4, Qm=qm)
    tacts += repell

    vis_elem_NN = pre.see_table(CorpsCandidat='RBDY2', candidat='DISKx', colorCandidat='NORTH',
                        CorpsAntagoniste='RBDY2', antagoniste='DISKx', colorAntagoniste='NORTH',
                        behav = repell, alert = offset) 

    svs += vis_elem_NN

    vis_elem_SS = pre.see_table(CorpsCandidat='RBDY2', candidat='DISKx', colorCandidat='SOUTH',
                        CorpsAntagoniste='RBDY2', antagoniste='DISKx', colorAntagoniste='SOUTH',
                        behav = repell, alert = offset) 

    svs += vis_elem_SS

    post = pre.postpro_commands()
    basic = pre.postpro_command(name='SOLVER INFORMATIONS', step=10)
    post.addCommand(basic)

    pre.writeDatbox(dim=2, mats=mats, mods=mods, bodies=bodies, tacts=tacts, sees=svs, post=post, 
                    datbox_path=f"okay_i_lied/disk40000_field/DATBOX", gravy=[0., 0., 0.]) # no more gravity 

    print('complete')



exp = 'okay_i_lied'

shapes = {'disk':0}

fric = 0.5
prop = 0.
size_range = [5., 10.]

num_grains = {'disk':50, 'triangle':75,'square': 65,'needle': 70}

qm = [4e+4, 5e+4, 6e+4]
field = [' 0.0000000e+00',' 0.0000000e+00']
 
# for shape in shapes: 
#     verts = shapes[shape]
#     if shape != 'square':
#         sq = None
#     else: 
#         sq = 'bar' # or 'alt'
#     for q in qm:    
#         adj =  f"/{shape}{int(q)}"
#         build_folders(experiment_name=exp, adj=adj)
#         if os.path.isdir('./'+exp+adj+'/DATBOX'): # just checking
#             print("datbox found")
#             write_log(adj, 'skipped, datbox found')
#         else:
#             gen_sample_settling(name=exp+adj, numgrains=num_grains[shape], shape=shape, size_range=size_range, 
#                                 proportion=prop, vertices=verts, ly=110., fric=fric, type=sq, qm=q)
#             write_log(adj, 'made')
#             command.write_bulk_behav_MAG(name=exp+adj, b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
#             command.command(name=exp+adj, time=2., num_files=40)
#             add_magnets(exp+adj, step=40, qm=q)
#             command.write_bulk_behav_MAG(name=exp+adj+'_magnetic', b1=field[0], b2=field[1], b3=' 0.0000000e+00') # NOTE FORMATTING!!!
#             command.command(name=exp+adj+'_magnetic', time=4., num_files=40)
#             write_log(name=adj, msg='success')
#             # write_log(name=exp, msg='fail')

 
# shapes = {'disks': 0}
# for shape in shapes: 
#     verts = shapes[shape]
#     if shape != 'square':
#         sq = None
#     else: 
#         sq = 'bar' # or 'alt'
#     for q in qm:    
#         adj =  f"/{shape}{int(q)}"
#         build_folders(experiment_name=exp, adj=adj)
#         if os.path.isdir('./'+exp+adj+'_shearing/DATBOX'): # just checking
#             print("datbox found")
#             write_log(adj, 'skipped, datbox found')
#         else:
#             print(exp+adj+'_magnetic')



add_magnets(name="okay_i_lied/disk40000_magnetic",  step=5, qm=4e+5)
# write_log(adj+' shear', 'made')
command.write_bulk_behav_MAG(name="okay_i_lied/disk40000_field", b1=field[0], b2=' 1.0000000e+06', b3=' 0.0000000e+00') # NOTE FORMATTING!!!
command.command(name="okay_i_lied/disk40000_field", time=5., num_files=40)
# write_log(name=adj + ' shear', msg='success')