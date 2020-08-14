#!/usr/local/bin/python3

import sys
import json
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

from sql_lexer import *
tokens = sql_lexer.tokens

# symbol table
symbols={}

# Normally, the first rule found in a yacc 
# specification defines the starting grammar 
# rule (top level rule). To change this, simply 
# supply a start specifier in your file. 
start = 'sql'

def p_sql(p):
    '''sql : statement_list'''
    symbols['sql'] = {
            'statement_list' : sym_join('statement_list'),
            }
    pass

def p_sql_empty(p):
    '''sql :'''
    symbols['sql'] = {}
    pass

def p_statement_list_1(p):
    '''statement_list : statement SEMI'''
    symbols['statement_list'] = [
            sym_join('statement'),
            ]
    pass

def p_statement_list_2(p):
    '''statement_list : statement_list statement SEMI'''
    symbols['statement_list'].append(sym_join('statement'))
    pass

def p_statement(p):
    '''statement : select_stmt'''
    symbols['statement'] = {
            'select_stmt' : sym_join('select_stmt'),
            }
    pass

def p_select_stmt(p):
    '''select_stmt : SELECT selection from_clause where_clause'''
    symbols['select_stmt'] = {
            'selection'     : sym_join('selection'),
            'from_clause'   : sym_join('from_clause'),
            'where_clause'  : sym_join('where_clause'),
            }
    pass

def p_selection_1(p):
    '''selection : scalar_exp_list'''
    symbols['selection'] = {
            'scalar_exp_list' : sym_join('scalar_exp_list'),
            }
    pass

def p_scalar_exp_list_1(p):
    '''scalar_exp_list : scalar_exp'''
    symbols['scalar_exp_list'] = [
            sym_join('scalar_exp'),
            ]
    pass

def p_scalar_exp_list_2(p):
    '''scalar_exp_list : scalar_exp_list COMMA scalar_exp'''
    symbols['scalar_exp_list'].append(sym_join('scalar_exp'))
    pass

def p_from_clause(p):
    '''from_clause : FROM table_ref_list'''
    symbols['from_clause'] = {
            'table_ref_list' : sym_join('table_ref_list'),
            }
    pass

def p_where_clause(p):
    '''where_clause : WHERE search_condition'''
    symbols['where_clause'] = {
            'search_condition' : sym_join('search_condition'),
            }
    pass

def p_where_clause_empty(p):
    '''where_clause :'''
    symbols['where_clause'] = {}
    pass

def p_table_ref_list_1(p):
    '''table_ref_list : table_ref'''
    symbols['table_ref_list'] = [
            sym_join('table_ref'),
            ]
    pass

def p_table_ref_list_2(p):
    '''table_ref_list : table_ref_list COMMA table_ref'''
    symbols['table_ref_list'].append(sym_join('table_ref'))
    pass

def p_table_ref(p):
    '''table_ref : name_ref'''
    symbols['table_ref'] = {
            'name_ref' : sym_join('name_ref'),
            }
    pass

def p_search_condition_1(p):
    '''search_condition : predicate seen_predicate OR predicate'''
    symbols['search_condition'] = {
            'predicate-l' : sym_join('seen_predicate'),
            'predicate-r' : sym_join('predicate'),
            'type' : 'OR',
            }
    pass 

def p_search_condition_2(p):
    '''search_condition : predicate seen_predicate AND predicate'''
    symbols['search_condition'] = {
            'predicate-l' : sym_join('seen_predicate'),
            'predicate-r' : sym_join('predicate'),
            'type' : 'AND',
            }
    pass 

#Embedded Actions seen_${rule}
def p_seen_predicate(p):
    '''seen_predicate :'''
    symbols['seen_predicate'] = sym_join('predicate')
    pass

def p_search_condition_4(p):
    '''search_condition : predicate'''
    symbols['search_condition'] = {
            'predicate' : sym_join('predicate'),
            'type' : '',
            }
    pass

def p_predicate_1(p):
    '''predicate : LP predicate RP'''
    pass

def p_predicate_2(p):
    '''predicate : comparison_predicate'''
    symbols['predicate'] = {
            'comparison_predicate' : sym_join('comparison_predicate')
            }
    pass

def p_comparison_predicate(p):
    '''comparison_predicate : scalar_exp seen_scalar_exp EQ scalar_exp'''
    symbols['comparison_predicate'] = {
            'scalar_exp_l' : sym_join('seen_scalar_exp'),
            'scalar_exp_r' : sym_join('scalar_exp'),
            'type' : 'EQ',
            }
    pass

#Embedded Actions seen_${rule}
def p_seen_scalar_exp (p):
    '''seen_scalar_exp :'''
    symbols['seen_scalar_exp'] = sym_join('scalar_exp')
    pass

def p_scalar_exp_8(p):
    '''scalar_exp : scalar_unit'''
    symbols['scalar_exp'] = {
            'scalar_unit' : sym_join('scalar_unit'),
            }
    pass

def p_scalar_unit_1(p):
    '''scalar_unit : NUM'''
    symbols['scalar_unit'] = {
            'type'  : 'NUM',
            'token' : p.slice[1].value,
            }
    pass

def p_scalar_unit_2(p):
    '''scalar_unit : STR'''
    symbols['scalar_unit'] = {
            'type'  : 'STR',
            'token' : p.slice[1].value,
            }
    pass

def p_scalar_unit_3(p):
    '''scalar_unit : name_ref'''
    symbols['scalar_unit'] = {
            'type'      : 'name_ref',
            'name_ref'  : sym_join('name_ref'),
            }
    pass

def p_name_ref_1(p):
    '''name_ref : ID'''
    symbols['name_ref'] = {
            'type'  : 'ID',
            'token' : p.slice[1].value,
            }
    pass 

def p_error(t):
    lineno = t.lexer.lineno
    column = t.lexer.lexpos - t.lexer.linepos - len(t.value) + 1
    print("[SYNTAX ERROR] pos:[%d,%d], token:[%s]" % (lineno, column, t))

def sym_join(key):
    ref = symbols[key]
    del symbols[key]
    return ref

if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    yacc.parse(sys.stdin.read(), lxr, debug=False)
    json_str = json.dumps(symbols)
    print(json_str)
