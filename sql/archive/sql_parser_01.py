#!/usr/local/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

from sql_lexer import *
tokens = sql_lexer.tokens

symbols={"LALALAL":[123,1234]}

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

def p_sql(t):
    ''' sql : statement_list '''
    symbols[123] = "ADD TOP ONE"
    pass

def p_sql_empty(t):
    ''' sql : '''
    pass

def p_statement_list_1(t):
    ''' statement_list : statement COMMA '''
    pass

def p_statement_list_2(t):
    ''' statement_list : statement_list statement '''
    pass

def p_statement(t):
    ''' statement : select_stmt '''
    pass

def p_select_stmt(t):
    ''' select_stmt : SELECT selection from_clause where_clause '''
    print(str(t))
    pass

def p_selection_1(t):
    ''' selection : scalar_exp_list '''
    pass

def p_selection_2(t):
    ''' selection : '*' '''
    pass

def p_scalar_exp_list_1(t):
    ''' scalar_exp_list : scalar_exp '''
    pass

def p_scalar_exp_list_2(t):
    ''' scalar_exp_list : scalar_exp_list ',' scalar_exp '''
    pass

def p_from_clause(t):
    ''' from_clause : FROM table_ref_list '''
    pass

def p_where_clause(t):
    ''' where_clause : WHERE search_condition '''
    pass

def p_where_clause_empty(t):
    ''' where_clause : '''
    pass

def p_table_ref_list_1(t):
    ''' table_ref_list : table_ref '''
    pass

def p_table_ref_list_2(t):
    ''' table_ref_list : table_ref_list ',' table_ref '''
    pass

def p_table_ref(t):
    ''' table_ref : name_ref '''
    pass

def p_search_condition_1(t):
    ''' search_condition : search_condition OR search_condition '''
    pass 

def p_search_condition_2(t):
    ''' search_condition : search_condition AND search_condition '''
    pass 

def p_search_condition_3(t):
    ''' search_condition : '(' search_condition ')' '''
    pass

def p_search_condition_4(t):
    ''' search_condition : predicate '''
    pass

def p_predicate_1(t):
    ''' predicate : comparison_predicate '''
    pass

def p_predicate_2(t):
    ''' predicate : like_predicate '''
    pass

def p_comparison_predicate(t):
    ''' comparison_predicate : scalar_exp COMPARISON scalar_exp '''
    pass

def p_like_predicate_1(t):
    ''' like_predicate : scalar_exp NOT LIKE like_literal '''
    pass

def p_like_predicate_2(t):
    ''' like_predicate : scalar_exp LIKE like_literal '''
    pass

def p_scalar_exp_1(t):
    ''' scalar_exp : scalar_exp '+' scalar_exp '''
    pass

def p_scalar_exp_2(t):
    ''' scalar_exp : scalar_exp '-' scalar_exp '''
    pass

def p_scalar_exp_3(t):
    ''' scalar_exp : scalar_exp '*' scalar_exp '''
    pass
def p_scalar_exp_4(t):
    ''' scalar_exp : scalar_exp '/' scalar_exp '''
    pass

def p_scalar_exp_5(t):
    ''' scalar_exp : '+' scalar_exp %prec UMINUS '''
    pass

def p_scalar_exp_6(t):
    ''' scalar_exp : '-' scalar_exp %prec UMINUS '''
    pass

def p_scalar_exp_7(t):
    ''' scalar_exp : '(' scalar_exp ')' '''
    pass

def p_scalar_exp_8(t):
    ''' scalar_exp : scalar_unit '''
    pass

def p_scalar_unit_1(t):
    ''' scalar_unit : INTNUM '''
    pass

def p_scalar_unit_2(t):
    ''' scalar_unit : name_ref '''
    pass

def p_name_ref_1(t):
    ''' name_ref : STRING '''
    pass 

def p_name_ref_2(t):
    ''' name_ref : name_ref '.' STRING '''
    pass

def p_like_literal_1(t):
    ''' like_literal : STRING '''
    pass

def p_like_literal_2(t):
    ''' like_literal : INTNUM '''
    pass

def p_error(t):
    print("Whoa. We're hosed")

if __name__ == '__main__':
    lxr = lex.lex()
    yacc.yacc(debug=True)
    yacc.parse(sys.stdin.read(),lxr,debug=False)
    print(symbols)
