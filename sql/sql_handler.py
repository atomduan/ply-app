#!/usr/local/bin/python3

import sys
import json
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

def interpret(symbols):
    sql = symbols['sql']
    int_sql(symbols['sql'])
    pass

def int_sql(sql):
    statement_list = sql['statement_list']
    for statement in statement_list:
        int_statement(statement)
        pass

def int_statement(statement):
    select_stmt = statement['select_stmt']
    int_select_stmt(select_stmt)
    pass

def int_select_stmt(select_stmt):
    #1. gen load table
    from_clause = select_stmt['from_clause']
    table_ref = from_clause['table_ref']
    table_name = table_ref['name_ref']['token']
    print('load_table %s' % (table_name))

    #2. condition filter
    where_clause = select_stmt['where_clause']
    search_condition = where_clause['search_condition']
    s_type = search_condition['type']
    if s_type == '':
        pred = search_condition['predicate']
        pass
    if s_type == 'OR':
        prel = search_condition['predicate-l']
        prer = search_condition['predicate-r']
        int_predicate(prel)
        print "compute_stack_push"
        int_predicate(prer)
        print "compute_stack_or"
        print "compute_stack_or"
        pass 
    if s_type == 'AND':
        prel = search_condition['predicate-l']
        prer = search_condition['predicate-r']
        int_predicate(prel)
        int_predicate(prer)
        print "select_compute_stack_and"
        pass

    #3. selecter field 
    selection = select_stmt['selection']
    pass
