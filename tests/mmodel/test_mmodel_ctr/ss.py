from scipy.integrate import odeint


def deriv(y, t, params):
	result = [0] * len(y)
	result[0] =  -(params[0] * y[0] * y[1]) / (params[2]) + 0.5 * y[3] - 0.5 * y[0]
	result[1] =  (params[0] * y[0] * y[1]) / (params[2]) - params[1] * y[1] + 0.5 * y[4] - 0.5 * y[1]
	result[2] =  params[1] * y[1] + 0.5 * y[5] - 0.5 * y[2]
	result[3] =  -(params[3] * y[3] * y[4]) / (params[5]) + 0.5 * y[0] - 0.5 * y[3]
	result[4] =  (params[3] * y[3] * y[4]) / (params[5]) - params[4] * y[4] + 0.5 * y[1] - 0.5 * y[4]
	result[5] =  params[4] * y[4] + 0.5 * y[2] - 0.5 * y[5]
	return result


def solve(y, t, params):
	return odeint(deriv, y, t, args=(params,))