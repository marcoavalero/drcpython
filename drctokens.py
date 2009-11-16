# CSC 6340
# Fall 2009
# Term Project
# Marco Valero, J. Paul Daigle

# module drctokens.py
# this file only contains the token rules for the Calculus

# token names

reserved = {
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'exists' : 'EXISTS',
    'forall' : 'FORALL',
    'exit' : 'EXIT',
    'use' : 'USE',
    'help' : 'HELP',
    'debug' : 'DEBUG',
    'nodebug' : 'NODEBUG',
    'database' : 'DATABASE',
    '<=' : 'LESSEQ',
    '>=' : 'GREAEQ',
    '<>' : 'DIFFERENT',
    '<' : 'LESS',
    '>' : 'GREAT',
    '=' : 'EQUAL',}

tokens = [
    'LBRACE', 'RBRACE', 'BAR',
    'LPAREN', 'RPAREN',
    'COMMA', 
    'NAME', 'NUMBER', 'STRING'] + list(reserved.values())


#Tokens


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]* |  <= | >= | <> | < | > | ='
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

#def t_RESERVED(t):
#    r'and | or | exists | forall | not | exit | use  | database | <= | >= | <> | < | > | ='
#    t.type = reserved.get(t.value, 'BOMB')
#    return t

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BAR    = r'\|'
t_COMMA  = r','
t_STRING = r"\'[^']*\'"
t_ignore = " \t"



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
