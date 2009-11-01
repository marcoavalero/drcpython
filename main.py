import sys
import drcdef
import warnings
import ply.yacc as yacc
from drcdef import *
from drcerr import *


yacc.yacc(module=drcdef)

def main():
    while True:
        try:
            s = raw_input('DRC> ')
        except EOFError:
            break
        if s == "exit":
            break
        try:
            yacc.parse(s)
        except DrcError:
            continue


main()
