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
    'mec', 'loop', 'se', 'senao', 'funcao', 'mostrar', 'voltar'
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
    r'[a-z][a-zA-Z0-9]*'
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


lex.lex(debug=1)

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)

names = {}


def p_statement_assign(p):
    "statement : mec ID EQUALS expression NEWLINE"
    print('assign', p[2], p[3], p[4])
    names[p[2]] = p[4]
    print(names)


def p_statement_expr(p):
    'statement : expression'
    print('mostrou', p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : INTEGER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = names[p[1]]
        print(names)
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

if len(sys.argv) == 2:
    if ".mec" not in sys.argv[1]:
        print("Arquivo não suportado!")
        exit(1)
    with open(sys.argv[1]) as f:
        data = f.read()
    try:
        prog = yacc.parse(data)
        print('FINAL', prog)
    except:
        print("Não foi possivel criar o parser!")
        pass
