class Node:
    pass


class SystemNode(Node):
    def __init__(self, equations):
        self.equations = equations


class EquationNode(Node):
    def __init__(self, differential, expression):
        self.differential = differential
        self.expression = expression


class DifferentialNode(Node):
    def __init__(self, function, parameter):
        self.function = function
        self.parameter = parameter


class ExpressionNode(Node):
    pass


class ParenthesisNode(ExpressionNode):
    def __init__(self, expression):
        self.expression = expression


class BinaryNode(ExpressionNode):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class FractionNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class AtomicNode(ExpressionNode):
    def __init__(self, value):
        self.value = value


class SymbolNode(AtomicNode):
    def __init__(self, value, isGlobal=False):
        self.value = value
        self.isGlobal = isGlobal


class NumberNode(AtomicNode):
    pass


class IdentifierNode(ExpressionNode):
    def __init__(self, symbol, subgroup=None, isGlobal=False):
        self.symbol = symbol
        self.subgroup = subgroup
        self.isGlobal = isGlobal


class UnaryNode(ExpressionNode):
    pass


class NegNode(UnaryNode):
    def __init__(self, expression):
        self.expression = expression


class GlobalNode(ExpressionNode):
    def __init__(self, value):
        self.value = value
