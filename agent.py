#!/usr/bin/env python3

"""
Framework for 2048 & 2048-like Games (Python 3)
agent.py: Define the behavior of variants of agents including players and environments

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NYCU, Taiwan
        https://cgilab.nctu.edu.tw/
"""

from board import board
from action import action
from weight import weight
from array import array
import random
import sys



class agent:
    """ base agent """

    def __init__(self, options = ""):
        self.info = {}
        options = "name=unknown role=unknown " + options
        for option in options.split():
            data = option.split("=", 1) + [True]
            self.info[data[0]] = data[1]
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def open_episode(self, flag = ""):
        return

    def close_episode(self, flag = ""):
        return

    def take_action(self, state):
        return action()

    def check_for_win(self, state):
        return False

    def property(self, key):
        return self.info[key] if key in self.info else None

    def notify(self, message):
        data = message.split("=", 1) + [True]
        self.info[data[0]] = data[1]
        return

    def name(self):
        return self.property("name")

    def role(self):
        return self.property("role")


class random_agent(agent):
    """ base agent for agents with random behavior """

    def __init__(self, options = ""):
        super().__init__(options)
        seed = self.property("seed")
        if seed is not None:
            random.seed(int(seed))
        return

    def choice(self, seq):
        target = random.choice(seq)
        return target

    def shuffle(self, seq):
        random.shuffle(seq)
        return


class weight_agent(agent):
    """ base agent for agents with weight tables and a learning rate """

    def __init__(self, options = ""):
        super().__init__(options)
        self.net = []
        init = self.property("init")
        if init is not None:
            self.init_weights(init)
        load = self.property("load")
        if load is not None:
            self.load_weights(load)
        self.alpha = 0
        alpha = self.property("alpha")
        if alpha is not None:
            self.alpha = float(alpha)
        return

    def __exit__(self, exc_type, exc_value, traceback):
        save = self.property("save")
        if save is not None:
            self.save_weights(save)
        return

    def init_weights(self, info):
        for i in info.split(','): # comma-separated sizes, e.g., "65536,65536"
            self.net += [weight(int(i))]
        return

    def load_weights(self, path):
        input = open(path, 'rb')
        size = array('L')
        size.fromfile(input, 1)
        size = size[0]
        for i in range(size):
            self.net += [weight()]
            self.net[-1].load(input)
        return

    def save_weights(self, path):
        output = open(path, 'wb')
        array('L', [len(self.net)]).tofile(output)
        for w in self.net:
            w.save(output)
        return


class rndenv(random_agent):
    """
    random environment
    add a new random tile to an empty cell
    2-tile: 90%
    4-tile: 10%
    """

    def __init__(self, options = ""):
        super().__init__("name=random role=environment " + options)
        return

    def take_action(self, state):
        empty = [pos for pos, tile in enumerate(state.state) if not tile]
        if empty:
            pos = self.choice(empty)
            tile = self.choice([1] * 9 + [2])
            return action.place(pos, tile)
        else:
            return action()


class player(random_agent):
    """
    dummy player
    select a legal action randomly
    """

    def __init__(self, options = ""):
        super().__init__("name=dummy role=player " + options)
        return

    def take_action(self, state):
        legal = [op for op in range(4) if board(state).slide(op) != -1]
        if legal:
            op = self.choice(legal)
            return action.slide(op)
        else:
            return action()


if __name__ == '__main__':
    print('2048 Demo: agent.py\n')
    pass
