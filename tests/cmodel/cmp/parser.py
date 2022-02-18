import ply.yacc as yacc
from .lexer import Lexer
from .ast import *


class Parser:
    def __init__(self):
        self.tokens = Lexer.tokens

    def parse(self, text):
        self.lex = Lexer()
        self.lex.build()
        self.parser = yacc.yacc(module=self)
        result = self.parser.parse(text, lexer=self.lex.lexer)
        return result

    @staticmethod
    def p_system(p):
        "system : equation_list"
        p[0] = SystemNode(p[1])

    @staticmethod
    def p_equation_list_single(p):
        "equation_list : equation"
        p[0] = [p[1]]

    @staticmethod
    def p_equation_list_multi(p):
        "equation_list : equation LBREAK equation_list"
        p[0] = [p[1]] + p[3]

    @staticmethod
    def p_equation(p):
        "equation : differential EQUAL expression"
        p[0] = EquationNode(p[1], p[3])

    @staticmethod
    def p_differential(p):
        "differential : FRAC OCUR DIF identifier CCUR OCUR DIF identifier CCUR"
        p[0] = DifferentialNode(p[4], p[8])

    @staticmethod
    def p_fraction(p):
        "fraction : FRAC OCUR expression CCUR OCUR expression CCUR"
        p[0] = FractionNode(p[3], p[6])

    @staticmethod
    def p_expression(p):
        "expression : arith"
        p[0] = p[1]

    @staticmethod
    def p_neg_expression(p):
        "expression : MINUS expression"
        p[0] = NegNode(p[2])

    @staticmethod
    def p_arith_term(p):
        "arith : term"
        p[0] = p[1]

    @staticmethod
    def p_arith_plus(p):
        "arith : arith PLUS term"
        p[0] = PlusNode(p[1], p[3])

    @staticmethod
    def p_arith_minus(p):
        "arith : arith MINUS term"
        p[0] = MinusNode(p[1], p[3])

    # @staticmethod
    # def p_term_fac(p):
    #     'term : factor'
    #     p[0] = p[1]

    @staticmethod
    def p_term_star(p):
        "term : term STAR factor"
        p[0] = StarNode(p[1], p[3])

    @staticmethod
    def p_term_idlist(p):
        "term : idlist"
        p[0] = p[1]

    @staticmethod
    def p_idlist_multi(p):
        "idlist : factor idlist"
        p[0] = StarNode(p[1], p[2])

    @staticmethod
    def p_idlist_single(p):
        "idlist : factor"
        p[0] = p[1]

    @staticmethod
    def p_factor_fraction(p):
        "factor : fraction"
        p[0] = p[1]

    @staticmethod
    def p_factor_num(p):
        "factor : NUMBER"
        p[0] = NumberNode(p[1])

    @staticmethod
    def p_factor_pexpression(p):
        "factor : OPAR expression CPAR"
        p[0] = ParenthesisNode(p[2])

    @staticmethod
    def p_factor_symbol(p):
        "factor : identifier"
        p[0] = p[1]

    @staticmethod
    def p_factor_symbol_global(p):
        "factor : PERCENT identifier"
        p[0] = GlobalNode(p[2])

    @staticmethod
    def p_symbol_atom(p):
        "identifier : atom"
        p[0] = p[1]

    @staticmethod
    def p_atom_symbol(p):
        "atom : SYMBOL"
        p[0] = SymbolNode(p[1])

    @staticmethod
    def p_atom_macro(p):
        "atom : MACRO"
        p[0] = SymbolNode(p[1])

    @staticmethod
    def p_symbol_comp(p):
        "identifier : atom UNDER atom"
        p[0] = IdentifierNode(p[1], p[3])

    @staticmethod
    def p_symbol_comp1(p):
        "identifier : atom UNDER NUMBER"
        p[0] = IdentifierNode(p[1], NumberNode(p[3]))

    @staticmethod
    def p_symbol_comp2(p):
        "identifier : atom UNDER OCUR identifier CCUR"
        p[0] = IdentifierNode(p[1], p[4])
