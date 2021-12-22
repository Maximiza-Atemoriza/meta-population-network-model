from scipy.integrate import odeint

class SimpleGraph:
    def __init__(self,model, f):
        self.model = model
        self.f = f
    
    def deriv(self, initial_conditions, t, params):
        node1_init = initial_conditions[:len(initial_conditions)//2]
        node1_params = params[:len(initial_conditions)//2]
        node2_init = initial_conditions[len(initial_conditions)//2:]
        node2_params = params[len(initial_conditions)//2:]

        node1_vars = self.model.deriv(node1_init, t, *node1_params)
        node2_vars = self.model.deriv(node2_init, t, *node2_params)

        result = []
        for i in range(len(node1_vars)):
            result.append(node1_vars[i] - self.f[0][1]*node1_init[i] + self.f[1][0] * node2_init[i])
        for i in range(len(node2_vars)):
            result.append(node2_vars[i] - self.f[1][0]*node2_init[i] + self.f[0][1] * node1_init[i])

        return result

    def solve(self, initial_conditions, t, params):
        return odeint(self.deriv, initial_conditions, t, args= (params,) )


