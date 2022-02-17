from scipy.integrate import odeint


def deriv(y, t, params):
	result = [0] * len(y)
	return result


def solve(y, t, params):
	return odeint(deriv, y, t, args=(params,))