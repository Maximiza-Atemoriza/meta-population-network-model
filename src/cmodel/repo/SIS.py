from scipy.integrate import odeint


class SIS:

    sets = ["S", "I"]
    params = ["beta", "alpha"]
    equations = {
        "S": lambda S, I, beta, alpha: f"-{beta} * {S} * {I} + {alpha} * {I}",
        "I": lambda S, I, beta, alpha: f"{beta} * {S} * {I} - {alpha} * {I}",
    }

    @staticmethod
    def deriv(y, t, params):
        S, I = y
        beta, alpha = params
        dSdt = -(beta * S * I) + alpha * I
        dIdt = beta * S * I - alpha * I
        return dSdt, dIdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SIS.deriv, y, t, args=(params,))
