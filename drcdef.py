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
    'forall' : 'FORALL',
    'exit' : 'EXIT',}

tokens = [
    'LBRACE', 'RBRACE', 'BAR',
    'LPAREN', 'RPAREN',
    'COMMA', 
    'COMPARISON',
    'NAME', 'NUMBER', 'STRING'] + list(reserved.values())

literals = ['=','<','>','{','}', '(',')','|',',']

#Tokens


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_RESERVED(t):
    r'and | or | exists | forall | not | exit'
    t.type = reserved.get(t.value, 'BOMB')
    return t

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BAR = r'\|'
t_COMMA = r','
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

start='query'

def p_query(p):
    'query :  LBRACE varlist BAR formula RBRACE'
    print "1"

def p_varlist_name(p):
    'varlist : NAME'
    print "2"

def p_varlist_expr(p):
    'varlist : varlist COMMA NAME'
    print "3"

def p_formula_base(p):
    'formula : atomicformula'
    print "4"

def p_formula_comp(p):
    '''formula : formula AND formula
               | formula OR formula'''
    
    print "5"

def p_formula_nega(p):
    'formula : NOT LPAREN formula RPAREN'
    print "7"

def p_formula_existsforall(p):
    '''formula : LPAREN EXISTS varlist RPAREN LPAREN formula RPAREN
             | LPAREN FORALL varlist RPAREN LPAREN formula RPAREN'''
    print "8"

def p_atomicformula_name(p):
    'atomicformula : NAME LPAREN arglist RPAREN'
    print "9"

def p_atomicformula_comparison(p):
    'atomicformula : arg COMPARISON arg'
    print "10"

def p_arglist_group(p):
    '''arglist : arg 
               | arglist COMMA arg'''
    print "11"

def p_arg_item(p):
    '''arg : NAME 
           | STRING 
           | NUMBER'''
    print "12"

def p_query_exit(p):
    'query : EXIT'
    print 'goodbye'
    exit()

    
def p_error(p):
    print "Syntax error"

import ply.yacc as yacc

yacc.yacc()

while True:
    try:
        s = raw_input('DRC> ')
    except EOFError:
        break
    yacc.parse(s)


