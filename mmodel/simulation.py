from scipy.integrate import odeint
from network import Network

# TODO: Remove all this section when cmodel repo is implemented
import importlib
def load_model(cmodel):
    module = importlib.import_module(f'cmodel.repo.{cmodel}')
    return getattr(module, cmodel)
# ============================================================= 


# Implemented with clausures for memory managemente efficiency
def simulate(network: Network, t):
    # Initial condition vector of the meta model 
    y = []

    # Parameters vector of the meta model
    params = []

    cmodels = {} # Store the models used in the network to avoid multiple dynamic loading

    # Adyacency list of the network
    in_edges = { n.id : [] for n in network.nodes } 

    # Associates every node with the total percent of elements leaving the node
    out_weight = { n.id : 0 for n in network.nodes }
    
    # Associates each set of each node of the meta model with the index of its initial conditions in the y vector
    set_map = {} 

    for edge in network.edges:
        out_weight[edge.source] += edge.weight
        in_edges[edge.target].append((edge.source, edge.weight))

    for node in network.nodes:
        try:
            cmodel = cmodels[node.cmodel]
        except:
            cmodel = cmodels[node.cmodel] = load_model(node.cmodel) # TODO: Change this line to use cmodel repo
        
        
        set_map[node.id] = dict(zip(cmodel.sets, range(len(y), len(y) + len(cmodel.sets))))
        y += node.y
        params += node.params
    
    print(set_map)
    def deriv(_y, _t, _params):
        result = []
        yindex = 0
        pindex = 0

        for nodex in network.nodes:
            node_cmodel = cmodels[nodex.cmodel]
            
            node_y = _y[yindex : yindex+len(node_cmodel.sets)]
            yindex += len(node_cmodel.sets)

            node_params = _params[pindex : pindex+len(node_cmodel.params)]
            pindex += len(node_cmodel.params)

            node_result = node_cmodel.deriv(node_y, _t, *node_params)

            for s, val in zip(node_cmodel.sets, node_result):
                for source, weight in in_edges[nodex.id]:
                    try:
                        val += weight * set_map[source][s] 
                    except KeyError: # The incident node does not have a matching set 
                        val += 0
                val -= out_weight[nodex.id] * set_map[nodex.id][s]
                
                result.append(val)

        return result

    return odeint(deriv, y, t, args = (params,)) 
            


            



            

