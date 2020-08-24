#!/usr/bin/env python3

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
    records = []
    load_table(table_name, records)

    #2. condition filter
    filter_records = []
    for r in records:
        where_clause = select_stmt['where_clause']
        search_condition = where_clause['search_condition']
        s_type = search_condition['type']
        if s_type == '':
            pred = search_condition['predicate']
            if int_predicate(pred, r):
                filter_records.append(r)
        if s_type == 'OR':
            prel = search_condition['predicate-l']
            prer = search_condition['predicate-r']
            if int_predicate(prel, r):
                filter_records.append(r)
                continue
            if int_predicate(prer, r):
                filter_records.append(r)
                continue
        if s_type == 'AND':
            prel = search_condition['predicate-l']
            prer = search_condition['predicate-r']
            if int_predicate(prel, r):
                if int_predicate(prer, r):
                    filter_records.append(r)

    #3. selecter field 
    fields = []
    selection = select_stmt['selection']
    scalar_exp_list = selection['scalar_exp_list']
    for scalar_exp in scalar_exp_list:
        scalar_unit = scalar_exp['scalar_unit']
        s_type = scalar_unit['type']
        if s_type != 'name_ref':
            token = scalar_unit['token']
        else:
            name_ref = scalar_unit['name_ref']
            token = name_ref['token']
        fields.append(token)
    
    result = []
    for record in filter_records:
        trunk_record = []
        for f in record:
            if f in fields:
                trunk_record.append(f)
        result.append(t_record) 

    #4. output result
    print(result)

def int_predicate(pred, r):
    #TODO duanjuntao
    return False

def load_table(table_name, records):
    #TODO duanjuntao
    pass
