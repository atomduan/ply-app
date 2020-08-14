#!/usr/local/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

from sql_lexer import *
tokens = sql_lexer.tokens

symbols={"LALALAL":[123,1234]}

def p_sql(t):
    '''sql : statement_list'''
    print("PARSE SUCCESS...")
    pass

def p_sql_empty(t):
    '''sql :'''
    pass

def p_statement_list_1(t):
    '''statement_list : statement SEMI'''
    pass

def p_statement_list_2(t):
    '''statement_list : statement_list statement SEMI'''
    pass

def p_statement(t):
    '''statement : select_stmt'''
    pass

def p_select_stmt(t):
    '''select_stmt : SELECT selection from_clause where_clause'''
    pass

def p_selection_1(t):
    '''selection : scalar_exp_list'''
    pass

def p_scalar_exp_list_1(t):
    '''scalar_exp_list : scalar_exp'''
    pass

def p_scalar_exp_list_2(t):
    '''scalar_exp_list : scalar_exp_list COMMA scalar_exp'''
    pass

def p_from_clause(t):
    '''from_clause : FROM table_ref_list'''
    pass

def p_where_clause(t):
    '''where_clause : WHERE search_condition'''
    pass

def p_where_clause_empty(t):
    '''where_clause :'''
    pass

def p_table_ref_list_1(t):
    '''table_ref_list : table_ref'''
    pass

def p_table_ref_list_2(t):
    '''table_ref_list : table_ref_list COMMA table_ref'''
    pass

def p_table_ref(t):
    '''table_ref : name_ref'''
    pass

def p_search_condition_1(t):
    '''search_condition : predicate OR predicate'''
    pass 

def p_search_condition_2(t):
    '''search_condition : predicate AND predicate'''
    pass 

def p_search_condition_4(t):
    '''search_condition : predicate'''
    pass

def p_predicate_1(t):
    '''predicate : LP predicate RP'''
    pass

def p_predicate_2(t):
    '''predicate : comparison_predicate'''
    pass

def p_comparison_predicate(t):
    '''comparison_predicate : scalar_exp EQ scalar_exp'''
    pass

def p_scalar_exp_8(t):
    '''scalar_exp : scalar_unit'''
    pass

def p_scalar_unit_1(t):
    '''scalar_unit : NUM'''
    pass

def p_scalar_unit_2(t):
    '''scalar_unit : STR'''
    pass

def p_scalar_unit_3(t):
    '''scalar_unit : name_ref'''
    pass

def p_name_ref_1(t):
    '''name_ref : ID'''
    pass 

def p_error(t):
    lineno = t.lexer.lineno
    column = t.lexer.lexpos - t.lexer.linepos - len(t.value) + 1
    print("[SYNTAX ERROR] pos:[%d,%d], token:[%s]" % (lineno, column, t))

if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    yacc.parse(sys.stdin.read(), lxr, debug=False)
