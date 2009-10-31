import sys
import drcdef
import ply.yacc as yacc
from drcdef import *
yacc.yacc(module=drcdef)

def main():
    while True:
        try:
            s = raw_input('DRC> ')
        except EOFError:
            break
        if s == "exit":
            break
        yacc.parse(s)

main()
