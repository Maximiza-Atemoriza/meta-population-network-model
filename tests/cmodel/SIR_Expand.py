from scipy.integrate import odeint
class SIR_Expand:

	sets = ['S', 'I', 'R']
	params = ['beta', 'N', 'gamma']
	equations = {
		'S' : lambda S,I,R,_S,_I,_R,beta,N,gamma,_beta,_N,_gamma: f' -({beta} * {S} * {_I}) / ({_N})',
		'I' : lambda S,I,R,_S,_I,_R,beta,N,gamma,_beta,_N,_gamma: f' ({beta} * {S} * {I}) / ({N}) - {gamma} * {I}',
		'R' : lambda S,I,R,_S,_I,_R,beta,N,gamma,_beta,_N,_gamma: f' {gamma} * {I}',
	}

	@staticmethod
	def deriv(y, t, params):
		S, I, R = y
		beta, N, gamma = params
		dSdt = -(beta * S * I) / (N)
		dIdt = (beta * S * I) / (N) - gamma * I
		dRdt = gamma * I
		return dSdt, dIdt, dRdt

	@staticmethod
	def solve(y, t, params):
		return odeint(SIR_Expand.deriv, y, t, args=(params,))
