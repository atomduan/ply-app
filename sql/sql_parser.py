#!/usr/bin/env python3

import sys
import json
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

from sql_lexer import *

tokens = sql_lexer.tokens

instructions = {}

# Normally, the first rule found in a yacc 
# specification defines the starting grammar 
# rule (top level rule). To change this, simply 
# supply a start specifier in your file. 
start = 'sql'

def p_sql(p):
    '''sql : statement_list '''
    instructions['sql'] = int_pop('statement_list')


def p_sql_empty(p):
    '''sql : empty '''
    instructions['sql'] = ['EMPI']


def p_statement_list_1(p):
    '''statement_list : statement ';' '''
    instructions['statement_list'] = int_pop('statement')


def p_statement_list_2(p):
    '''statement_list : statement_list statement ';' '''
    tmp_instructions = int_pop('statement_list')
    tmp_instructions.append(int_pop('statement')) 
    instructions['statement_list'] = tmp_instructions
    pass

def p_statement(p):
    '''statement : select_stmt '''
    instructions['statement'] = int_pop('select_stmt')


def p_select_stmt(p):
    '''select_stmt : SELECT selection from_clause where_clause '''
    # loading table
    tmp_instructions = int_pop('from_clause')
    # loading selection
    tmp_instructions.extend(int_pop('selection'))
    # loading recode
    tmp_instructions.append('LDTB EMPTY REG_TLB_TMP') 
    tmp_instructions.append('F_CHECK_LOOP:')
    tmp_instructions.append('LTNX REG_TLB "F_EMPTY"') 
    tmp_instructions.extend(int_pop('where_clause'))
    tmp_instructions.append('CHKN R_CMP 0 "F_CHECK_LOOP"') 
    # trunk fileds
    tmp_instructions.append('FLRC REG_RCD') 
    tmp_instructions.append('ADRC REG_RCD REG_TLB_TMP') 
    tmp_instructions.append('JUMP "F_CHECK_LOOP"') 
    tmp_instructions.append('F_EMPTY:') 
    tmp_instructions.append('MVTB REG_TLB_TMP REG_TLB')
    instructions['select_stmt'] = tmp_instructions


def p_selection_1(p):
    '''selection : scalar_exp_list '''
    instructions['selection'] = ['MREG'+' '+'REG_SEL'+' '+'"'+str(p[1])+'"']


def p_scalar_exp_list_1(p):
    '''scalar_exp_list : scalar_exp '''
    p[0] = str(p[1])


def p_scalar_exp_list_2(p):
    '''scalar_exp_list : scalar_exp_list ',' scalar_exp '''
    p[0] = ''.join([p[1], ',', p[3]])


def p_from_clause(p):
    '''from_clause : FROM table_ref '''
    table_name = p[2]
    instructions['from_clause'] = ['LDTB'+' "'+table_name+'" '+'REG_TLB']


def p_where_clause(p):
    '''where_clause : WHERE search_condition '''
    instructions['where_clause'] = int_pop('search_condition');


def p_where_clause_empty(p):
    '''where_clause : empty '''
    instructions['where_clause'] = ['EMPI']


def p_table_ref(p):
    '''table_ref : name_ref '''
    p[0] = p[1]


def p_search_condition(p):
    '''search_condition : predicate
                        | predicate seen_predicate OR predicate
                        | predicate seen_predicate AND predicate empty '''
    if len(p) == 2: 
        instructions['search_condition'] = int_pop('predicate')
    elif len(p) == 5:
        tmp_instructions = int_pop('seen_predicate')
        tmp_instructions.append('CHEK R_CMP 0 "F_FIN"') 
        tmp_instructions.extend(int_pop('predicate')) 
        tmp_instructions.append('F_FIN:') 
        instructions['search_condition'] = tmp_instructions
    elif len(p) == 6:
        tmp_instructions = int_pop('seen_predicate')
        tmp_instructions.append('CHKN R_CMP 0 "F_FIN"') 
        tmp_instructions.extend(int_pop('predicate')) 
        tmp_instructions.append('F_FIN:') 
        instructions['search_condition'] = tmp_instructions


#Embedded Actions seen_${rule}
def p_seen_predicate(p):
    '''seen_predicate : '''
    instructions['seen_predicate'] = int_pop('predicate')


def p_predicate(p):
    '''predicate : '(' predicate ')'
                 | scalar_exp '=' scalar_exp '''
    if len(p) == 4: 
        instructions['predicate'] = ['COMP'+' '+str(p[1])+' '+str(p[3])]


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
    pass


def int_pop(key):
    tmp_instructions = instructions[key]
    del instructions[key]
    return tmp_instructions; 


def interprete(instructions):
    for ins in instructions['sql']:
        print(ins)


if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    yacc.parse(sys.stdin.read(), lxr, debug=True)
    interprete(instructions);
