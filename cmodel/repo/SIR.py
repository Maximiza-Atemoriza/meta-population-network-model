from scipy.integrate import odeint
class SIR:

	sets = ['S', 'I', 'R']
	params = ['beta', 'gamma', 'N']
	equations = {
		'S' : lambda S,I,R,beta,gamma,N: f' -({beta} * {S} * {I}) / ({N})',
		'I' : lambda S,I,R,beta,gamma,N: f' ({beta} * {S} * {I}) / ({N}) - {gamma} * {I}',
		'R' : lambda S,I,R,beta,gamma,N: f' {gamma} * {I}',
	}

	@staticmethod
	def deriv(y, t, params):
		S, I, R = y
		beta, gamma, N = params
		dSdt = -(beta * S * I) / (N)
		dIdt = (beta * S * I) / (N) - gamma * I
		dRdt = gamma * I
		return dSdt, dIdt, dRdt

	@staticmethod
	def solve(y, t, params):
		return odeint(SIR.deriv, y, t, args=(params,))
