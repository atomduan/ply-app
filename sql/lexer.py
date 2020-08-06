#!/usr/local/bin/python3

#https://www.dabeaz.com/ply/ply.html#ply_nn21

import sys
import lex

tokens = (
    'COMPARISON',
    'INTNUM',
    'STRING',
    'OTHER',
    'SELECT',
    'FROM',
    'WHERE',
    'LIKE',
    'AS',
)

states = (
    ('strsc','exclusive'),
)

t_OTHER         = r'.'
t_ignore        = ' \t'
t_strsc_ignore  = r''

def t_begin_strsc(t):
    r'\"'
    t.lexer.begin('strsc')

def t_strsc_STRCTNT(t):
    r'[^\"]+'
    t.type = 'STRING'
    return t

def t_strsc_end(t):
    r'\"'
    t.lexer.begin('INITIAL')

def t_SELECT(t):
    r'(?i)SELECT'
    t.type = 'SELECT'
    return t

def t_FROM(t):
    r'(?i)FROM'
    t.type = 'FROM'
    return t

def t_WHERE(t):
    r'(?i)WHERE'
    t.type = 'WHERE'
    return t

def t_LIKE(t):
    r'(?i)LIKE'
    t.type = 'LIKE'
    return t

def t_AS(t):
    r'(?i)AS'
    t.type = 'AS'
    return t

def t_COMPARISON(t):
    r'(=|<>|<|>|<=|>=)'
    t.type = 'COMPARISON'
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)    
    t.type = 'INTNUM'
    return t

def t_STRING(t):
    r'[a-zA-Z0-9_-]+'
    t.type = 'STRING'
    return t

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

if __name__ == '__main__':
    lexer = lex.lex()
    data = sys.stdin.read()

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
