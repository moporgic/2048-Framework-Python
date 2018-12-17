#!/usr/bin/env python3

"""
Basic framework for developing 2048 programs in Python

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""


from board import board
from action import action
from episode import episode
from statistic import statistic
from agent import agent
from ctypes.test.test_pickling import name


class match(episode):
    
    def __init__(self, id, play, evil):
        super(match, self).__init__()
        self.id = id
        self.play = play
        self.evil = evil
        return
    
    def name(self):
        return self.id
    
    def take_action(self):
        who = self.take_turns(self.play, self.evil)
        return who.take_action(self.state())
    
class arena:
    
    def __init__(self, name = "anonymous", path = None):
        self.ongoing = {}
        self.lounge = {}
        self.name = name
        self.dump = None
        if path is not None:
            self.set_dump_file(path)
        return
    
    def __getitem__(self, index):
        return self.ongoing[index]
    
    def __setitem__(self, index, value):
        self.ongoing[index] = value
        return
    
    def __len__(self):
        return len(self.ongoing)
    
    def at(self, id):
        return self.ongoing[id]
    
    def open(self, id, tag):
        if id in self.ongoing:
            return False
        play = self.find_agent(tag[:tag.index(":")], "play")
        evil = self.find_agent(tag[(tag.index(":") + 1):], "evil")
        if play.role() == "dummy" and evil.role() == "dummy":
            return False
        
        m = match(id, play, evil)
        m.open_episode(tag)
        self.ongoing[id] = m
        return True
    
    def close(self, id, tag):
        if not id in self.ongoing:
            return False
        m = self.ongoing[id]
        m.close_episode(tag)
        if self.dump is not None:
            self.dump.write(str(m) + "\n")
            self.dump.flush()
        self.ongoing.pop(id, None)
        return True
    
    def register_agent(self, a):
        if a.name() in self.lounge:
            return False
        self.lounge[a.name()] = a
        return True
    
    def remove_agent(self, a):
        return self.lounge.pop(a.name(), None)
    
    def find_agent(self, name, role):
        if name[0] == "$" and name[1:] == self.account():
            for who in self.lounge.values():
                if who.role()[0] == role[0]:
                    return who
        if name in self.lounge and self.lounge[name].role()[0] == role[0]:
            return self.lounge[name]
        return agent("name=" + name + " role=dummy")
    
    def list_matches(self):
        return self.ongoing.values()
    
    def list_agents(self):
        return self.lounge.values()
    
    def account(self):
        return self.name
    
    def set_account(self, name):
        self.name = name
        
    def set_dump_file(self, path):
        if self.dump is not None:
            self.dump.close()
        self.dump = open(path, "a")
    
    