from .mmodel import MetaModel, load_model


class SimpleTripMetaModel(MetaModel):
    def __compute_structures__(self):
        network = self.network

        # Store the models used in the network to avoid multiple dynamic loading
        cmodels = {}

        # Adyacency list of the network
        in_edges = {n.id: [] for n in network.nodes}

        # Associates every node with the total percent of elements leaving the node
        out_weight = {n.id: 0 for n in network.nodes}

        # Associates each set of each node with its position at the initial conditions vector
        set_map = {}

        for edge in network.edges:
            out_weight[edge.source] += edge.weight
            in_edges[edge.target].append((edge.source, edge.weight))

        cury = 0
        for node in network.nodes:
            try:
                cmodel = cmodels[node.cmodel]
            except KeyError:
                cmodel = cmodels[node.cmodel] = load_model(node.cmodel)

            set_map[node.id] = dict((s, i) for i, s in enumerate(cmodel.sets, cury))
            cury += len(cmodel.sets)

        return cmodels, in_edges, out_weight, set_map

    def __generate_code__(self, structures):
        network = self.network
        n = len(network.nodes)

        cmodels, in_edges, out_weight, set_map = structures

        code = "from scipy.integrate import odeint\n\n\n"
        code += "def deriv(y, t, params):\n"
        code += "\tresult = [0] * len(y)\n"

        cur_set = 0
        for s in cmodels["SIR"].sets:
            for cur_node in range(n):
                equation = f"\t{s}_{cur_node + 1} = "
                start = cur_node
                while start < n * n:
                    equation += f" y[{cur_set * n * n + start}] +"
                    start += n
                equation = equation[:-1]
                equation += "\n"
                code += equation
            cur_set += 1

        code += "\treturn result\n"
        code += "\n\n"
        code += "def solve(y, t, params):\n"
        code += "\treturn odeint(deriv, y, t, args=(params,))"
        return code
