import ply.lex as lex

class Lexer:
    tokens = [
        'SYMBOL', # A single letter
        'NUMBER', # An integer or decimal
        'MACRO', # LaTex macros
        'PLUS', # +
        'MINUS', # -
        'FRAC', # Special case of macro that works as division
        'STAR', # *
        'EQUAL', # =
        'OPAR', # (
        'CPAR', # )
        'OCUR', # {
        'CCUR', # }
        'UNDER', # _
        'DIF', # Symbol and macro used in the differential (d or \partial)
        'LBREAK', # \\
    ]

    def __init__(self):
        pass

    def build(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self,text):
        self.lexer.input(text)
        for t in self.lexer:
            yield t

    t_NUMBER = r'\d+(\.\d*)?'
    def t_SYMBOL(self, t): 
        r'[a-zA-Z]'
        if t.value == 'd':
            t.type = 'DIF'
        return t

    def t_MACRO(self, t):
        r'\\[a-zA-Z]+'
        t.value = t.value[1:]
        if t.value.lower() == 'frac':
            t.type ='FRAC'
        elif t.value.lower() == 'cdot':
            t.value = '*'
            t.type = 'STAR'
        elif t.value == 'partial':
            t.type = 'DIF'
        return t

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_EQUAL = r'='
    t_OPAR = r'\('
    t_CPAR = r'\)'
    t_OCUR =  r'{'
    t_CCUR = r'}'
    t_UNDER = r'_'
    t_LBREAK = r'\\\\'
    t_ignore = ' \t\r\n'
