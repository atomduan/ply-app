#!/usr/bin/env python3

import sys
import json
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

from sql_lexer import *
from sql_handler import *

tokens = sql_lexer.tokens

instrus = {}

# Normally, the first rule found in a yacc 
# specification defines the starting grammar 
# rule (top level rule). To change this, simply 
# supply a start specifier in your file. 
start = 'sql'

def p_sql(p):
    '''sql : statement_list'''
    pass

def p_sql_empty(p):
    '''sql :'''
    pass

def p_statement_list_1(p):
    '''statement_list : statement SEMI'''
    pass

def p_statement_list_2(p):
    '''statement_list : statement_list statement SEMI'''
    pass

def p_statement(p):
    '''statement : select_stmt'''
    pass

def p_select_stmt(p):
    '''select_stmt : SELECT selection from_clause where_clause'''
    pass

def p_selection_1(p):
    '''selection : scalar_exp_list'''
    pass

def p_scalar_exp_list_1(p):
    '''scalar_exp_list : scalar_exp'''
    pass

def p_scalar_exp_list_2(p):
    '''scalar_exp_list : scalar_exp_list COMMA scalar_exp'''
    pass

def p_from_clause(p):
    '''from_clause : FROM table_ref'''
    table_name = p[2]
    inst = 'LDTB'+' '+table_name
    instrus['from_clause'] = inst
    pass

def p_where_clause(p):
    '''where_clause : WHERE search_condition'''
    pass

def p_where_clause_empty(p):
    '''where_clause :'''
    pass

def p_table_ref(p):
    '''table_ref : name_ref'''
    p[0] = p[1]

def p_search_condition_1(p):
    '''search_condition : predicate'''
    pass

def p_search_condition_2(p):
    '''search_condition : predicate OR predicate'''
    pass 

def p_search_condition_3(p):
    '''search_condition : predicate AND predicate'''
    pass 

def p_predicate_1(p):
    '''predicate : LP predicate RP'''
    pass

def p_predicate_2(p):
    '''predicate : comparison_predicate'''
    instrus['predicate'] = instrus['comparison_predicate']
    pass

def p_comparison_predicate(p):
    '''comparison_predicate : scalar_exp EQ scalar_exp'''
    inst = ['COMP'+' '+str(p[1])+' '+str(p[2])]
    instrus['comparison_predicate'] = inst

def p_scalar_exp_8(p):
    '''scalar_exp : scalar_unit'''
    p[0] = p[1]

def p_scalar_unit_1(p):
    '''scalar_unit : NUM'''
    p[0] = int(p[1])

def p_scalar_unit_2(p):
    '''scalar_unit : STR'''
    p[0] = str(p[1])

def p_scalar_unit_3(p):
    '''scalar_unit : name_ref'''
    p[0] = p[1]

def p_scalar_unit_4(p):
    '''scalar_unit : ASTER'''
    p[0] = p[1]

def p_name_ref_1(p):
    '''name_ref : ID'''
    p[0] = str(p[1])

def p_error(t):
    lineno = t.lexer.lineno
    column = t.lexer.lexpos - t.lexer.linepos - len(t.value) + 1
    print("[SYNTAX ERROR] pos:[%d,%d], token:[%s]" % (lineno, column, t))

def instrus_shift(key):
    tmp_instrus = instrus[key]
    instrus[key] = 

if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    yacc.parse(sys.stdin.read(), lxr, debug=False)
