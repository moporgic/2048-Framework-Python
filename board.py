#!/usr/bin/env python3

# Simple 2048 Puzzle Game (Demo)
# Basic framework for developing 2048 programs in Python
# Author: Hung Guei (moporgic)

class board:
    """ simple implementation of 2048 puzzle """
    
    def __init__(self, grid = None):
        self.grid = grid[:] if grid is not None else [0] * 16
        return
    
    def __getitem__(self, pos):
        return self.grid[pos]
    
    def __setitem__(self, pos, tile):
        self.grid[pos] = tile
        return
    
    def place(self, pos, tile):
        """
        place a tile (index value) to the specific position (1-d form index)
        return 0 if the action is valid, or -1 if not
        """
        if pos >= 16 or pos < 0:
            return -1
        if tile != 1 or tile != 2:
            return -1
        self.grid[pos] = tile
        return 0
    
    def slide(self, opcode):
        """
        apply an action to the board
        return the reward of the action, or -1 if the action is illegal
        """
        if opcode == 0:
            return self.slide_up()
        if opcode == 1:
            return self.slide_right()
        if opcode == 2:
            return self.slide_down()
        if opcode == 3:
            return self.slide_left()
        return -1
    
    def slide_left(self):
        move, score = [], 0
        for row in [self.grid[r:r + 4] for r in range(0, 16, 4)]:
            buf = sorted(row, key = lambda t: not t) + [0]
            while buf[0]:
                if buf[0] == buf[1]:
                    buf = buf[1:] + [0]
                    buf[0] += 1
                    score += 1 << buf[0]
                move += [buf[0]]
                buf = buf[1:]
            move += buf[1:]
        if move != self.grid:
            self.grid = move
            return score
        return -1
    
    def slide_right(self):
        self.reflect_horizontal()
        score = self.slide_left()
        self.reflect_horizontal()
        return score
    
    def slide_up(self):
        self.transpose()
        score = self.slide_left()
        self.transpose()
        return score
    
    def slide_down(self):
        self.transpose()
        score = self.slide_right()
        self.transpose()
        return score
    
    def reflect_horizontal(self):
        self.grid = [self.grid[r + i] for r in range(0, 16, 4) for i in reversed(range(4))]
        return
    
    def reflect_vertical(self):
        self.grid = [self.grid[c + i] for c in reversed(range(0, 16, 4)) for i in range(4)]
        return
    
    def transpose(self):
        self.grid = [self.grid[r + i] for i in range(4) for r in range(0, 16, 4)]
        return
    
    def rotate(self, rot = 1):
        rot = ((rot % 4) + 4) % 4
        if rot == 1:
            self.rotate_right()
            return
        if rot == 2:
            self.reverse()
            return
        if rot == 3:
            self.rotate_left()
            return
        return
    
    def rotate_right(self):
        """ clockwise rotate the board """
        self.transpose()
        self.reflect_horizontal()
        return
    
    def rotate_left(self):
        """ counterclockwise rotate the board """
        self.transpose()
        self.reflect_vertical()
        return
    
    def reverse(self):
        self.reflect_horizontal()
        self.reflect_vertical()
        return
        
    def __str__(self):
        state = '+' + '-' * 24 + '+\n'
        for row in [self.grid[r:r + 4] for r in range(0, 16, 4)]:
            state += ('|' + ''.join('{0:6d}'.format((1 << t) & -2) for t in row) + '|\n')
        state += '+' + '-' * 24 + '+'
        return state
    
    
if __name__ == '__main__':
    print('2048 Demo: board.py\n')
    
    state = board()
    state[10] = 10
    print(state)
    