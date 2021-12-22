import importlib
import numpy as np
import matplotlib.pyplot as plt
from models.graph_models.simple import SimpleGraph

# Pick a model
model_name = 'SIR'  

#Initial Population in Nodes 0,1
N0 = 500  
N1 = 500

#Initial Conditions and parameters in Nodes 0,1
I0,R0  = 1,0
S0 = N0 - I0 - R0
beta0, gamma0 = 0.2, 1./10 

I1,R1  = 1,0
S1 = N1 - I1 - R1
beta1, gamma1 = 0.2, 1./10 

y = S0,I0,R0,S1,I1,R1
params = (N0, beta0, gamma0, N1, beta1, gamma1)

# Time
t = np.linspace(0, 160, 160)

#Importing the SIR
module = importlib.import_module(f'models.{model_name}')
model = getattr(module, model_name)


#Defining the weigths of the graph
#   \ 0  0.8\
#f =\ 0.1  0\
#   \       \
# f_{ij} = Part of population in Node i that goes to Node j
f =[[0, 0.8], [0.1, 0]]# In this case, the majority of people in node 0 goes to node 1
#Creating the graph
network = SimpleGraph(model, f)

#Solvit
ret = network.solve(y,t,params)

#All variables of the two nodes
S0, I0, R0, S1, I1, R1 = ret.T


#Plotting shit
# fig = plt.figure(facecolor='w')
axs= (plt.figure(facecolor='#dddddd')).subplots(1,2)
ax = axs[0]
# ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S0/1000, 'b', alpha=0.5, lw=2, label='Susceptible0')
ax.plot(t, I0/1000, 'r', alpha=0.5, lw=2, label='Infected0')
ax.plot(t, R0/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity0')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
# ax.grid(b=True, which='major', c='w', lw=2, ls='-')
ax.grid(True)
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)

ax1 = axs[1]
# ax1 = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax1.plot(t, S1/1000, 'b', alpha=0.5, lw=2, label='Susceptible1')
ax1.plot(t, I1/1000, 'r', alpha=0.5, lw=2, label='Infected1')
ax1.plot(t, R1/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity1')
ax1.set_xlabel('Time /days')
ax1.set_ylabel('Number (1000s)')
ax1.set_ylim(0,1.2)
ax1.yaxis.set_tick_params(length=0)
ax1.xaxis.set_tick_params(length=0)
# ax1.grid(b=True, which='major', c='w', lw=2, ls='-')
ax1.grid(True)
legend = ax1.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax1.spines[spine].set_visible(False)

plt.show()

