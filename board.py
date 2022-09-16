#!/usr/bin/env python3

"""
Framework for 2048 & 2048-Like Games (Python 3)
board.py: Define the game state and basic operations of the game of 2048

Author: Hung Guei
        Computer Games and Intelligence (CGI) Lab, NYCU, Taiwan
        https://cgilab.nctu.edu.tw/
"""

class board:
    """ simple implementation of 2048 puzzle """

    def __init__(self, state = None, info = None):
        self.state = state[:] if state is not None else [0] * 16
        self.info = info
        return

    def __getitem__(self, pos):
        return self.state[pos]

    def __setitem__(self, pos, tile):
        self.state[pos] = tile
        return

    def place(self, pos, tile):
        """
        place a tile (index value) to the specific position (1-d index)
        return 0 if the action is valid, or -1 if not
        """
        if pos >= 16 or pos < 0 or self.state[pos] != 0:
            return -1
        if tile != 1 and tile != 2:
            return -1
        self.state[pos] = tile
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
        for row in [self.state[r:r+4] for r in range(0, 16, 4)]:
            row, buf = [], [t for t in row if t]
            while buf:
                if len(buf) >= 2 and buf[0] is buf[1]:
                    buf = buf[1:]
                    buf[0] += 1
                    score += 1 << buf[0]
                row += [buf[0]]
                buf = buf[1:]
            move += row + [0] * (4 - len(row))
        if move != self.state:
            self.state = move
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

    def rotate(self, rot = 1):
        """ rotate the board clockwise by given times """
        rot = ((rot % 4) + 4) % 4
        if rot == 1:
            self.rotate_clockwise()
            return
        if rot == 2:
            self.reverse()
            return
        if rot == 3:
            self.rotate_counterclockwise()
            return
        return

    def rotate_clockwise(self):
        self.transpose()
        self.reflect_horizontal()
        return

    def rotate_counterclockwise(self):
        self.transpose()
        self.reflect_vertical()
        return

    def reverse(self):
        self.reflect_horizontal()
        self.reflect_vertical()
        return

    def reflect_horizontal(self):
        self.state = [self.state[r + i] for r in range(0, 16, 4) for i in reversed(range(4))]
        return

    def reflect_vertical(self):
        self.state = [self.state[c + i] for c in reversed(range(0, 16, 4)) for i in range(4)]
        return

    def transpose(self):
        self.state = [self.state[r + i] for i in range(4) for r in range(0, 16, 4)]
        return

    def __str__(self):
        state = '+' + '-' * 24 + '+\n'
        for row in [self.state[r:r + 4] for r in range(0, 16, 4)]:
            state += ('|' + ''.join('{0:6d}'.format((1 << t) & -2) for t in row) + '|\n')
        state += '+' + '-' * 24 + '+'
        return state


if __name__ == '__main__':
    print('2048 Demo: board.py\n')
    pass
