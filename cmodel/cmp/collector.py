from . import visitor
from .ast import *
from .codegen import CodeGenerator


class CollectorVisitor:
    def __init__(self):
        self.sets = []
        self.variable = None
        self.parameters = set()
        self.generator = CodeGenerator()

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(SystemNode)
    def visit(self, node: SystemNode):
        for e in node.equations:
            self.visit(e)
        return self.sets, self.variable, self.parameters.difference(set(self.sets))
    
    @visitor.when(EquationNode)
    def visit(self, node : EquationNode):
        self.visit(node.differential)
        self.visit(node.expression)

    @visitor.when(DifferentialNode)
    def visit(self, node : DifferentialNode):
        self.sets.append(self.generator.visit(node.function))
        self.variable = self.generator.visit(node.parameter)

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)
    
    @visitor.when(NumberNode)
    def visit(self, node : NumberNode):
        pass

    @visitor.when(NegNode)
    def visit(self, node : NegNode):
        self.visit(node.expression)

    @visitor.when(SymbolNode)
    def visit(self, node: SymbolNode):
        self.parameters.add(node.value)

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode):
        self.parameters.add(self.generator.visit(node))

    @visitor.when(ParenthesisNode)
    def visit(self, node: ParenthesisNode):
        self.visit(node.expression)
