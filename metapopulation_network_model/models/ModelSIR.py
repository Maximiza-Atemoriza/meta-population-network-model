from scipy.integrate import odeint
class ModelSIR:

	sets = ['S', 'I', 'R']
	params = ['N', 'beta', 'gamma']

	@staticmethod
	def deriv(initial_conditions, t, N, beta, gamma):
		S, I, R = initial_conditions
		dSdt = -(beta * S * I) / (N)
		dIdt = (beta * S * I) / (N) - gamma * I
		dRdt = gamma * I
		return dSdt, dIdt, dRdt

	@staticmethod
	def solve(initial_conditions, t, params):
		return odeint(ModelSIR.deriv, initial_conditions, t, args=params)
