import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

# lifting this code from https://rajeshrinet.github.io/blog/2014/ising-model/
# straightforward, but i think this is not quite what i want??? not sure. 
# also need a way to minimse the energy 

def initialstate(N):   
    ''' generates a random spin configuration for initial condition'''
    state = 2*np.random.randint(2, size=(N,N))-1
    # above generates square matrix (NxN) containing 0 or 1. then double and subtract 1 to get -1 or 1.  
    return state


def mcmove(config, beta, N):
    '''Monte Carlo move using Metropolis algorithm '''
    for i in range(N): 
        for j in range(N): # for every node:
                a = np.random.randint(0, N) 
                b = np.random.randint(0, N)
                s =  config[a, b] #random node 
                nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N] # sum adjacent nodes (edges wrap around)
                cost = 2*s*nb # times by node. match gives 1, else -1, then double (why - interaction goes both ways)
                if cost < 0: 
                    s *= -1 # accept the change (-1 -> 1, 1 -> -1)
                elif rand() < np.exp(-cost*beta): # acceptance probability 
                    s *= -1
                config[a, b] = s # set new spin
    return config


def calcEnergy(config, N):
    '''Energy of a given configuration'''
    # hamiltonian (for constant J=1 and no H) simplifies to this.
    energy = 0
    for i in range(len(config)):
        for j in range(len(config)):
            S = config[i,j] #-1 or 1
            nb = config[(i+1)%N, j] + config[i,(j+1)%N] + config[(i-1)%N, j] + config[i,(j-1)%N] # each also -1 or 1 
            energy += -nb*S
    return energy/4. 


def simulate(config, N, beta):   
    ''' This module simulates the Ising model'''

    f = plt.figure(figsize=(15, 15), dpi=80);    
    configPlot(f, config, 0, N, 1);
    
    msrmnt = 1001
    for i in range(msrmnt):
        mcmove(config, beta, N)
        if i == 1:       configPlot(f, config, i, N, 2);
        if i == 4:       configPlot(f, config, i, N, 3);
        if i == 32:      configPlot(f, config, i, N, 4);
        if i == 100:     configPlot(f, config, i, N, 5);
        if i == 1000:    configPlot(f, config, i, N, 6);
                
                
def configPlot(f, config, i, N, n_):
    ''' This modules plts the configuration once passed to it along with time etc '''
    X, Y = np.meshgrid(range(N), range(N))
    sp =  f.add_subplot(3, 3, n_ )  
    plt.setp(sp.get_yticklabels(), visible=False)
    plt.setp(sp.get_xticklabels(), visible=False)      
    plt.pcolormesh(X, Y, config, cmap = 'coolwarm')
    plt.title('Time=%d'%i); plt.axis('tight')    


# run (and params)
N = 100
config = initialstate(N= N)
print('initialised')
# taking const. temp for now 
T = 1.5
beta = 1/T 
burnin = 200
mcsteps = 300

for i in range(burnin): 
    mcmove(config= config, beta= beta, N= N)
print('burn in complete')
E = np.zeros(mcsteps)
for i in range(mcsteps): 
    mcmove(config= config, beta= beta, N= N)
    Ene = calcEnergy(config= config, N= N)
    if i%10==0: print(Ene)
    E[i] += Ene # for plotting 

simulate(config= config, N= N, beta= beta)


ind = np.arange(mcsteps, step= 1)

# f = plt.figure(figsize=(18, 10)); # plot the energy   
# plt.scatter(ind, E, s=50, marker='o', color='green')
# plt.xlabel("Interation", fontsize=20);
# plt.ylabel("Energy ", fontsize=20);         plt.axis('tight');

plt.show()