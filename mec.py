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
    'mec', 'meczada', 'loopzin', 'se', 'senao', 'funcao', 'mostrar', 'vale', 'pprt', 'falso', 'vdd'
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
        p[0] = []
        p[0] = p[1]
    elif len(p) == 3:
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
    '''statement : mec ID vale expression NEWLINE
                 | mec ID vale expression '''
    ID = p[2]
    if ID in constants:
        raise ("Constante já declarada")
    # names[ID] = p[4]
    p[0] = ('mec', ID, p[4])


def p_statement_constant(p):
    '''statement : meczada ID vale expression
                 | meczada ID vale expression NEWLINE'''
    ID = p[2]
    if ID in constants:
        raise ("Constante já declarada")
    # constants[ID] = p[4]
    p[0] = ('meczada', ID, p[4])


def p_statement_reassign(p):
    '''statement : ID vale expression
                 | ID vale expression NEWLINE'''
    ID = p[1]
    if ID in constants:
        raise ("Constante já declarada")
    # names[ID] = p[3]
    p[0] = ('mec', ID, p[3])


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
        p[0] = ('expr', p[1], p[2], p[3])


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
        p[0] = ('cond', ('bool', p[1]))
    elif len(p) == 4:
        p[0] = ('cond', p[1], p[2], p[3])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_if_statement(p):
    '''
    statement : se expression LBRACES program RBRACES NEWLINE
    '''
    # if p[2]:
    #     p[0] = p[4]
    # else:
    #     p[0] = ('empty')
    p[0] = ('if', p[2], p[4])


def p_if_statement_newline(p):
    '''
    statement : se expression LBRACES NEWLINE program RBRACES NEWLINE
    '''
    # if p[2]:
    #     p[0] = p[5]
    # else:
    #     p[0] = ('empty')
    p[0] = ('if', p[2], p[5])


def p_if_statement_newline_else(p):
    '''
    statement : se expression LBRACES NEWLINE program RBRACES senao LBRACES NEWLINE program RBRACES NEWLINE
    '''
    # if p[2]:
    #     p[0] = p[5]
    # else:
    #     p[0] = p[10]
    p[0] = ('if', p[2], p[5], p[10])


def p_if_statement_newline_else_newline(p):
    '''
    statement : se expression LBRACES NEWLINE program RBRACES NEWLINE senao LBRACES NEWLINE program RBRACES NEWLINE
    '''
    # if p[2]:
    #     p[0] = p[5]
    # else:
    #     p[0] = p[11]
    p[0] = ('if', p[2], p[5], p[11])


def p_loop(p):
    '''
    command : loopzin LPAREN statement SEMI cond SEMI statement RPAREN LBRACES NEWLINE program RBRACES
    '''
    p[0] = ('loop', p[3], p[5], p[7], p[11])


def p_expression_int(p):
    "expression : INTEGER"
    p[0] = ('int', int(p[1]))


def p_expression_float(p):
    "expression : FLOAT"
    p[0] = ('float', float(p[1]))


def p_expression_string(p):
    "expression : STRING"
    p[0] = ('str', str(p[1]).strip('"'))


def p_expression_name(p):
    "expression : ID"

    p[0] = ('getID', p[1])
    # try:
    #     if ID in constants:
    #         p[0] = constants[ID]
    #         return
    #     p[0] = names[ID]
    # except LookupError:
    #     print("Undefined name '%s'" % p[1])
    #     p[0] = 0


def p_error(p):
    if p:
        print("Erro de sintaxe em'%s'" % p.value)
    # else:
    #     print("Erro de sintaxe em EOF")


parser = yacc.yacc()


def mostrar(st, item):
    print(item)


def cond(st, lhs, op, rhs):
    result = False
    if op == '<':
        result = lhs < rhs
    elif op == '<=':
        result = lhs <= rhs
    elif op == '>':
        result = lhs > rhs
    elif op == '>=':
        result = lhs >= rhs
    elif op == '==':
        result = lhs == rhs
    return result


def boolCond(st, _bool):
    if _bool == 'vdd':
        return True
    return False


def expr(st, lhs, op, rhs):
    result = None
    if op == '+':
        result = lhs + rhs
    elif op == '-':
        result = lhs - rhs
    elif op == '*':
        result = lhs * rhs
    elif op == '/':
        result = lhs / rhs
    return result


def assign(st, ID, value):
    global names
    names[ID] = value


def assignConst(st, ID, value):
    global constants
    constants[ID] = value


def getID(st, ID):
    try:
        if ID in constants.keys():
            return constants[ID]
        elif ID in names.keys():
            return names[ID]
        raise "Variavel não existente"
    except:
        print("Variavel não existente")
        pass


def interp(prog):
    # print(prog)
    # print(names)
    for command in prog:
        inst = command[0]
        if type(command) == list:
            interp(command)
        elif inst == 'int' or inst == 'float' or inst == 'str' or inst == 'bool':
            return command[1]
        elif inst == 'mec':
            assign(command[0], command[1], interp([command[2]]))
        elif inst == 'meczada':
            assignConst(command[0], command[1], interp([command[2]]))
        elif inst == 'getID':
            return getID(*command)
        elif inst == 'mostrar':
            mostrar(command[0], interp([command[1]]))
        elif inst == 'expr':
            return expr(command[0], interp([command[1]]),
                        command[2], interp([command[3]]))
        elif inst == 'cond':
            if len(command) == 4:
                return cond(command[0], interp([command[1]]), command[2], interp([command[3]]))
            elif len(command) == 2:
                return boolCond(command[0], interp([command[1]]))
        elif inst == 'if':
            cond_inst = command[1]
            cond_result = interp([cond_inst])

            if len(command) == 3:
                if cond_result:
                    interp([command[2]])
            elif len(command) == 4:
                if cond_result:
                    interp([command[2]])
                else:
                    interp([command[3]])
        elif inst == 'loop':
            interp([command[1]])
            while interp([command[2]]):
                interp([command[4]])
                interp([command[3]])


if len(sys.argv) == 2:
    if ".mec" not in sys.argv[1]:
        print("Arquivo não suportado!")
        exit(1)
    with open(sys.argv[1]) as f:
        data = f.read()
    prog = parser.parse(data, debug=0)
    # print('FINAL', prog)
    interp(prog)
    try:
        pass
    except:
        print("Não foi possivel criar o parser!")
