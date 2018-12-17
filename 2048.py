#!/usr/bin/env python3

"""
Framework for 2048 & 2048-like Games (Python 3)

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

from board import board
from action import action
from episode import episode
from statistic import statistic
from agent import player
from agent import rndenv
from arena import arena
import sys
import re
import io


def shell():
    host = arena("anonymous")
    
    for para in sys.argv[1:]:
        if "--name=" in para or "--account=" in para:
            host.set_account(para[(para.index("=") + 1):])
        elif "--save=" in para or "--dump=" in para:
            host.set_dump_file(para[(para.index("=") + 1):])
        elif "--play=" in para:
            play = player(para[(para.index("=") + 1):])
            host.register_agent(play)
        elif "--evil=" in para:
            evil = rndenv(para[(para.index("=") + 1):])
            host.register_agent(evil)
            
    match_move = re.compile("^#\S+ \S+$") # e.g. "#M0001 ?", "#M0001 #U"
    match_ctrl = re.compile("^#\S+ \S+ \S+$") # e.g. "#M0001 open Slider:Placer", "#M0001 close score=15424"
    arena_ctrl = re.compile("^[@$].+$") # e.g. "@ login", "@ error the account "Name" has already been taken"
    arena_info = re.compile("^[?%].+$") # e.g. "? message from anonymous: 2048!!!"
    
    for command in sys.stdin:
        command = command[:-1]
        try:
            if match_move.match(command):
                id, move = command.split(" ")
                
                if move == "?":
                    # your agent need to take an action
                    a = host.at(id).take_action()
                    host.at(id).apply_action(a)
                    print(id + " " + str(a))
                    
                else:
                    # perform your opponent's action
                    a = action()
                    code = io.StringIO(move)
                    a.load(code)
                    host.at(id).apply_action(a)
            
            elif match_ctrl.match(command):
                id, ctrl, tag = command.split(" ")
                
                if ctrl == "open":
                    # a new match is pending
                    if host.open(id, tag):
                        print(id + " accept")
                    else:
                        print(id + " reject")
                        
                elif ctrl == "close":
                    # a match is finished
                    host.close(id, tag)
                    
            elif arena_ctrl.match(command):
                ctrl = command[1:].strip().split(" ")[0]
                
                if ctrl == "login":
                    # register yourself and your agents
                    agents = [" " + who.name() + "(" + who.role() + ")" for who in host.list_agents()]
                    print("@", "login: " + host.account() + "".join(agents))
                    
                elif ctrl == "status":
                    # display current local status
                    print("+++++ status +++++", file = sys.stderr)
                    agents = [" " + who.name() + "(" + who.role() + ")" for who in host.list_agents()]
                    print("login: " + host.account() + "".join(agents), file = sys.stderr)
                    matches = ["\n% " + ep.name() + ' ' + str(ep) for ep in host.list_matches()]
                    print("match: " + str(len(matches)) + "".join(matches), file = sys.stderr)
                    print("----- status -----", file = sys.stderr)
                    
                elif ctrl == "error" or ctrl == "exit":
                    # error message from arena server
                    message = command[(re.search(r"[^@$ ]", command).start()):]
                    print(message, file = sys.stderr)
                    break
                
            elif arena_info.match(command):
                # message from arena server
                pass
                
        except Exception as ex:
            message = type(ex).__name__ + ": " + str(ex)
            print("?", "exception " + message + " at " + '"' + command + '"')
            print("exception " + message + " at " + '"' + command + '"', file = sys.stderr)
                   
    return

if __name__ == '__main__':
    print('2048 Demo: ' + " ".join(sys.argv))
    print()
    
    total, block, limit = 1000, 0, 0
    play_args, evil_args = "", ""
    load, save = "", ""
    summary = False
    for para in sys.argv[1:]:
        if "--total=" in para:
            total = int(para[(para.index("=") + 1):])
        elif "--block=" in para:
            block = int(para[(para.index("=") + 1):])
        elif "--limit=" in para:
            limit = int(para[(para.index("=") + 1):])
        elif "--play=" in para:
            play_args = para[(para.index("=") + 1):]
        elif "--evil=" in para:
            evil_args = para[(para.index("=") + 1):]
        elif "--load=" in para:
            load = para[(para.index("=") + 1):]
        elif "--save=" in para:
            save = para[(para.index("=") + 1):]
        elif "--summary" in para:
            summary = True
        elif "--shell" in para:
            shell()
            exit()
    
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
    
        