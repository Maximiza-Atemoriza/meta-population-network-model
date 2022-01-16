from .parser import Parser
from .collector import CollectorVisitor
from .codegen import CodeGenerator

# Compiles a system of equations given by text
# to a file called model_name.py located at path
def compile_model(text, model_name, path):
    p = Parser()
    ast = p.parse(text)

    c = CollectorVisitor()
    g = c.generator
    
    sets, variable, parameters = c.visit(ast)
    equations = g.visit(ast)

    formated_equations = g.visit(ast, interpolation=True)
    delegate = 'lambda ' + ','.join(sets) + ',' + ','.join(parameters) + ':'

    code = f"""from scipy.integrate import odeint\nclass {model_name}:\n\n"""

    # properties of the model
    code += '\tsets = [' + ', '.join(f'\'{s}\'' for s in sets) + ']\n'
    code += '\tparams = [' + ', '.join(f'\'{p}\'' for p in parameters) + ']\n'
    code += '\tequations = {\n' 
    for s, e in zip(sets, formated_equations):
        right = e.split('=')[1]
        code += f'\t\t\'{s}\' : ' + delegate + f' f\'{right}\',\n'
    code += '\t}\n\n'

    # simulation
    code += '\t@staticmethod\n'
    code += f'\tdef deriv(y, {c.variable}, params):\n'
    code += '\t\t' + ', '.join(sets) + ' = y\n'
    code += '\t\t' + ', '.join(parameters) + ' = params\n'
    for e in equations:
        code += '\t\t' + e + '\n'
    code += '\t\treturn ' + ', '.join(f'd{s}d{c.variable}' for s in c.sets) + '\n\n'
    code += '\t@staticmethod\n'
    code += '\tdef solve(y, t, params):\n'
    code += f'\t\treturn odeint({model_name}.deriv, y, t, args=(params,))\n'
    with open(f'{model_name}.py', 'w') as f:
        f.write(code)
