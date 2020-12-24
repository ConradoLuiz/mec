import ply.yacc as yacc
import ply.lex as lex
import sys

'''
keywords = (
    'LET', 'READ', 'DATA', 'PRINT', 'GOTO', 'IF', 'THEN', 'FOR', 'NEXT', 'TO', 'STEP',
    'END', 'STOP', 'DEF', 'GOSUB', 'DIM', 'REM', 'RETURN', 'RUN', 'LIST', 'NEW'
)
'''
keywords = (
    'mec', 'meczada', 'loop', 'se', 'senao', 'funcao', 'mostrar', 'voltar'
)

tokens = keywords + (
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING',
    'ID', 'NEWLINE', 'COMMENT'
)

t_ignore = ' \t'


def t_COMMENT(t):
    r'\# .*'
    return t


def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value
    return t


t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

names = {}
constants = {}


def p_program(p):
    '''program : program statement
               | statement'''
    if len(p) == 2 and p[1]:
        p[0] = {}
        line, stat = p[1]
        p[0][line] = stat
    elif len(p) == 3:
        p[0] = p[1]
        if not p[0]:
            p[0] = {}
        if p[2]:
            line, stat = p[2]
            p[0][line] = stat


def p_statement_assign(p):
    "statement : mec ID EQUALS expression NEWLINE"
    ID = p[2]
    if ID in constants:
        raise ("Constante já declarada")
    names[ID] = p[4]


def p_statement_constant(p):
    '''statement : meczada ID EQUALS expression 
                 | meczada ID EQUALS expression NEWLINE'''
    ID = p[2]
    if ID in constants:
        raise ("Constante já declarada")
    constants[ID] = p[4]


def p_statement_reassign(p):
    '''statement : ID EQUALS expression 
                 | ID EQUALS expression NEWLINE'''
    ID = p[1]
    if ID in constants:
        raise ("Constante já declarada")
    names[ID] = p[3]


def p_statement_expr(p):
    '''statement : expression
                 | expression NEWLINE'''
    # print(p[1])
    pass


def p_statement_comment(p):
    '''statement : COMMENT command
                 | COMMENT command NEWLINE'''
    pass


def p_statement_command(p):
    '''statement : command
                 | command NEWLINE'''
    p[0] = p[1]


def p_command_mostrar(p):
    '''command : mostrar LPAREN expression RPAREN
               | mostrar LPAREN expression RPAREN NEWLINE'''
    print(p[3])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_int(p):
    "expression : INTEGER"
    p[0] = int(p[1])


def p_expression_float(p):
    "expression : FLOAT"
    p[0] = float(p[1])


def p_expression_string(p):
    "expression : STRING"
    p[0] = str(p[1]).strip('"')


def p_expression_name(p):
    "expression : ID"
    ID = p[1]
    try:
        if ID in constants:
            p[0] = constants[ID]
            return
        p[0] = names[ID]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Erro de sintaxe em'%s'" % p.value)
    # else:
    #     print("Erro de sintaxe em EOF")


parser = yacc.yacc()

if len(sys.argv) == 2:
    if ".mec" not in sys.argv[1]:
        print("Arquivo não suportado!")
        exit(1)
    with open(sys.argv[1]) as f:
        data = f.read()
    prog = parser.parse(data, debug=0)
    try:
        # print('FINAL', prog)
        pass
    except:
        print("Não foi possivel criar o parser!")
