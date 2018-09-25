# Simple 2048 Puzzle Game (Demo)
# Basic framework for developing 2048 programs in Python
# Author: Hung Guei (moporgic)

from board import board

class action:
    """ action code for TDL2048 """
    
    def __init__(self, code = -1):
        self.code = code
        return
    
    def apply(self, board):
        return -1
    
    def save(self, output):
        output.write(self.__str__())
        return True
    
    def load(self, input):
        input.read(2)
        return
    
    def __str__(self):
        return "??"
    
    def event(self):
        return self.code & 0x00ffffff
    
    def type(self):
        return self.code & 0xff000000
    
    
class slide(action):
    """ create a sliding action with board opcode """
    type = 0x73000000 # ASCII code 's' << 24
    
    def __init__(self, code = -1):
        super().__init__(slide.type | code)
        return
    
    
class place(action):
    """ create a placing action with position and tile """
    type = 0x70000000 # ASCII code 'p' << 24
    
    def __init__(self, code = -1):
        super().__init__(place.type | code)
        return
    
    def __init__(self, pos, tile):
        super().__init__(place.type | (pos & 0x0f) | (tile << 4))
        return
    
    def position(self):
        return self.event() & 0x0f
    
    def tile(self):
        return self.event() >> 4
    
    
if __name__ == '__main__':
    print('2048 Demo: action.py\n')
    
    state = board()
    state[10] = 1
    print(state)
    
    with open('X:/hello.txt', 'r') as f:
        pos = f.tell()
        print(f.read(2))
        f.seek(pos)
        print(f.read(2))
        
    print(slide.type)
    s = slide(10)
    print(s.code)
    
    print(place.type)
    p = place(10, 13)
    print(p.code)
    print(p.position())
    print(p.tile())