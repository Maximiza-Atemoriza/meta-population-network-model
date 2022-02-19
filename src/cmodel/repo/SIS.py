from scipy.integrate import odeint
class SIS:

	sets = ['S', 'I', 'N']
	params = ['beta', 'gamma']
	equations = {
		'S' : lambda S,I,N,_S,_I,_N,beta,gamma: f' -({beta} * {S} * {_I}) / ({_N}) + {gamma} * {I}',
		'I' : lambda S,I,N,_S,_I,_N,beta,gamma: f' ({beta} * {S} * {_I}) / ({_N}) - {gamma} * {I}',
		'N' : lambda S,I,N,_S,_I,_N,beta,gamma: f' 0',
	}

	@staticmethod
	def deriv(y, t, params):
		S, I, N = y
		beta, gamma = params
		dSdt = -(beta * S * I) / (N) + gamma * I
		dIdt = (beta * S * I) / (N) - gamma * I
		dNdt = 0
		return dSdt, dIdt, dNdt

	@staticmethod
	def solve(y, t, params):
		return odeint(SIS.deriv, y, t, args=(params,))
