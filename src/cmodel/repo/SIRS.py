from scipy.integrate import odeint
class SIRS:

	sets = ['S', 'I', 'R', 'N']
	params = ['xi', 'beta', 'gamma']
	equations = {
		'S' : lambda S,I,R,N,_S,_I,_R,_N,xi,beta,gamma: f' -({beta} * {S} * {_I}) / ({_N}) + {xi} * {R}',
		'I' : lambda S,I,R,N,_S,_I,_R,_N,xi,beta,gamma: f' ({beta} * {S} * {_I}) / ({_N}) - {gamma} * {I}',
		'R' : lambda S,I,R,N,_S,_I,_R,_N,xi,beta,gamma: f' {gamma} * {I} - {xi} * {R}',
		'N' : lambda S,I,R,N,_S,_I,_R,_N,xi,beta,gamma: f' 0',
	}

	@staticmethod
	def deriv(y, t, params):
		S, I, R, N = y
		xi, beta, gamma = params
		dSdt = -(beta * S * I) / (N) + xi * R
		dIdt = (beta * S * I) / (N) - gamma * I
		dRdt = gamma * I - xi * R
		dNdt = 0
		return dSdt, dIdt, dRdt, dNdt

	@staticmethod
	def solve(y, t, params):
		return odeint(SIRS.deriv, y, t, args=(params,))
