from .mmodel import MetaModel, load_model
import numpy as np


class SimpleTripMetaModel(MetaModel):
    def __transform_input__(self, y, params):
        network = self.network
        cmodel = load_model(network.nodes[0].cmodel)
        sets = cmodel.sets
        
        N = len(network.nodes)
        matrices = { s : numpy.zeros(shape=(N,N)) for s in sets }

        cury = 0
        for i in range(N):
            for s in sets:
                matrices[s][i][i] = y[cury]
                cury += 1
        newy = []
        for s in sets:
            newy += list(matrices[s].reshape(N*N))
        return newy, params

    def __transform_output__(self, ret):
        network = self.network
        cmodel = load_model(network.nodes[0].cmodel)
        sets = cmodel.sets

        N = len(network.nodes)
        matrices = {}
        for i, s in enumerate(sets):
            matrix = np.array(ret[i*N*N:(i+1)*N*N]).reshape(shape=(N,N))
            matrices[s] = matrix
        
        results = {}

        for i in range(N):
            results[i] = {}
            for s in sets:
                results[i][s] = 0
                for j in range(N):
                    results[i][s] += matrices[s][j][i]
        return results



    def __compute_structures__(self):
        network = self.network
        
        N = len(network.nodes)

        # Store the models used in the network to avoid multiple dynamic loading
        cmodels = {}

        # Asociates every node with the starting and ending positions of its parameters in the param vector
        params_map = { i : (0,0) for i in range(N) }

        node_map = {}

        curp = 0
        for node in network.nodes:
            try:
                cmodel = cmodels[node.cmodel]
            except KeyError:
                cmodel = cmodels[node.cmodel] = load_model(node.cmodel)
            
            params_map[node.id] = (curp, curp + len(cmodel.params))
            curp += len(cmodel.params)

            node_map[node.id] = node


        # Build an adyacency matrix for the network
        ady_matrix = [[0 for i in range(N)] for j in range(N)]
        for edge in network.edges:
            ady_matrix[edge.source][edge.target] = edge.weight
        
        
        local_pos = lambda k,i,j : k * N * N + i * N + j
        global_pos = lambda k,j: [local_pos(k,i,j) for i in range(N)]

        return cmodels, ady_matrix, node_map, params_map, local_pos, global_pos

    def __generate_code__(self, structures):
        network = self.network
        cmodels, ady_matrix, node_map, params_map, local_pos, global_pos = structures
        
        N = len(network.nodes)
        sets = cmodels[network.nodes[0].cmodel].sets
        K = len(sets)
        
        def get_global_symbol(k,j):
            return "(" + "+".join([f"y[{local_pos(k,i,j)}]" for i in range(N)]) + ")"


        code = "from scipy.integrate import odeint\n\n\n"
        code += "def deriv(y, t, params):\n"
        code += "\tresult = [0] * len(y)\n"

        for k, s in enumerate(sets):
            for i in range(N):
                for j in range(N):
                    node = node_map[j]
                    cmodel = cmodels[node.cmodel]
                    # Generate the equation of the set s for the node i,j 
                    # This represents the population of the subyacent node i living in the subyacent node j
                    equation = f"\tresult[{local_pos(k,i,j)}] = "
                    
                    # Get the value of the sets of node i,j
                    local_symbols = [f"y[{local_pos(kx,i,j)}]" for kx in range(K)]
                    global_symbols = [get_global_symbol(kx,j) for kx in range(K)]
                    start, end = params_map[j]
                    params_symbols = [f"params[{p}]" for p in range(start, end)]
                    symbols = local_symbols + global_symbols + params_symbols

                    equation += cmodel.equations[s](*symbols) 

                    if i == j:
                        out_weight = 0
                        for u in range(N):
                            out_weight += ady_matrix[i][u]
                            if ady_matrix[u][i] > 0:
                                equation += f" + {ady_matrix[u][i]} * y[{local_pos(k,i,u)}]"

                        equation += f" - {out_weight} * y[{local_pos(k,i,i)}]"
                    else:
                        equation += f" + {ady_matrix[i][j]} * y[{local_pos(k,i,i)}]"
                        equation += f" - {ady_matrix[j][i]} * y[{local_pos(k,i,j)}]"

                    code += equation + "\n"


        code += "\treturn result\n"
        code += "\n\n"
        code += "def solve(y, t, params):\n"
        code += "\treturn odeint(deriv, y, t, args=(params,))"
        return code
