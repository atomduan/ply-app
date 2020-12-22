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
    instrus['sql'] = instrus_join('statement_list')
    pass

def p_sql_empty(p):
    '''sql :'''
    instrus['sql'] = ['EMPI']
    pass

def p_statement_list_1(p):
    '''statement_list : statement SEMI'''
    instrus['statement_list'] = instrus_join('statement')
    pass

def p_statement_list_2(p):
    '''statement_list : statement_list statement SEMI'''
    tmp_instrus = instrus_join('statement_list')
    tmp_instrus.append(instrus_join('statement')) 
    instrus['statement_list'] = tmp_instrus
    pass

def p_statement(p):
    '''statement : select_stmt'''
    instrus['statement'] = instrus_join('select_stmt')
    pass

def p_select_stmt(p):
    '''select_stmt : SELECT selection from_clause where_clause'''
    # loading table
    tmp_instrus = instrus_join('from_clause')
    # loading selection
    tmp_instrus.extend(instrus_join('selection'))
    # loading recode
    tmp_instrus.append('LDTB EMPTY REG_TLB_TMP') 
    tmp_instrus.append('F_CHECK_LOOP:')
    tmp_instrus.append('LTNX REG_TLB "F_EMPTY"') 
    tmp_instrus.extend(instrus_join('where_clause'))
    tmp_instrus.append('CHKN R_CMP 0 "F_CHECK_LOOP"') 
    # trunk fileds
    tmp_instrus.append('FLRC REG_RCD') 
    tmp_instrus.append('ADRC REG_RCD REG_TLB_TMP') 
    tmp_instrus.append('JUMP "F_CHECK_LOOP"') 
    tmp_instrus.append('F_EMPTY:') 
    tmp_instrus.append('MVTB REG_TLB_TMP REG_TLB')
    instrus['select_stmt'] = tmp_instrus
    pass

def p_selection_1(p):
    '''selection : scalar_exp_list'''
    instrus['selection'] = ['MREG'+' '+'REG_SEL'+' '+'"'+str(p[1])+'"']
    pass

def p_scalar_exp_list_1(p):
    '''scalar_exp_list : scalar_exp'''
    p[0] = str(p[1])
    pass

def p_scalar_exp_list_2(p):
    '''scalar_exp_list : scalar_exp_list COMMA scalar_exp'''
    p[0] = str(p[1])+','+str(p[3])
    pass

def p_from_clause(p):
    '''from_clause : FROM table_ref'''
    table_name = p[2]
    instrus['from_clause'] = ['LDTB'+' '+table_name+' '+'REG_TLB']
    pass

def p_where_clause(p):
    '''where_clause : WHERE search_condition'''
    instrus['where_clause'] = instrus_join('search_condition');
    pass

def p_where_clause_empty(p):
    '''where_clause :'''
    instrus['where_clause'] = ['EMPI']
    pass

def p_table_ref(p):
    '''table_ref : name_ref'''
    p[0] = p[1]

def p_search_condition_1(p):
    '''search_condition : predicate'''
    instrus['search_condition'] = instrus_join('predicate')
    pass

def p_search_condition_2(p):
    '''search_condition : predicate seen_predicate OR predicate'''
    tmp_instrus = instrus_join('seen_predicate')
    tmp_instrus.append('CHEK R_CMP 0 "F_FIN"') 
    tmp_instrus.extend(instrus_join('predicate')) 
    tmp_instrus.append('F_FIN:') 
    instrus['search_condition'] = tmp_instrus
    pass 

def p_search_condition_3(p):
    '''search_condition : predicate seen_predicate AND predicate'''
    tmp_instrus = instrus_join('seen_predicate')
    tmp_instrus.append('CHKN R_CMP 0 "F_FIN"') 
    tmp_instrus.extend(instrus_join('predicate')) 
    tmp_instrus.append('F_FIN:') 
    instrus['search_condition'] = tmp_instrus
    pass 

#Embedded Actions seen_${rule}
def p_seen_predicate(p):
    '''seen_predicate :'''
    instrus['seen_predicate'] = instrus_join('predicate')
    pass

def p_predicate_1(p):
    '''predicate : LP predicate RP'''
    instrus['predicate'] = instrus_join('predicate')
    pass

def p_predicate_2(p):
    '''predicate : comparison_predicate'''
    instrus['predicate'] = instrus_join('comparison_predicate')
    pass

def p_comparison_predicate(p):
    '''comparison_predicate : scalar_exp EQ scalar_exp'''
    instrus['comparison_predicate'] = ['COMP'+' '+str(p[1])+' '+str(p[3])]
    pass

def p_scalar_exp_8(p):
    '''scalar_exp : scalar_unit'''
    p[0] = p[1]
    pass

def p_scalar_unit_1(p):
    '''scalar_unit : NUM'''
    p[0] = int(p[1])
    pass

def p_scalar_unit_2(p):
    '''scalar_unit : STR'''
    p[0] = str(p[1])
    pass

def p_scalar_unit_3(p):
    '''scalar_unit : name_ref'''
    p[0] = p[1]
    pass

def p_scalar_unit_4(p):
    '''scalar_unit : ASTER'''
    p[0] = p[1]
    pass

def p_name_ref_1(p):
    '''name_ref : ID'''
    p[0] = str(p[1])
    pass

def p_error(t):
    lineno = t.lexer.lineno
    column = t.lexer.lexpos - t.lexer.linepos - len(t.value) + 1
    print("[SYNTAX ERROR] pos:[%d,%d], token:[%s]" % (lineno, column, t))
    pass

def instrus_join(key):
    tmp_instrus = instrus[key]
    del instrus[key]
    return tmp_instrus; 

if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    yacc.parse(sys.stdin.read(), lxr, debug=False)
    for ins in instrus['sql']:
        print(ins)
