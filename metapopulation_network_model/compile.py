from io import open_code
from .cmp.parser import Parser
from .cmp.collector import CollectorVisitor

# Compiles a system of equations given by text
# to a file called model_name.py located at path
def compile_model(text, model_name, path):
    p = Parser()
    ast = p.parse(text)
    c = CollectorVisitor()
    c.visit(ast)
    parameters = c.parameters.difference(set(c.sets))
    code = f"""from scipy.integrate import odeint\nclass {model_name}:\n\n"""
    code += '\tsets = [' + ', '.join(f'\'{s}\'' for s in c.sets) + ']\n'
    code += '\tparams = [' + ', '.join(f'\'{param}\'' for param in parameters) + ']\n\n'
    code += '\t@staticmethod\n'
    code += f'\tdef deriv(initial_conditions, {c.variable}, ' + ', '.join(parameters) + '):\n'
    code += '\t\t' + ', '.join(c.sets) + ' = initial_conditions\n'
    for e in c.generator.visit(ast):
        code += '\t\t' + e + '\n'
    code += '\t\treturn ' + ', '.join(f'd{s}d{c.variable}' for s in c.sets) + '\n\n'
    code += '\t@staticmethod\n'
    code += '\tdef solve(initial_conditions, t, params):\n'
    code += f'\t\treturn odeint({model_name}.deriv, initial_conditions, t, args=params)\n'
    with open(f'{path}/{model_name}.py', 'w') as f:
        f.write(code)
