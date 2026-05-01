from pylmgc90 import chipy


def write_bulk_behav_MAG(name:str, b1:str, b2:str, b3:str):
     filename = f"{name}/DATBOX/BULK_BEHAV.DAT"
     lines = ['$field  \n', f"                   mag1={b1}  mag2={b2}  mag3={b3}"]
     if len(lines[1]) != 80: 
          print('Uh oh! Your strings are wrong.')
     with open(filename, 'a') as file: 
        file.writelines(lines)

def command(time: float, num_files: int, name: str):

    chipy.overall_SetWorkingDirectory(name)

    # Initializing
    chipy.Initialize()

    # checking/creating mandatory subfolders
    chipy.checkDirectories()

    # logMes
    # chipy.utilities_DisableLogMes()

    # defining some variables
    # space dimension
    dim = 2

    # modeling hypothesis ( 1 = plain strain, 2 = plain stress, 3 = axi-symmetry)
    mhyp = 1

    # time evolution parameters
    total_time = time
    dt = 1e-3
    nb_steps = int(total_time // dt)
    print('will run for ',nb_steps,' steps')

    # theta integrator parameter  <- what is this?? OKAY this is for crank-nicolson numerical simulation. 
    # 0.5 means the scheme is conservative for smooth evolution problem. obviously want to choose this with intent. 
    theta = 0.5

    # deformable True or False
    deformable = False

    # interaction parameters  <- R_n tolerance  
    Rloc_tol = 5.e-2

    # nlgs parameters  nlgs=non-linear-gauss-seidel. 
    tol = 5e-4 # convergance tolerance
    relax = 1.0 # relaxation param 
    norm = 'Quad ' # three options: quad, QM/16, maxm. used to check convergence. 
    gs_it1 = 50 # max number of convergence checks
    gs_it2 = 200 # number of iterations before convergence check
    solver_type='Stored_Delassus_Loops         '  # <- reportedly efficient in 2d for rigid bodies. 

    # write parameter
    freq_write   = nb_steps // num_files

    # display parameters
    freq_display = freq_write // 2

    itchatche = True

    #
    # read and load  
    #

    # Set space dimension
    chipy.SetDimension(dim,mhyp) # 
    #
    chipy.utilities_logMes('INIT TIME STEPPING')
    chipy.TimeEvolution_SetTimeStep(dt)
    chipy.Integrator_InitTheta(theta)

    # chipy.utilities_logMes('READ DATBOX')
    # chipy.ReadDatbox(deformable=False)

    chipy.utilities_logMes('READ BODIES')
    chipy.ReadBodies()

    chipy.utilities_logMes('READ BEHAVIOURS')
    chipy.ReadBehaviours()

    chipy.LoadTactors()
    chipy.LoadBehaviours()
    # THERMO RIGID 
    chipy.ReadModels()

    chipy.ReadDrivenDof()

    chipy.utilities_logMes('READ INI Vloc Rloc')
    chipy.ReadIni()

    chipy.utilities_logMes('WRITE BODIES')
    chipy.WriteBodies()

    chipy.utilities_logMes('WRITE BEHAVIOURS')  
    chipy.WriteBehaviours()

    chipy.utilities_logMes('WRITE DRIVEN DOF')
    chipy.WriteDrivenDof()


    # shearing bcs 
    # if right != None: 
    #     chipy.RBDY2_SetBodiesInvisible([2,3]) # vertical walls removed. this is body ID not index.
    #     chipy.SetPeriodicCondition(xperiod=right+.5) # periodic BCs instead
    #     print('set period: ', right )



    #
    # open display & postpro
    #

    chipy.utilities_logMes('DISPLAY & WRITE')
    chipy.OpenDisplayFiles()
    chipy.OpenPostproFiles()

    #
    # simulation part ...
    #

    # since constant compute elementary mass once
    chipy.utilities_logMes('COMPUTE MASS')
    chipy.ComputeMass()


    for k in range(nb_steps):
        if k%50 == 0:
                print( f"computing step {k}" )
        #
        chipy.utilities_logMes('INCREMENT STEP')
        chipy.utilities_EnableLogMes()
        chipy.IncrementStep()
        chipy.utilities_DisableLogMes()

        chipy.utilities_logMes('COMPUTE Fext')
        chipy.ComputeFext()                   # external force
        chipy.utilities_logMes('COMPUTE Fint')
        chipy.ComputeBulk()                   # rigidity and internal force info for all bodies
        chipy.utilities_logMes('COMPUTE Free Vlocy')
        chipy.ComputeFreeVelocity()           # velocity when no interactions detected (also interactions are computed)

        chipy.utilities_logMes('RESOLUTION' )
        chipy.RecupRloc(Rloc_tol)             # get previous interaction states

        chipy.utilities_logMes('SELECT PROX TACTORS')
        chipy.SelectProxTactors()             # run detections

        chipy.ExSolver(solver_type, norm, tol, relax, gs_it1, gs_it2) # run nlgs solver for contacts. 
        # these params defined above. 
        chipy.UpdateTactBehav()

        chipy.StockRloc() # record new state of interactions.

        chipy.utilities_logMes('COMPUTE DOF, FIELDS, etc.')
        chipy.ComputeDof()                    # compute displacements based on velocity for current time step

        chipy.utilities_logMes('UPDATE DOF, FIELDS')
        chipy.UpdateStep()

        chipy.utilities_logMes('WRITE OUT')
        chipy.WriteOut(freq_write)            # output if timestep multiple of freq_write.

        chipy.utilities_logMes('VISU & POSTPRO')
        chipy.WriteDisplayFiles(freq_display)  # output for imaging.
        chipy.WritePostproFiles()

        chipy.checkInteractiveCommand() # some more specific output types can be implemented here. 

    #
    # close display & postpro
    #
    chipy.CloseDisplayFiles()
    chipy.ClosePostproFiles()

    # this is the end
    chipy.Finalize()


def command_shear(time: float, num_files: int, name: str, right):

    chipy.overall_SetWorkingDirectory(name)

    # Initializing
    chipy.Initialize()

    # checking/creating mandatory subfolders
    chipy.checkDirectories()

    # logMes
    # chipy.utilities_DisableLogMes()

    # defining some variables
    # space dimension
    dim = 2

    # modeling hypothesis ( 1 = plain strain, 2 = plain stress, 3 = axi-symmetry)
    mhyp = 1

    # time evolution parameters
    total_time = time
    dt = 1e-3
    nb_steps = int(total_time // dt)
    print('will run for ',nb_steps,' steps')

    # theta integrator parameter  <- what is this?? OKAY this is for crank-nicolson numerical simulation. 
    # 0.5 means the scheme is conservative for smooth evolution problem. obviously want to choose this with intent. 
    theta = 0.5

    # deformable True or False
    deformable = False

    # interaction parameters  <- R_n tolerance  
    Rloc_tol = 5.e-2

    # nlgs parameters  nlgs=non-linear-gauss-seidel. 
    tol = 5e-4 # convergance tolerance
    relax = 1.0 # relaxation param 
    norm = 'Maxm ' # three options: quad, QM/16, maxm. used to check convergence. 
    gs_it1 = 50 # max number of convergence checks
    gs_it2 = 200 # number of iterations before convergence check
    solver_type='Stored_Delassus_Loops         '  # <- reportedly efficient in 2d for rigid bodies. 

    # write parameter
    freq_write   = nb_steps // num_files

    # display parameters
    freq_display = freq_write // 2

    itchatche = True

    #
    # read and load  
    #

    # Set space dimension
    chipy.SetDimension(dim,mhyp) # 
    #
    chipy.utilities_logMes('INIT TIME STEPPING')
    chipy.TimeEvolution_SetTimeStep(dt)
    chipy.Integrator_InitTheta(theta)

    # chipy.utilities_logMes('READ DATBOX')
    # chipy.ReadDatbox(deformable=False)

    chipy.utilities_logMes('READ BODIES')
    chipy.ReadBodies()
    print('setting conditions')
    print(right)
    chipy.RBDY2_SetBodiesInvisible([2,3]) # vertical walls removed. this is body ID not index.
    # chipy.SetPeriodicCondition(xperiod=right+.5) # periodic BCs instead
    chipy.RBDY2_SetPeriodicCondition(right)
    chipy.DKDKx_SetPeriodicCondition(right)
    print('set!')
    print('set period: ', right )

    chipy.utilities_logMes('READ BEHAVIOURS')
    chipy.ReadBehaviours()

    chipy.LoadTactors()
    chipy.LoadBehaviours()
    # THERMO RIGID 
    chipy.ReadModels()

    chipy.ReadDrivenDof()

    chipy.utilities_logMes('READ INI Vloc Rloc')
    chipy.ReadIni()

    chipy.utilities_logMes('WRITE BODIES')
    chipy.WriteBodies()

    chipy.utilities_logMes('WRITE BEHAVIOURS')  
    chipy.WriteBehaviours()

    chipy.utilities_logMes('WRITE DRIVEN DOF')
    chipy.WriteDrivenDof()


    # shearing bcs 
    # if right != None: 
    
    




    #
    # open display & postpro
    #

    chipy.utilities_logMes('DISPLAY & WRITE')
    chipy.OpenDisplayFiles()
    chipy.OpenPostproFiles()

    #
    # simulation part ...
    #

    # since constant compute elementary mass once
    chipy.utilities_logMes('COMPUTE MASS')
    chipy.ComputeMass()


    for k in range(nb_steps):
        if k%50 == 0:
                print( f"computing step {k}" )
        #
        chipy.utilities_logMes('INCREMENT STEP')
        chipy.utilities_EnableLogMes()
        chipy.IncrementStep()
        chipy.utilities_DisableLogMes()

        chipy.utilities_logMes('COMPUTE Fext')
        chipy.ComputeFext()                   # external force
        chipy.utilities_logMes('COMPUTE Fint')
        chipy.ComputeBulk()                   # rigidity and internal force info for all bodies
        chipy.utilities_logMes('COMPUTE Free Vlocy')
        chipy.ComputeFreeVelocity()           # velocity when no interactions detected (also interactions are computed)

        chipy.utilities_logMes('RESOLUTION' )
        chipy.RecupRloc(Rloc_tol)             # get previous interaction states

        chipy.utilities_logMes('SELECT PROX TACTORS')
        chipy.SelectProxTactors()             # run detections

        chipy.ExSolver(solver_type, norm, tol, relax, gs_it1, gs_it2) # run nlgs solver for contacts. 
        # these params defined above. 
        chipy.UpdateTactBehav()

        chipy.StockRloc() # record new state of interactions.

        chipy.utilities_logMes('COMPUTE DOF, FIELDS, etc.')
        chipy.ComputeDof()                    # compute displacements based on velocity for current time step

        chipy.utilities_logMes('UPDATE DOF, FIELDS')
        chipy.UpdateStep()

        chipy.utilities_logMes('WRITE OUT')
        chipy.WriteOut(freq_write)            # output if timestep multiple of freq_write.

        chipy.utilities_logMes('VISU & POSTPRO')
        chipy.WriteDisplayFiles(freq_display)  # output for imaging.
        chipy.WritePostproFiles()

        chipy.checkInteractiveCommand() # some more specific output types can be implemented here. 

    #
    # close display & postpro
    #
    chipy.CloseDisplayFiles()
    chipy.ClosePostproFiles()

    # this is the end
    chipy.Finalize()
