import numpy as np

def f(x): 
    return x**(-1) - np.sin(x) -0.2*x +3

def fprime(x): 
    return -x**(-2) - np.cos(x) -0.2

x = np.arange(1, 6, 0.05)
xi = np.arange(1, 6, 0.5)

true = [f(p) for p in x]
explicit = [true[0]]
implicit = [true[0]]
crn = [true[0]]
for i, p in enumerate(xi[:-1]): 
    explicit += [explicit[i] + 0.5*fprime(p)]
    implicit += [implicit[i] + 0.5*fprime(xi[i+1])]
    crn += [crn[i] + 0.5*0.5*(fprime(p) + fprime(xi[i+1]))]

import matplotlib.pyplot as plt

# fig, ax = plt.subplots()
# plt.plot(xi, explicit, marker='o', label = 'Explicit', color='C1')
# plt.plot(xi, implicit, marker='o', label =  'Implicit', color='C2')
# plt.plot(xi, crn, marker = 'o', label='Crank-Nicholson', color='C3')
# plt.plot(x ,  true, linestyle='-', label = 'f(x)', color='C0')
# plt.legend()
# plt.savefig('graphs/euler-2.png')


def imposedForce(t):
    if t <=1.:
        f = 1e+5
    elif t > 1. and t<=5. : 
       f = 1e+5*t
    else: 
       f = 5e+5
    return f
    
t = np.arange(0, 8, 0.1)
y = [imposedForce(i) for i in t]

# fig, ax = plt.subplots()
# plt.plot(t, y, color = 'red')
# ax.set_xlabel('Time')
# ax.set_ylabel('Compressive Force')
# plt.savefig('graphs/out/compression')





# bond0 = [0.4700850190730865, 0.42343294285159533, 0.514700652833584, 0.5695940209373842, 0.4144436714698696]
# bond5 = [0.5272557051554402, 0.5951849876033307, 0.5597361825005753, 0.5559191326527287, 0.4389064510249173]

# disks1 = [0.5048901294323409 , 0.5744234729109101]

# bond0 = [0.6100679515892681]
# bond5 = []
# bond04 = []
# bond54 = []


# n = [7,6,5,4,3]
# fig, ax = plt.subplots()
# plt.plot(n, bond0, marker = 'o', color='C2', label = 'Uniform')
# plt.plot(n, bond5, marker = 'o', color='C3', label = 'Bi-Disperse')
# plt.hlines(disks1, xmin=2, xmax=8, colors=['C2', 'C3'], linestyles='--', alpha = 0.7)
# ax.set_xlabel('Side Number')
# ax.set_ylabel('Hexatic Bond Order')
# plt.legend()

# plt.savefig('graphs/out/hexatic.png')



# # bond04 = [0.5588504844651296, 0.5658426907764547, 0.5210209651098564, 0.40828481747352535, 0.38607244285823766]
# # bond54 = [0.5305939608303635, 0.540740362314347, 0.5113086425658896, 0.48428776472675844, 0.42372316704120216]

# # disks2 = [ 0.4704106951386805, 0.48287869325920846]



# n = [7,6,5,4,3]
# fig, ax = plt.subplots()
# plt.plot(n, bond04, marker = 'o', color='C2', label = 'Uniform')
# plt.plot(n, bond54, marker = 'o', color='C3', label = 'Bi-Disperse')
# plt.hlines(disks2, xmin=2, xmax=8, colors=['C2', 'C3'], linestyles='--', alpha = 0.7)
# ax.set_xlabel('Side Number')
# ax.set_ylabel('4-fold Bond Order')
# plt.legend()

# plt.savefig('graphs/out/quartic.png')




# packing0 = [ 0.7905334751429873, 0.7862621715927423, 0.7712296777707149, 0.867331942389885, 0.7575516709978513]
# packing5 = [ 0.7976438285857713, 0.8070906921337275, 0.7993398837733594, 0.7699599717096738, 0.7532206094174883]
# n = [7,6,5,4,3]

# disk=[0.8286873520707964, 0.8410847979113389]


# fig, ax = plt.subplots()
# plt.plot(n, packing0, marker = 'o', color='C1', label = 'Uniform')
# plt.plot(n, packing5, marker = 'o', color='C4', label = 'Bi-disperse')
# plt.hlines(disk, xmin=2, xmax=8, colors=['C1', 'C4'], linestyles='--', alpha = 0.7)
# ax.set_xlabel('Side Number')
# ax.set_ylabel('Packing Fraction')
# plt.legend()

# plt.savefig('graphs/out/phivsn.png')

import pandas as pd
import os

cn0 = pd.DataFrame(columns=['Z'])
for i in np.arange(6, 80, 5).tolist(): 
    if os.path.isfile(f"clean/no_magnets_disk0/fric0_prop5_compression/coord_num/coord_num_{i}"):
            temp = pd.read_csv(f"clean/no_magnets_disk0/fric0_prop5_compression/coord_num/coord_num_{i}", 
                                sep=']', names=['fluff', f"Z"])
            temp.drop(0, inplace = True)
            
            # print(temp['Z'])
    else: 
            temp = pd.DataFrame([None], columns=[f"Z"])
        
    cn0=pd.concat([cn0, temp['Z']]).reset_index(drop=True)

cn3 = pd.DataFrame(columns=['Z'])
for i in np.arange(6, 80, 5).tolist(): 
    if os.path.isfile(f"clean/no_magnets_polyg3/fric0_prop5_compression/coord_num/coord_num_{i}"):
            temp = pd.read_csv(f"clean/no_magnets_polyg3/fric0_prop5_compression/coord_num/coord_num_{i}", 
                                sep=']', names=['fluff', f"Z"])
            temp.drop(0, inplace = True)
            
            # print(temp['Z'])
    else: 
            temp = pd.DataFrame([None], columns=[f"Z"])
        
    cn3=pd.concat([cn3, temp['Z']]).reset_index(drop=True)

cn4 = pd.DataFrame(columns=['Z'])
for i in np.arange(6, 80, 5).tolist(): 
    if os.path.isfile(f"clean/no_magnets_polyg4/fric0_prop5_compression/coord_num/coord_num_{i}"):
            temp = pd.read_csv(f"clean/no_magnets_polyg4/fric0_prop5_compression/coord_num/coord_num_{i}", 
                                sep=']', names=['fluff', f"Z"])
            temp.drop(0, inplace = True)
            
            # print(temp['Z'])
    else: 
            temp = pd.DataFrame([None], columns=[f"Z"])
        
    cn4=pd.concat([cn4, temp['Z']]).reset_index(drop=True)

cn5 = pd.DataFrame(columns=['Z'])
for i in np.arange(6, 80, 5).tolist(): 
    if os.path.isfile(f"clean/no_magnets_polyg5/fric0_prop5_compression/coord_num/coord_num_{i}"):
            temp = pd.read_csv(f"clean/no_magnets_polyg5/fric0_prop5_compression/coord_num/coord_num_{i}", 
                                sep=']', names=['fluff', f"Z"])
            temp.drop(0, inplace = True)
            
            # print(temp['Z'])
    else: 
            temp = pd.DataFrame([None], columns=[f"Z"])
        
    cn5=pd.concat([cn5, temp['Z']]).reset_index(drop=True)
cn6 = pd.DataFrame(columns=['Z'])
for i in np.arange(6, 80, 5).tolist(): 
    if os.path.isfile(f"clean/no_magnets_polyg6/fric0_prop5_compression/coord_num/coord_num_{i}"):
            temp = pd.read_csv(f"clean/no_magnets_polyg6/fric0_prop5_compression/coord_num/coord_num_{i}", 
                                sep=']', names=['fluff', f"Z"])
            temp.drop(0, inplace = True)
            
            # print(temp['Z'])
    else: 
            temp = pd.DataFrame([None], columns=[f"Z"])
        
    cn6=pd.concat([cn6, temp['Z']]).reset_index(drop=True)
cn7 = pd.DataFrame(columns=['Z'])
for i in np.arange(6, 80, 5).tolist(): 
    if os.path.isfile(f"clean/no_magnets_polyg7/fric0_prop5_compression/coord_num/coord_num_{i}"):
            temp = pd.read_csv(f"clean/no_magnets_polyg7/fric0_prop5_compression/coord_num/coord_num_{i}", 
                                sep=']', names=['fluff', f"Z"])
            temp.drop(0, inplace = True)
            
            # print(temp['Z'])
    else: 
            temp = pd.DataFrame([None], columns=[f"Z"])
        
    cn7=pd.concat([cn7, temp['Z']]).reset_index(drop=True)




time = np.arange(6, 80, 5).tolist()
time2 = np.arange(6,60,5).tolist()
time3 = np.arange(6,75,5).tolist()
time4 = np.arange(6,60,5).tolist()
cn0['Z'] = pd.to_numeric(cn0['Z'])
cn0.round(decimals=3)
cn3['Z'] = pd.to_numeric(cn3['Z'])
cn3.round(decimals=3)
cn4['Z'] = pd.to_numeric(cn4['Z'])
cn4.round(decimals=3)
cn5['Z'] = pd.to_numeric(cn5['Z'])
cn5.round(decimals=3)
cn6['Z'] = pd.to_numeric(cn6['Z'])
cn6.round(decimals=3)
cn7['Z'] = pd.to_numeric(cn7['Z'])
cn7.round(decimals=3)


# fig, ax = plt.subplots()
# plt.plot(time, cn0['Z'], marker = 'o', color='C6', label = 'n=0')
# # # plt.plot(time, cn3['Z'], marker = 'o', color='C1', label = 'n=3')
# plt.plot(time2, cn4['Z'], marker = 'o', color='C2', label = 'n=4')
# plt.plot(time, cn5['Z'], marker = 'o', color='C3', label = 'n=5')
# # # plt.plot(time, cn6['Z'], marker = 'o', color='C4', label = 'n=6')
# plt.plot(time, cn7['Z'], marker = 'o', color='C5', label = 'n=7')
# # # plt.plot(n, packing5, marker = 'o', color='C4', label = 'Bi-disperse')
# # plt.hlines(disk, xmin=2, xmax=8, colors=['C1', 'C4'], linestyles='--', alpha = 0.7)
# # ax.set_ylim(3.2, 4.2)
# ax.set_xlabel('Time')
# ax.set_ylabel('Coordination Number')
# plt.legend()

# plt.savefig('graphs/out/polygscnfric.png')




phi0=[]
for i in np.arange(6, 80, 5).tolist(): 
    path = f"clean/no_magnets_disk0/fric0_prop5_compression/phi/packing_frac_{i}"
    if os.path.isfile(path):
          with open(path, 'r') as f: 
                phi0 += [round(float(f.readline()),3)]
    else: 
        phi0 += [None]

# phi3=[]
# for i in np.arange(6, 80, 5).tolist(): 
#     path = f"clean/no_magnets_polyg3/fric5_prop5_compression/phi/packing_frac_{i}"
#     if os.path.isfile(path):
#           with open(path, 'r') as f: 
#                 phi3 += [round(float(f.readline()),3)]
#     else: 
#         phi3 += [None]


phi4=[]
for i in np.arange(6, 80, 5).tolist(): 
    path = f"clean/no_magnets_polyg4/fric0_prop5_compression/phi/packing_frac_{i}"
    if os.path.isfile(path):
          with open(path, 'r') as f: 
                phi4 += [round(float(f.readline()),3)]
    else: 
        phi4 += [None]


phi5=[]
for i in np.arange(6, 80, 5).tolist(): 
    path = f"clean/no_magnets_polyg5/fric0_prop5_compression/phi/packing_frac_{i}"
    if os.path.isfile(path):
          with open(path, 'r') as f: 
                phi5 += [round(float(f.readline()),3)]
    else: 
        phi5 += [None]


# phi6=[]
# for i in np.arange(6, 80, 5).tolist(): 
#     path = f"clean/no_magnets_polyg6/fric5_prop5_compression/phi/packing_frac_{i}"
#     if os.path.isfile(path):
#           with open(path, 'r') as f: 
#                 phi6 += [round(float(f.readline()),3)]
#     else: 
#         phi6 += [None]


phi7=[]
for i in np.arange(6, 80, 5).tolist(): 
    path = f"clean/no_magnets_polyg7/fric0_prop5_compression/phi/packing_frac_{i}"
    if os.path.isfile(path):
          with open(path, 'r') as f: 
                phi7 += [round(float(f.readline()),3)]
    else: 
        phi7 += [None]



time = np.arange(6, 80, 5).tolist()


# fig, ax = plt.subplots()
# plt.plot(time, phi0, marker = 'o', color='C6', label = 'n=0')
# # plt.plot(time, phi3, marker = 'o', color='C1', label = 'n=3')
# plt.plot(time, phi4, marker = 'o', color='C2', label = 'n=4')
# plt.plot(time, phi5, marker = 'o', color='C3', label = 'n=5')
# # plt.plot(time, phi6, marker = 'o', color='C4', label = 'n=6')
# plt.plot(time, phi7, marker = 'o', color='C5', label = 'n=7')
# # plt.plot(n, packing5, marker = 'o', color='C4', label = 'Bi-disperse')
# # plt.hlines(disk, xmin=2, xmax=8, colors=['C1', 'C4'], linestyles='--', alpha = 0.7)
# # ax.set_ylim(3.2, 4.2)
# ax.set_xlabel('Time')
# ax.set_ylabel('Packing Fraction')
# plt.legend()

# plt.savefig('graphs/out/pacfracpolygfric.png')



fig, ax = plt.subplots()

plt.plot(phi0, cn0['Z'], marker = 'o', color='C6', label = 'n=0')
# plt.plot(time, phi3, marker = 'o', color='C1', label = 'n=3')
plt.plot(phi4, cn4['Z'], marker = 'o', color='C2', label = 'n=4')
plt.plot(phi5, cn5['Z'], marker = 'o', color='C3', label = 'n=5')
# plt.plot(time, phi6, marker = 'o', color='C4', label = 'n=6')
plt.plot(phi7, cn7['Z'], marker = 'o', color='C5', label = 'n=7')

# plt.plot()

ax.set_ylabel('Coordination Number')
ax.set_xlabel('Packing Fraction')
plt.legend()

plt.savefig('graphs/out/cnvsphi0.png')