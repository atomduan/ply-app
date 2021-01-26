#!/usr/bin/env python3

import sys
import json
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

from sql_lexer import *

tokens = sql_lexer.tokens


# Normally, the first rule found in a yacc 
# specification defines the starting grammar 
# rule (top level rule). To change this, simply 
# supply a start specifier in your file. 
start = 'sql'

def p_sql(p):
    '''sql : statement_list
           | empty '''
    p[0] = p[1]


def p_statement_list(p):
    '''statement_list : statement ';'
                      | statement_list statement ';' '''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1]
        p[0].extend(p[2])


def p_statement(p):
    '''statement : select_stmt '''
    p[0] = p[1]


def p_select_stmt(p):
    '''select_stmt : SELECT selection from_clause where_clause '''
    # loading table
    p[0] = p[3]
    # loading selection
    p[0].extend(p[2])
    # loading recode
    p[0].append('LDTB EMPTY REG_TLB_TMP') 
    p[0].append('F_CHECK_LOOP:')
    p[0].append('LTNX REG_TLB "F_EMPTY"') 
    p[0].extend(p[4])
    p[0].append('CHKN R_CMP 0 "F_CHECK_LOOP"') 
    # trunk fileds
    p[0].append('FLRC REG_RCD') 
    p[0].append('ADRC REG_RCD REG_TLB_TMP') 
    p[0].append('JUMP "F_CHECK_LOOP"') 
    p[0].append('F_EMPTY:') 
    p[0].append('MVTB REG_TLB_TMP REG_TLB')


def p_selection(p):
    '''selection : scalar_exp_list '''
    p[0] = ['MREG'+' '+'REG_SEL'+' '+'"'+str(p[1])+'"']


def p_scalar_exp_list(p):
    '''scalar_exp_list : scalar_exp
                       | scalar_exp_list ',' scalar_exp '''
    if len(p) == 2:
        p[0] = str(p[1])
    elif len(p) == 4:
        p[0] = ''.join([p[1], ',', p[3]])


def p_from_clause(p):
    '''from_clause : FROM table_ref '''
    p[0] = [''.join(['LDTB', ' "', p[2], '" ', 'REG_TLB'])]


def p_where_clause(p):
    '''where_clause : WHERE search_condition
                    | empty '''
    if len(p) == 3:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = ['EMPI']


def p_table_ref(p):
    '''table_ref : name_ref '''
    p[0] = p[1]


def p_search_condition(p):
    '''search_condition : predicate
                        | predicate OR predicate
                        | predicate AND predicate '''
    if len(p) == 2: 
        p[0] = p[1]
    elif p[2] == 'OR':
        p[0] = p[1]
        p[0].append('CHEK R_CMP 0 "F_FIN"') 
        p[0].extend(p[1]) 
        p[0].append('F_FIN:') 
    elif p[2] == 'AND':
        p[0] = p[1]
        p[0].append('CHKN R_CMP 0 "F_FIN"') 
        p[0].extend(p[1]) 
        p[0].append('F_FIN:') 


def p_predicate(p):
    '''predicate : '(' predicate ')'
                 | scalar_exp '=' scalar_exp '''
    if len(p) == 4: 
        p[0] = ['COMP'+' '+str(p[1])+' '+str(p[3])]


def p_scalar_exp(p):
    '''scalar_exp : scalar_unit '''
    p[0] = p[1]


def p_name_ref(p):
    '''name_ref : scalar_unit ''' 
    p[0] = str(p[1])


def p_scalar_unit(p):
    '''scalar_unit : NUM
                   | STR
                   | ID '''
    p[0] = str(p[1])


def p_empty(p):
    '''empty : '''


def p_error(t):
    lineno = t.lexer.lineno
    column = t.lexer.lexpos - t.lexer.linepos - len(t.value) + 1
    print("[SYNTAX ERROR] pos:[%d,%d], token:[%s]" % (lineno, column, t))


if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    sql = yacc.parse(sys.stdin.read(), lxr, debug=False)
    if sql is not None:
        for instruction in sql:
            print(instruction)
