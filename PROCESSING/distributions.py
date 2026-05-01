
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
import pandas

path = "graphs/forces_27.txt"

# with open(path, 'r') as f: 
#     lines = f.readlines()
#     for line in lines: 
#         force = re.split(', ', line)

def get_force_graph(path:str, step):
    forces = pandas.read_csv(f"{path}/forces_{step}.txt", sep=',', names=['index', 'forces']).set_index('index')
    average = forces['forces'].mean()
    var = forces.std()

    too_big = forces[forces['forces'] > average + 3*var['forces']].index
    forces_adj = forces.drop(too_big)
    print(len(too_big))
    print('yes')

    fig, ax = plt.subplots()
    forcedist=sbn.displot(forces, x='forces', bins = 50, log_scale=True)
    plt.axvline(average, color='red')
    forcedist.set(xlim=(1, None))
    forcedist.set(xlabel='Normal Force Magnitude')
    fig = forcedist.fig
    fig.savefig(f"graphs/{path}/force_dist/force-distribution-test{step}.png")

    fig, ax = plt.subplots()
    forcedist=sbn.histplot(forces_adj, x='forces', bins=50, kde=True, ax=ax)
    plt.axvline(average, color='red')
    forcedist.set(xlim=(1, None))
    forcedist.set(ylim=(1, 60))
    ax.set_yscale('log')
    forcedist.set(xlabel='Normal Force Magnitude')
    # fig = forcedist.fig
    fig.savefig(f"graphs/{path}/force_dist/force-distribution-kde{step}.png")

import order
def get_rdf_graph(path:str, step:int, d, bin, dists2, num_grains ): 
    x = np.arange(0.01, 110., bin) # could make these smaller but then itll take even longer
    y = [order.get_rdf(name=path, step=step, r=r, bin=bin, dists2=dists2, num_grains=num_grains) for r in x] 

    xd = x/d 
    data = pandas.DataFrame({'r/d': xd, 'rdf': y})

    fig, ax = plt.subplots()
    rdfdist = sbn.relplot(data, x='r/d', y='rdf', kind='line')
    plt.axvline(1, color='gray', linestyle='--')
    plt.axvline(2, color='gray', linestyle='--')
    plt.axvline(3, color='gray', linestyle='--')
    # rdfdist.set(xlabel='Distance', )
    fig = rdfdist.fig
    fig.savefig(f"graphs/{path}/rdf/rdf_plot_{step}")

def get_rdf_graph2(path:str, step:int, d, bin, dists2, num_grains ): 
    x = np.arange(0.01, 110., bin) # could make these smaller but then itll take even longer
    y = [order.get_rdf(name=path, step=step, r=r, bin=bin, dists2=dists2, num_grains=num_grains)  for r in x] 

    xd = x/d 
    data = pandas.DataFrame({'r/d': xd, 'rdf': y})

    fig, ax = plt.subplots()
    rdfdist = sbn.relplot(data, x='r/d', y='rdf', kind='line')
    # plt.axvline(1, color='gray', linestyle='--')
    # plt.axvline(2, color='gray', linestyle='--')
    # plt.axvline(3, color='gray', linestyle='--')
    # rdfdist.set(xlabel='Distance', )
    rdfdist.set(xlim=(None, 20))
    fig = rdfdist.fig
    fig.savefig(f"graphs/{path}/rdf/rdf_plot_adj_{step}")


def alignment_graph(name, step): 

    aligns = order.get_alignments(name, step)


    data = pandas.DataFrame({'Angle': aligns})

    fig, ax = plt.subplots()
    algraph = sbn.histplot(data=data, x='Angle', bins=40)
    algraph.set(xlim=(-np.pi, np.pi))
    algraph.set(ylim=(0, 5))
    
    plt.savefig(f"graphs/out/angles/{name}{step}alignment")


