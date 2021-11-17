import importlib
import numpy as np
from compile import compile_model
import matplotlib.pyplot as plt


text = r"""
\frac{dS}{dt} = - \frac{\beta S I}{N}\\
\frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I\\
\frac{dR}{dt} = \gamma I
"""

model_name = 'ModelSIR'
#compile_model(text, model_name)


# Total population, N.
N = 1000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.2, 1./10 
# A grid of time points (in days)
t = np.linspace(0, 160, 160)




module = importlib.import_module(f'models.{model_name}')
model = getattr(module, model_name)



# you need to place the sets and parameters in the same order as they appear in the source file generated 
y0 = S0, I0, R0
params = (N, beta, gamma)
# you can consult the order with
print(model.sets)
print(model.params)
#you can 

ret = model.solve(y0, t, params)
S, I, R = ret.T
# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
plt.savefig('a.png')
