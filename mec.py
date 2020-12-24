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
    'mec', 'meczada', 'loop', 'se', 'senao', 'funcao', 'mostrar', 'vale', 'pprt', 'falso', 'vdd'
)

tokens = keywords + (
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING',
    'ID', 'NEWLINE', 'COMMENT', 'LBRACES', 'RBRACES'
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
t_LBRACES = r'\{'
t_RBRACES = r'\}'
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
        # print('program : statement ->', p[0], p[1])
        p[0] = []
        p[0] = p[1]
    elif len(p) == 3:
        # print('program : program statement ->', p[0], p[1], p[2])
        # if p[1] and not p[2]:
        #     print('entrou so p1')
        #     p[0] = p[1]

        # if p[2] and not p[1]:
        #     print('entrou so p2')
        #     p[0] = p[2]

        if p[1] and p[2]:
            # print('entrou p1 e p2')
            if type(p[1]) == tuple:
                # print('tupla')
                p[0] = [p[1], p[2]]
            elif type(p[1]) == list:
                # print('lista')
                p[1].append(p[2])
                p[0] = p[1]

    else:
        p[0] = []
    # print(p[0])
    # print('------------------------------------------------')
    # print('------------------------------------------------')


def p_empty(p):
    'empty :'
    pass


def p_statement_assign(p):
    "statement : mec ID vale expression NEWLINE"
    ID = p[2]
    if ID in constants:
        raise ("Constante já declarada")
    names[ID] = p[4]
    p[0] = ('empty',)


def p_statement_constant(p):
    '''statement : meczada ID vale expression 
                 | meczada ID vale expression NEWLINE'''
    ID = p[2]
    if ID in constants:
        raise ("Constante já declarada")
    constants[ID] = p[4]
    p[0] = ('empty',)


def p_statement_reassign(p):
    '''statement : ID vale expression 
                 | ID vale expression NEWLINE'''
    ID = p[1]
    if ID in constants:
        raise ("Constante já declarada")
    names[ID] = p[3]
    p[0] = ('empty',)


# def p_statement_expr(p):
#     '''statement : empty'''
#     pass


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
    p[0] = ('mostrar', p[3])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | cond '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]


def p_condicao(p):
    '''cond : falso 
            | vdd
            | expression LT expression
            | expression LE expression
            | expression GT expression
            | expression GE expression
            | expression EQUALS EQUALS expression
            '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        op = p[2]
        if op == '<':
            p[0] = p[1] < p[3]
        elif op == '<=':
            p[0] = p[1] <= p[3]
        elif op == '>':
            p[0] = p[1] > p[3]
        elif op == '>=':
            p[0] = p[1] >= p[3]
        elif op == '==':
            p[0] = p[1] == p[3]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_if_statement(p):
    '''
    statement : se expression LBRACES program RBRACES NEWLINE
    '''
    if p[2]:
        p[0] = p[4]
    else:
        p[0] = ('empty')


def p_if_statement_newline(p):
    '''
    statement : se expression LBRACES NEWLINE program RBRACES NEWLINE
    '''
    if p[2]:
        p[0] = p[5]
    else:
        p[0] = ('empty')


def p_if_statement_newline_else(p):
    '''
    statement : se expression LBRACES NEWLINE program RBRACES senao LBRACES NEWLINE program RBRACES NEWLINE
    '''
    if p[2]:
        p[0] = p[5]
    else:
        p[0] = p[10]


def p_if_statement_newline_else_newline(p):
    '''
    statement : se expression LBRACES NEWLINE program RBRACES NEWLINE senao LBRACES NEWLINE program RBRACES NEWLINE
    '''
    if p[2]:
        p[0] = p[5]
    else:
        p[0] = p[11]


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


def interp(prog):
    for command in prog:
        if type(command) == list:
            interp(command)
        elif command[0] == 'mostrar':
            print(command[1])


if len(sys.argv) == 2:
    if ".mec" not in sys.argv[1]:
        print("Arquivo não suportado!")
        exit(1)
    with open(sys.argv[1]) as f:
        data = f.read()
    prog = parser.parse(data, debug=0)
    print('FINAL', prog)
    interp(prog)
    try:
        pass
    except:
        print("Não foi possivel criar o parser!")
