from scipy.integrate import odeint


def deriv(y, t, params):
    result = [0] * len(y)
    S_1 = y[0] + y[2]
    S_2 = y[1] + y[3]
    I_1 = y[4] + y[6]
    I_2 = y[5] + y[7]
    R_1 = y[8] + y[10]
    R_2 = y[9] + y[11]
    return result


def solve(y, t, params):
    return odeint(deriv, y, t, args=(params,))
