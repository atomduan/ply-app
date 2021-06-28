#!/usr/bin/env python3

# https://www.dabeaz.com/ply/ply.html#ply_nn21

import sys
import ply.lex as lex

last_line_pos = 0

reserved = ['SELECT', 'FROM', 'WHERE', 'OR', 'AND']

#output directly as literial token, do not need to define t_* rules
literals = [';', ',', '=', '(', ')', '+', '-', '*', '/']

tokens = [ 'ID', 'NUM', 'STR', ] + reserved

#start condition
states = (
    ('strsc', 'exclusive'),
)

t_strsc_ignore  = r''
t_ignore        = ' \t'

#string content
def t_begin_strsc(t):
    r'\"'
    t.lexer.begin('strsc')

def t_strsc_STRCTNT(t):
    r'[^\"]+'
    t.type = 'STR'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.linepos = t.lexer.lexpos + t.value.count('\n')
    return t

def t_strsc_end(t):
    r'\"'
    t.lexer.begin('INITIAL')

#comment content
def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.linepos = t.lexer.lexpos + t.value.count('\n')

def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1
    t.lexer.linepos = t.lexer.lexpos + t.value.count('\n')

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'NUM'
    return t

def t_ID(t):
    r'[a-zA-Z0-9_]+'
    if t.value.upper() in reserved:
        t.type = t.value = t.value.upper()
    else:
        t.type = 'ID'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.linepos = t.lexer.lexpos + len(t.value)

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

if __name__ == '__main__':
    import re
    lexer = lex.lex(reflags=re.IGNORECASE)
    data = sys.stdin.read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
