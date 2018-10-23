#!/usr/bin/env python3

"""
Basic framework for developing 2048 programs in Python

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

from board import board


class state_type:
    
    before = 'b'
    after = 'a'
    illegal = 'i'
    
    def __init__(self, type = 'i'):
        self.type = type
        return

    def __str__(self):
        return self.type
    
    def save(self, output):
        output.write(self.__str__())
        return True
    
    def load(self, input):
        self.type = input.read(1)
        return True
    
    def is_before(self):
        return self.type == before
    
    def is_after(self):
        return self.type == after
    
    def is_illegal(self):
        return self.type == illegal


class state_hint:
    
    def __init__(self, state):
        self.state = state
        return

    def __str__(self):
        return "+" + self.type()

    def type(self):
        return str(self.state.info) if self.state.info != 0 else 'x'
    
    def save(self, output):
        output.write(self.__str__())
        return True
    
    def load(self, input):
        hint = input.read()
        hint = hint[1:]
        self.state.info = int(hint) if hint != 'x' else 0
        return True
    

class solver:
    
    def __init__(self, options = ""):
        # TODO: explore the tree and store the result
        return
    
    def solve(self, state, type = state_type.before):
        # to fetch the hint (if type == state_type::after, hint will be 0)
#         hint = state.info
        
        # for a legal state, return its three values.
#         return min, avg, max

        # for an illegal state, simply return -1
        return -1



if __name__ == '__main__':
    print('2048 Demo: solver.py\n')
    
    state = board()
    state[10] = 1
    print(state)
    
    print(action.place.type)
    p = action.place(10, 13)
    print(p.code)
    print(p.position())
    print(p.tile())
    p.apply(state)
    print(state)
    
    print(action.slide.type)
    s = action.slide(1)
    print(s.code)
    s.apply(state)
    print(state)
        
    with open('X:/hello.txt', 'w') as f:
#         pos = f.tell()
#         print(f.read(2))
#         f.seek(pos)
#         print(f.read(2))
        s.save(f)
        p.save(f)
        
    