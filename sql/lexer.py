#!/usr/local/bin/python3

import sys
import lex

tokens = (
    'CMP',
    'INTNUM',
    'STRING',
    'OTHER',
)

t_OTHER     = r'.'

def t_CMP(t):
    r'(=|<>|<|>|<=|>=)'
    t.type = 'CMP'
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

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
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
