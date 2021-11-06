#!/usr/bin/env python3

"""
Framework for 2048 & 2048-like Games (Python 3)
2048.py: Main file for the 2048 framework

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NYCU, Taiwan
        https://cgilab.nctu.edu.tw/
"""

from board import board
from action import action
from episode import episode
from statistic import statistic
from agent import player
from agent import rndenv
import sys


if __name__ == '__main__':
    print('2048 Demo: ' + " ".join(sys.argv))
    print()

    total, block, limit = 1000, 0, 0
    play_args, evil_args = "", ""
    load, save = "", ""
    summary = False
    for arg in sys.argv[1:]:
        if "--total=" in arg:
            total = int(arg[(arg.index("=") + 1):])
        elif "--block=" in arg:
            block = int(arg[(arg.index("=") + 1):])
        elif "--limit=" in arg:
            limit = int(arg[(arg.index("=") + 1):])
        elif "--play=" in arg:
            play_args = arg[(arg.index("=") + 1):]
        elif "--evil=" in arg:
            evil_args = arg[(arg.index("=") + 1):]
        elif "--load=" in arg:
            load = arg[(arg.index("=") + 1):]
        elif "--save=" in arg:
            save = arg[(arg.index("=") + 1):]
        elif "--summary" in arg:
            summary = True

    stat = statistic(total, block, limit)

    if load:
        input = open(load, "r")
        stat.load(input)
        input.close()
        summary |= stat.is_finished()

    with player(play_args) as play, rndenv(evil_args) as evil:
        while not stat.is_finished():
            play.open_episode("~:" + evil.name())
            evil.open_episode(play.name() + ":~")

            stat.open_episode(play.name() + ":" + evil.name())
            game = stat.back()
            while True:
                who = game.take_turns(play, evil)
                move = who.take_action(game.state())
                if not game.apply_action(move) or who.check_for_win(game.state()):
                    break
            win = game.last_turns(play, evil)
            stat.close_episode(win.name())

            play.close_episode(win.name())
            evil.close_episode(win.name())

    if summary:
        stat.summary()

    if save:
        output = open(save, "w")
        stat.save(output)
        output.close()

