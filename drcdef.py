# CSC 6340 
# Fall 2009

# drcdef.py
# phase 1 grammar for DRC queries

# token names

reserved = {
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'exists' : 'EXISTS',
    'forall' : 'FORALL',}

tokens = [
    'LBRACE', 'RBRACE', 'BAR',
    'LPAREN', 'RPAREN',
    'COMMA',
    'COMPARISON',
    'NAME', 'NUMBER', 'STRING'] + list(reserved.values())

#Tokens

start='query'

def p_query(p):
    'query :  LBRACE varlist BAR formula RBRACE'

def p_varlist_name:
    'varlist : NAME'

def p_varlist_expr:
    'varlist : varlist COMMA NAME'

def p_formula_base:
    'formula : atomicformula'

def p_formula_comp:
    '''formula : formula AND formula
               | formula OR formula'''

def p_formula_nega:
    'NOT LPAREN formlua RPAREN'

def p_formula_
