#!/usr/bin/env python3

"""
Framework for 2048 & 2048-like Games (Python 3)

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

from board import board
from action import action
from solver import state_type
from solver import state_hint
from solver import solver
import sys
import io


if __name__ == '__main__':
    print('2048 Demo: ' + " ".join(sys.argv))
    print()
    
    solve_args = ""
    precision = 10
    for para in sys.argv[1:]:
        if "--solve=" in para:
            solve_args = para[(para.index("=") + 1):]
        elif "--precision=" in para:
            precision = int(para[(para.index("=") + 1):])
    
    solve = solver(solve_args)
    state = board()
    type = state_type()
    hint = state_hint(state)
    for line in sys.stdin:
        type.load(io.StringIO(line[0:line.index(' ')]))
        state.load(io.StringIO(line[(line.index(' ')+1):line.index('+')]))
        hint.load(io.StringIO(line[line.index('+'):]))
        value = solve.solve(state, type)
        print(type, state, hint, "=", value)

