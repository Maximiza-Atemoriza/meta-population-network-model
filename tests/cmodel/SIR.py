from scipy.integrate import odeint
class SIR:

	sets = ['S', 'I', 'R', 'N']
	params = ['beta', 'gamma']
	equations = {
		'S' : lambda S,I,R,N,_S,_I,_R,_N,beta,gamma: f' -({beta} * {S} * {_I}) / ({_N})',
		'I' : lambda S,I,R,N,_S,_I,_R,_N,beta,gamma: f' ({beta} * {S} * {_I}) / ({_N}) - {gamma} * {I}',
		'R' : lambda S,I,R,N,_S,_I,_R,_N,beta,gamma: f' {gamma} * {I}',
		'N' : lambda S,I,R,N,_S,_I,_R,_N,beta,gamma: f' 0',
	}

	@staticmethod
	def deriv(y, t, params):
		S, I, R, N = y
		beta, gamma = params
		dSdt = -(beta * S * I) / (N)
		dIdt = (beta * S * I) / (N) - gamma * I
		dRdt = gamma * I
		dNdt = 0
		return dSdt, dIdt, dRdt, dNdt

	@staticmethod
	def solve(y, t, params):
		return odeint(SIR.deriv, y, t, args=(params,))
