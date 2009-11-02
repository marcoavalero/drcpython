import sys
import drcdef
import warnings
import ply.yacc as yacc
from drcdef import *
from drcerr import *
from drcobj import *

yacc.yacc(module=drcdef)

def main():
    while True:
        try:
            s = raw_input('DRC> ')
        except EOFError:
            break
        try:
            t = yacc.parse(s)
        except DrcError:
            continue
        t.print_node()
        
main()
