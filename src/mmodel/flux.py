from .mmodel import MetaModel, load_model

class FluxMetaModel(MetaModel):

    def __compute_structures__(self):
        network = self.network
        
        # Store the models used in the network to avoid multiple dynamic loading
        cmodels = {} 
        
        # Adyacency list of the network
        in_edges = { n.id : [] for n in network.nodes }
    
        # Associates every node with the total percent of elements leaving the node
        out_weight = { n.id : 0 for n in network.nodes }
        
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
            
            set_map[node.id] = dict((s,i) for i,s in enumerate(cmodel.sets, cury))
            cury += len(cmodel.sets)

        return cmodels, in_edges, out_weight, set_map


    def __generate_code__(self, structures):
        network = self.network

        cmodels, in_edges, out_weight, set_map = structures

        code = 'from scipy.integrate import odeint\n\n\n'
        code += 'def deriv(y, t, params):\n'
        code += '\tresult = [0] * len(y)\n'
        curr = 0 # Current result set
        cury = 0 # Current y array index
        curp = 0 # Current param array index
        for nodex in network.nodes:
            cmodel = cmodels[nodex.cmodel]

            symbols = [f'y[{i}]' for i in range(cury, cury + len(cmodel.sets))]
            cury += len(cmodel.sets)

            symbols += [f'params[{i}]' for i in range(curp, curp + len(cmodel.params))]
            curp += len(cmodel.params)

            for s, g in cmodel.equations.items():
                equation = f'\tresult[{curr}] = '

                equation += g(*symbols)

                for source, weight in in_edges[nodex.id]:
                    try:
                        equation += f' + {weight} * y[{set_map[source][s]}]'
                    except KeyError:
                        pass

                equation += f' - {out_weight[nodex.id]} * y[{set_map[nodex.id][s]}]\n'

                code += equation
                curr += 1
        code += '\treturn result\n'
        code += '\n\n' 
        code += 'def solve(y, t, params):\n'
        code += '\treturn odeint(deriv, y, t, args=(params,))'
        return code




