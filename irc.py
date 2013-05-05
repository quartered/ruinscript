#!/usr/bin/python

import socket
import re

class IRC:
    hook_dict = {}
    bot_hook_dict = {}
    def __init__(self):
        pass
    def connect(self, serveraddress, bindaddress=('0.0.0.0', 0)):
        self.conn = socket.socket()
        self.conn.bind(bindaddress)
        self.conn.connect(serveraddress)
        
        self.call_bot_event('connect')
        self.conn_loop(self.conn)
    def conn_loop(self, conn):
        recv = ''
        while 1:
            recv += conn.recv(1024)
            while '\r\n' in recv:
                (msg, rn, recv) = recv.partition('\r\n')
                self.irc_handler(msg)
                
    def bot_handler(self, event):
        for func in self.bot_hook_dict[event]:
            func(self, event)
    def add_bot_hook(self, name, callback):
        if not callable(callback):
            raise TypeError("'%s' object is not callable" % 
type(callback))
        try:
            self.bot_hook_dict[name].append(callback)
        except KeyError:
            self.bot_hook_dict[name] = [callback]
    def call_bot_event(self, event):
        try:
            self.bot_handler(event)
        except KeyError:
            pass
            
    def irc_handler(self, msg):
        for name in self.hook_dict:
            match = self.hook_dict[name][0].match(msg)
            if match:
                if match.groupdict():
                    self.hook_dict[name][1](self, **match.groupdict())
                else:
                    self.hook_dict[name][1](self, *match.groups())
    def add_hook(self, name, callback, regex, re_flags=0):
        '''add_hook(name, callback, regex)
        adds key to hook_dict, {'name': (regex, callback)}'''
        if not callable(callback):
            raise TypeError("'%s' object is not callable" % 
type(callback))
        if name in self.hook_dict:
            raise ValueError("Key '%s' is already present" % name)
        self.hook_dict[name] = (re.compile(regex, re_flags), callback)
    def del_hook(self, name):
        try:
            del self.hook_dict[name]
        except KeyError:
            raise KeyError("Key '%s' not found" % name)
            
    def send(self, msg):
        self.conn.send(msg+'\r\n')
        print "debug ->> " + msg
