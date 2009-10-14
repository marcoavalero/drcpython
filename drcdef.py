# CSC 6340 
# CSC 6340 
# Fall 2009
# Marco Valero, John Daigle
# drcdef.py
# phase 1 grammar for DRC queries

#module for the yacc file
    
# Build the lexer
import drctokens
import ply.lex as lex
from drctokens import tokens
lex.lex(module=drctokens)

# Dictionary and DRCNode counter
import drcobj
from drcobj import DRC
import drcarg
from drcarg import Arg
#vars = {}
#args = {}
# dictionary = []


# Parsing rules

start='query'

def p_query(p):
    'query :  LBRACE varlist BAR formula RBRACE'
#    print "1"
    p[0] = p[2]
    p[0].set_type("Query")
    p[0].set_children(p[4])
    p[0].reducetree() 
    p[0].print_node() 

def p_varlist_name(p):
    'varlist : NAME'
    p[0]  = DRC("TempArgNode")
    p[0].set_varlist(p[1])
#    print "2"

def p_varlist_expr(p):
    'varlist : varlist COMMA NAME'
    p[0] = p[1]
    p[0].set_varlist(p[3])
#    del p[1]
#    print "3"

def p_formula_base(p):
    'formula : atomicformula'
    p[0] = p[1]
#    print "4"

def p_formula_and(p):
    'formula : formula AND formula'
#    print "5"
    p[0]  = DRC(p[2]) 
    p[0].set_children(p[1])
    p[0].set_children(p[3])  

def p_formula_or(p):
    'formula : formula OR formula'
#    print "6"
    p[0]  = DRC(p[2])  
    p[0].set_children(p[1])
    p[0].set_children(p[3])  

def p_formula_nega(p):
    'formula : NOT LPAREN formula RPAREN'
#    print "7"
    p[0]  = DRC(p[1])
    p[0].set_children(p[3])

def p_formula_existsforall(p):
    '''formula : LPAREN EXISTS varlist RPAREN LPAREN formula RPAREN
             | LPAREN FORALL varlist RPAREN LPAREN formula RPAREN'''
#    print "8"
    p[0] = p[3]
    p[0].set_type(p[2])    
    p[0].set_children(p[6])

def p_atomicformula_name(p):
    'atomicformula : NAME LPAREN arglist RPAREN'
#    print "9"
    p[0] = p[3]
    p[0].set_predicate(p[1])
    p[0].set_type("Predicate")

def p_atomicformula_comparison(p):
    '''atomicformula : arg LESSEQ arg
                     | arg GREAEQ arg
                     | arg DIFFERENT arg
                     | arg LESS arg
                     | arg GREAT arg
                     | arg EQUAL arg'''
#    print "10"
    p[0] = DRC("Comparison")
    p[0].set_leftop(p[1].argList)
    p[0].set_operator(p[2])
    p[0].set_rightop(p[3].argList)

def p_arglist_single(p):
    'arglist : arg'
    p[0] = p[1]
#    print "11a"
    
def p_arglist_group(p):
    'arglist : arglist COMMA arg'''
    p[0]  = p[1]
    p[0].set_arglist(p[3].argList[0])
#    del p[1]
#    print "11b"

def p_arg_item_name(p):
    'arg : NAME' 
    p[0]  = DRC("TempArgNode")
    argg = Arg(type="Name", value=p[1])
    p[0].set_arglist(argg)
#    print "12"

def p_arg_item_number(p):
    'arg : NUMBER'
    p[0]  = DRC("TempArgNode")
    argg = Arg(type="NUMBER", value=p[1])
    p[0].set_arglist(argg)

def p_arg_item_string(p):
    'arg : STRING' 
    p[0]  = DRC("TempArgNode")
    argg = Arg(type="STRING", value=p[1])
    p[0].set_arglist(argg)

def p_query_exit(p):
    'query : EXIT'
    print 'goodbye'
    exit()

    
def p_error(p):
    print "Syntax error"


    

