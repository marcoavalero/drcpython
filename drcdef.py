# CSC 6340 
# CSC 6340 
# Fall 2009
# Marco Valero, John Daigle
# drcdef.py
# phase 1 grammar for DRC queries

#module for the yacc file
    
# Build the lexer
import random
import drctokens
import ply.lex as lex
from drctokens import tokens
lex.lex(module=drctokens)

# Dictionary and DRCNode counter
import drcobj
from drcobj import DRC
import drcarg
from drcarg import *
import drcdbe
from drcdbe import *

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
    p[0].prune_tree()
    p[0].numbernodes(1)


def p_varlist_name(p):
    'varlist : NAME'
    p[0]  = DRC("TempArgNode")
    p[0].set_varlist(DRC_Var(idid=p[1]))
#    print "2"

def p_varlist_expr(p):
    'varlist : varlist COMMA NAME'
    p[0] = p[1]
    p[0].set_varlist(DRC_Var(idid=p[3]))
#    del p[1]
#    print "3"

def p_formula_paren(p):
    'formula : LPAREN formula RPAREN'
    p[0] = p[2]

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

def p_formula_exists(p):
    'formula : LPAREN EXISTS varlist RPAREN LPAREN formula RPAREN'
#    print "8"
    p[0] = p[3]
    p[0].set_type(p[2])    
    p[0].set_children(p[6])

def p_formula_forall(p):
    'formula : LPAREN FORALL varlist RPAREN LPAREN formula RPAREN'
#    print "8"
    notnode = DRC("not")
    notnode.set_children(p[6])
    existsnode = p[3]
    existsnode.set_type("exists")    
    existsnode.set_children(notnode)
    p[0]  = DRC("not")
    p[0].set_children(existsnode)


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
    #argg = DRC_Var(idid=p[1]) #NOT THE DEBUG LINE
    #argg = DRC_Var(idid=p[1], type = random.choice(["STRING", "NUMBER"])) #DEBUG LINE
    argg = DRC_Var(idid=p[1]) #NOT THE DEBUG LINE
    p[0].set_arglist(argg)
    #    print "12"

def p_arg_item_number(p):
    'arg : NUMBER'
    p[0]  = DRC("TempArgNode")
    argg = Int_Con(data=p[1])
    p[0].set_arglist(argg)

def p_arg_item_string(p):
    'arg : STRING' 
    p[0]  = DRC("TempArgNode")
    argg = Str_Con(data=p[1])
    p[0].set_arglist(argg)

def p_query_exit(p):
    'query : EXIT'
    print 'goodbye'
    exit()

def p_query_database(p):
    'query : DATABASE'
    p[0]  = DRC("DBNode")

def p_query_usedb(p):
    'query : USE STRING'
    p[0]  = DRC("USEDB")
    filename = p[2]
    filename = filename.strip('\'')
    p[0].predicateName = filename
    print "Database changed to ", filename

def p_query_help(p):
    'query : HELP'
    p[0]  = DRC("HELP")
    p[0].predicateName = p[1]
    print "DRC Parser version 1.0 (by Marco Valero & John Daigle)\n\nCommand\t\t\tDescription\n-------\t\t\t----------\nuse 'database_name'\tChanges the database\ndatabase\t\tShows the database tables\ndebug\t\t\tEnables debug mode\nnodebug\t\t\tDisables debug mode\n"

def p_query_debug(p):
    'query : DEBUG'
    p[0]  = DRC("DEBUG")
    p[0].predicateName = p[1]
    print "Debug mode enabled\n"

def p_query_nodebug(p):
    'query : NODEBUG'
    p[0]  = DRC("NODEBUG")
    p[0].predicateName = p[1]
    print "Debug mode disabled\n"
    
def p_error(p):
    raise DrcError("Syntax error" + str(p))


    

