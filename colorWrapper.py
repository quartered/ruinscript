#!/usr/bin/python

class colorWrapper:
    def __init__(self, start, end=''):
        self.start = start
        self.end = end
   
    def wrap_color(self, text):
        return self.start + text + self.end
