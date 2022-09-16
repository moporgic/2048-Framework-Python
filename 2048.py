#!/usr/bin/env python3

"""
Framework for 2048 & 2048-Like Games (Python 3)
2048.py: Main file for the 2048 framework

Author: Hung Guei
        Computer Games and Intelligence (CGI) Lab, NYCU, Taiwan
        https://cgilab.nctu.edu.tw/
"""

from board import board
from action import action
from episode import episode
from statistics import statistics
from agent import random_slider
from agent import random_placer
import sys


if __name__ == '__main__':
    print('2048 Demo: ' + " ".join(sys.argv))
    print()

    total, block, limit = 1000, 0, 0
    slide_args, place_args = "", ""
    load_path, save_path = "", ""
    args = sys.argv[1:]
    while args:
        arg = args.pop(0).lstrip("-")
        match_arg = lambda flag: arg.find(flag) == 0
        next_opt = lambda: arg[(arg.find("=") + 1):] if (arg.find("=") + 1) else args.pop(0)
        if match_arg("total"):
            total = int(next_opt())
        elif match_arg("block"):
            block = int(next_opt())
        elif match_arg("limit"):
            limit = int(next_opt())
        elif match_arg("slide") or match_arg("play"):
            slide_args = next_opt()
        elif match_arg("place") or match_arg("env"):
            place_args = next_opt()
        elif match_arg("load"):
            load_path = next_opt()
        elif match_arg("save"):
            save_path = next_opt()

    stats = statistics(total, block, limit)

    if load_path:
        input = open(load_path, "r")
        stats.load(input)
        input.close()
        if stats.is_finished():
            stats.summary()

    with random_slider(slide_args) as slide, random_placer(place_args) as place:
        while not stats.is_finished():
            # print("======== Game %d ========" % stats.step(), file=sys.stderr)
            slide.open_episode("~:" + place.name())
            place.open_episode(slide.name() + ":~")

            stats.open_episode(slide.name() + ":" + place.name())
            game = stats.back()
            while True:
                who = game.take_turns(slide, place)
                move = who.take_action(game.state())
                # print("%s\n#%d %s: %s" % (game.state(), game.step(), who.name(), move), file=sys.stderr)
                if not game.apply_action(move) or who.check_for_win(game.state()):
                    break
            win = game.last_turns(slide, place)
            stats.close_episode(win.name())

            slide.close_episode(win.name())
            place.close_episode(win.name())

    if save_path:
        output = open(save_path, "w")
        stats.save(output)
        output.close()

