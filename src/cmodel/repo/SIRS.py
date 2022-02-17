from scipy.integrate import odeint


class SIRS:

    sets = ["S", "I", "R"]
    params = ["beta", "gamma", "xi"]
    equations = {
        "S": lambda S, I, R, beta, gamma, xi: f" -({beta} * {S} * {I}) + {xi}*{R}",
        "I": lambda S, I, R, beta, gamma, xi: f" ({beta} * {S} * {I})  - {gamma} * {I}",
        "R": lambda S, I, R, beta, gamma, xi: f" {gamma} * {I} - {xi}*{R}",
    }

    @staticmethod
    def deriv(y, t, params):
        S, I, R = y
        beta, gamma, xi = params
        dSdt = -(beta * S * I) + xi*R 
        dIdt = (beta * S * I) - gamma * I
        dRdt = gamma * I - xi*R
        return dSdt, dIdt, dRdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SIRS.deriv, y, t, args=(params,))
