from . import visitor
from .ast import *


class CodeGenerator(object):
    def __init__(self):
        self.interpolation = False

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(SystemNode)
    def visit(self, node: SystemNode, interpolation=False):
        self.interpolation = interpolation
        return [self.visit(e) for e in node.equations]

    @visitor.when(EquationNode)
    def visit(self, node: EquationNode):
        return f"{self.visit(node.differential)} = {self.visit(node.expression)}"

    @visitor.when(DifferentialNode)
    def visit(self, node: DifferentialNode):
        return f"d{self.visit(node.function)}d{self.visit(node.parameter)}"

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        return (
            f"{self.visit(node.left_expression)} + {self.visit(node.right_expression)}"
        )

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        return (
            f"{self.visit(node.left_expression)} - {self.visit(node.right_expression)}"
        )

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        return (
            f"{self.visit(node.left_expression)} * {self.visit(node.right_expression)}"
        )

    @visitor.when(NegNode)
    def visit(self, node: NegNode):
        return f"-{self.visit(node.expression)}"

    @visitor.when(FractionNode)
    def visit(self, node: FractionNode):
        return f"({self.visit(node.left_expression)}) / ({self.visit(node.right_expression)})"

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode):
        return node.value

    @visitor.when(SymbolNode)
    def visit(self, node: SymbolNode):
        if self.interpolation:
            return "{" + node.value + "}"
        return node.value

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode):
        if node.subgroup:
            result = f"{self.visit(node.symbol)}_{self.visit(node.subgroup)}"
        else:
            result = self.visit(node.symbol)

        if self.interpolation:
            result = "{" + result + "}"

        return result

    @visitor.when(GlobalNode)
    def visit(self, node: GlobalNode):
        result = self.visit(node.value)
        if self.interpolation:
            result = result[:1] + "_" + result[1:]

        return result

    @visitor.when(ParenthesisNode)
    def visit(self, node: ParenthesisNode):
        return f"({self.visit(node.expression)})"
