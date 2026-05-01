import math, random
import numpy as np 
from pylmgc90 import pre
import general as gr

def gen_sample_settling(name: str, numgrains: int, shape:str, size_range: list, proportion: float, 
                        vertices:int, ly:float, fric:float):
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

    # grains

    radii = pre.granulo_TwoSizesNumber(nb=numgrains, r_min=size_range[0], 
                                       r_max=size_range[1], p_min=proportion)
    
    particles_keep, coords, dradii = pre.depositInBox2D(radii, ly=ly, lx=lx)
    if shape == 'disk': 
        gr.disk_grains(bodies=bodies, model=mod, material=grains, 
                    dradii=dradii, coords=coords)
    elif shape == 'polyg': 
        gr.polyg_grains(bodies=bodies, vertices=vertices, model=mod, 
                     material=grains, dradii=dradii, coords=coords)
    elif shape == 'needle': 
        gr.needle_grains(bodies=bodies, vertices=vertices, model=mod, 
                     material=grains, dradii=dradii, coords=coords)
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

    pre.writeDatbox(dim=2, mats=mats, mods=mods, bodies=bodies, tacts=tacts, sees=svs, post=post, datbox_path=f"{name}/DATBOX")

    print('complete')
