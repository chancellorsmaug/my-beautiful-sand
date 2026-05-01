# my-beautiful-sand
Project code to create LMGC90 simulations, and manipulate output data. 


## To run a simulation: 

First, install LMGC90 following the guidance: [[href(https://git-xen.lmgc.univ-montp2.fr/lmgc90/lmgc90_user/-/wikis/download_and_install)]]

A simple 'grains in a box' simulation can be run using the function ```gen_sample_settling()``` from [[EXPERIMENTS/experiment.py]], to build the geometry, followed by ```command()``` from [[EXPERIMENTS/command.py]] to run the solver. 

The parameters for ```gen_sample_settling()``` are: 

```
name: str, # file to save output to
numgrains: int, # number of grains to create
shape:str, # shape of grain, should be 'disk', 'polyg', or 'needle'.
size_range: list, # two possible grain radii
proportion: float, # proportion of small to big grains
vertices:int, # number of vertices for 'polyg' and 'needle' shapes. 
ly:float, # height in which to generate grains. recommended 150.
fric:float # frcition coefficient between grains
```

The parameters for ```command()``` are: 

```
time: float, # time to run simulation for. recommended 2-10 seconds
num_files: int, # number of data files to create. must be positive
name: str # file DATBOX is stored in 
```

Outputs can be visualised using ParaView. Additional compression or shearing experiments can be run using functions in [[EXPERIMENTS/compression_shear.py]], followed by ```command()``` a second time. 

## To get force networks and other output statistics: 

A variety of output statistics can be found using files in [[PROCESSING]], including force networks, distributions, and the coordination number. 

## To add magnetic interaction to LMGC90: 

Edits must be made to the LMGC90 core files. The interaction law can be added following the intructions found here: [[href(https://lmgc90.pages-git-xen.lmgc.univ-montp2.fr/lmgc90_dev/dev_contact_law.html)]], and using the code blocks found in [[LMGC90 Edits]]. The blocks in [[LMGC90 Edits/interaction-law.f90]] describe the force relation, and should be added to the mod_nlgs.f90 file. The blocks in [[LMGC90 Edits/miscillaneous-interaction-law.f90]] should be added to the file indicated in the comments. 

Magnetic force in an external field must be added using the blocks in [[LMGC90 Edits/external-field.f90]]. These should be added most importantly to mod_mecaMAILx.f90 and mod_RBDY2.f90, wherever gravity (```gravy```) is calculated. Other files can also be modified, but notation may be incompatible. 

