# CSC 6340 
# Fall 2009
# Marco Valero, John Daigle
# drcdef.py
# phase 1 grammar for DRC queries

    
# Build the lexer
import drctokens
import ply.lex as lex
from drctokens import tokens
lex.lex(module=drctokens)
# Dictionary and DRCNode counter

vars = {}
args = {}

# Parsing rules

start='query'

def p_query(p):
    'query :  LBRACE qpair RBRACE'
    print p[2]

def p_qpair(p):
    'qpair : varlist BAR formula'
    p[0] = p[1]

def p_varlist_name(p):
    'varlist : NAME'
    print "2"

def p_varlist_expr(p):
    'varlist : varlist COMMA NAME'
    print "3"

def p_formula_base(p):
    'formula : atomicformula'
    print "4"

def p_formula_and(p):
    'formula : formula AND formula'
    print "5"
    p[0]  = p[1] and p[2]

def p_formula_or(p):
    'formula : formula OR formula'
    print "6"
    p[0]  = p[1] or p[2]    

def p_formula_nega(p):
    'formula : NOT LPAREN formula RPAREN'
    print "7"
    p[0]  = not p[3]

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
    if s == "exit":
        break
    yacc.parse(s)
    

