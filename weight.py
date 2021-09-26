#!/usr/bin/env python3

"""
Framework for 2048 & 2048-like Games (Python 3)
weight.py: Lookup table template for n-tuple network

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NYCU, Taiwan
        https://cgilab.nctu.edu.tw/
"""

from array import array


class weight:

    def __init__(self, len = 0):
        self.value = [0] * len
        return

    def __getitem__(self, index):
        return self.value[index]

    def __setitem__(self, index, value):
        self.value[index] = value
        return

    def __len__(self):
        return len(self.value)

    def save(self, output):
        """ serialize this weight to a file object """
        array('Q', [len(self.value)]).tofile(output)
        array('f', self.value).tofile(output)
        return True

    def load(self, input):
        """ deserialize from a file object """
        size = array('Q')
        size.fromfile(input, 1)
        size = size[0]
        value = array('f')
        value.fromfile(input, size)
        self.value = list(value)
        return True
