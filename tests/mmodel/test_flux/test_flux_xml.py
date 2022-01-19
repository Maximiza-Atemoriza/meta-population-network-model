from mmodel.flux import FluxMetaModel
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0,160,160)
# Test constructor

net_file = './tests/mmodel/test_flux/example_network.json'
name = 'example_network'

mmodel = FluxMetaModel(name, net_file)

results = mmodel.simulate('./tests/mmodel/test_flux/input.xml', t)

S0 = results[1]['S']
I0 = results[1]['I']
R0 = results[1]['R']

S1 = results[2]['S']
I1 = results[2]['I']
R1 = results[2]['R']

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
plt.savefig('./tests/mmodel/test_flux/result_xml.png')



