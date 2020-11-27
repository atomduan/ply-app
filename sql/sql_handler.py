#!/usr/bin/env python3

import os
import sys
import json
import ply.lex as lex
import ply.yacc as yacc
import sql_lexer

def interpret(symbols):
    sql = symbols['sql']
    int_sql(symbols['sql'])


def int_sql(sql):
    statement_list = sql['statement_list']
    for statement in statement_list:
        int_statement(statement)


def int_statement(statement):
    select_stmt = statement['select_stmt']
    int_select_stmt(select_stmt)


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
    is_aster = False
    fields = []
    selection = select_stmt['selection']
    scalar_exp_list = selection['scalar_exp_list']
    for scalar_exp in scalar_exp_list:
        scalar_unit = scalar_exp['scalar_unit']
        s_type = scalar_unit['type']
        if s_type != 'name_ref':
            token = scalar_unit['token']
            if s_type == 'ASTER':
                is_aster = True
        else:
            name_ref = scalar_unit['name_ref']
            token = name_ref['token']
        fields.append(token)
    result = []
    for record in filter_records:
        if is_aster == False:
            fr = {}
            for key in record:
                if key in fields:
                    fr[key] = record[key]
            result.append(fr)
        else:
            result.append(record)

    #4. output result
    print(result)


def int_predicate(pred, r):
    comparison_predicate = pred['comparison_predicate']
    c_type = comparison_predicate['type']
    if c_type == 'EQ':
        scalar_exp_l = comparison_predicate['scalar_exp_l'],
        scalar_exp_r = comparison_predicate['scalar_exp_r'],
        lval = eval_scalar(scalar_exp_l, r)
        rval = eval_scalar(scalar_exp_r, r)
        return lval == rval
    return True


def eval_scalar(scalar_exp, record):
    #TODO bug here why [0] ?
    scalar_unit = scalar_exp[0]['scalar_unit']
    s_type = scalar_unit['type']
    if s_type == 'NUM':
        s_token = scalar_unit['token']
        return str(s_token)
    if s_type == 'STR':
        s_token = scalar_unit['token']
        return str(s_token)
    if s_type == 'name_ref':
        name_ref = scalar_unit['name_ref']
        idstr = name_ref['token']
        return eval_record_val(idstr, record)
    return "ERR"


def eval_record_val(idstr, recode):
    return recode[idstr]


def load_table(table_name, records):
    count = 0
    meta = []
    db_path = os.getcwd() + "/resource/" + table_name + ".tbl"
    with open(db_path) as f:
        for line in iter(f):
            if count == 0:
                meta = line.strip().split(" ")
            else:
                r = {}
                data = line.strip().split(" ")
                for i in range(len(meta)):
                    r[meta[i]] = data[i]
                records.append(r)
            count = count + 1
