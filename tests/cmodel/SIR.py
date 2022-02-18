from scipy.integrate import odeint


class SIR:

    sets = ["S", "I", "R"]
    params = ["N", "gamma", "beta"]
    equations = {
        "S": lambda S, I, R, N, gamma, beta: f" -({beta} * {S} * {I}) / ({N})",
        "I": lambda S, I, R, N, gamma, beta: f" ({beta} * {S} * {I}) / ({N}) - {gamma} * {I}",
        "R": lambda S, I, R, N, gamma, beta: f" {gamma} * {I}",
    }

    @staticmethod
    def deriv(y, t, params):
        S, I, R = y
        N, gamma, beta = params
        dSdt = -(beta * S * I) / (N)
        dIdt = (beta * S * I) / (N) - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    @staticmethod
    def solve(y, t, params):
        return odeint(SIR.deriv, y, t, args=(params,))
