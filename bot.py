#!/usr/bin/python

import irc, re, os, commands, sys, random, operator, difflib, sqlite3, urllib, urllib2, urlparse
from xml.etree import ElementTree 
import parseQuestions
import urban
import trivia
import youtube
import tv
bindip = '2001:41d0:8:912b:0:0:0:2'
connect_info = {'nick': 'notcraig',
                        'ident': 'notcraig',
                        'realname': 'notcraig',
                        'server address': ('irc.swiftirc.net', 6667),
                        'ajoin channel': '#gudhak'}
                        
bot_vars = {}

def main():
    bot = irc.IRC()
    bot.add_bot_hook('connect', on_connect)
    bot.add_hook('on_ping', on_ping, r'^PING :(?P<server>.+)$', re.I)
    bot.add_hook('on_welcome', on_welcome, r':(?P<server>[^ ]+) 001 (?P<nick>[^ ]+) :(?P<welcome_message>.+)', re.I)
    bot.add_hook('on_all', on_all, r'(.+)', re.I)
    bot.add_hook('on_youtube', youtube.on_youtube, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :.*(https?://)?(www\.)?youtu(\.be|be\.com)/(watch\?.*v=|)(?P<vid>[\w-]{11})', re.I)
    bot.add_hook('on_ytsearch', youtube.on_ytsearch, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :@yt(?: (?P<searchterm>.+))?', re.I)
    bot.add_hook('on_answercheck', trivia.on_answercheck, r':(?P<fullhost>(?P<nick>[^!]+)!(?P<ident>[^@]+)@(?P<hostname>[^ ]+)) (?P<command>[^ ]+) (?P<target>[^ ]+) :(?P<message>.+)')
    bot.add_hook('on_categories', trivia.on_categories, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :!categories', re.I)
    bot.add_hook('on_stop', trivia.on_stop, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :!stop', re.I)
    bot.add_hook('on_next', trivia.on_next, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :!next(?: (?P<cat>.+))?', re.I)
    bot.add_hook('on_category', trivia.on_category, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :!category(?: (?P<cat>.+))?', re.I)
    bot.add_hook('on_score', trivia.on_score, r':(?P<fullhost>(?P<nick>[^!]+)!(?P<ident>[^@]+)@(?P<hostname>[^ ]+)) (?P<command>[^ ]+) (?P<target>[^ ]+) :!score', re.I)
    bot.add_hook('on_add', trivia.on_add, r':(?P<fullhost>(?P<nick>[^!]+)!(?P<ident>[^@]+)@(?P<hostname>[^ ]+)) (?P<command>[^ ]+) (?P<target>[^ ]+) :!add(?: (?P<filename>.+))?', re.I)
    bot.add_hook('on_delete', trivia.on_delete, r':(?P<fullhost>(?P<nick>[^!]+)!(?P<ident>[^@]+)@(?P<hostname>[^ ]+)) (?P<command>[^ ]+) (?P<target>[^ ]+) :!delete (?P<qID>[^ ].+)?', re.I)
    bot.add_hook('on_answer', trivia.on_answer, r':(?P<fullhost>(?P<nick>[^!]+)!(?P<ident>[^@]+)@(?P<hostname>[^ ]+)) (?P<command>[^ ]+) (?P<target>[^ ]+) :!answer (?P<qID>[^ ]+) (?P<newanswer>.+)?', re.I)
    bot.add_hook('on_trivia', trivia.on_trivia, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :!trivia(?: (?P<cat>.+))?', re.I)
#    bot.add_hook('on_tvinfo', tv.on_tvinfo, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :@tv(?: (?P<searchterm>.+))?', re.I)
#    bot.add_hook('on_tvnext', tv.on_tvnext, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :@next(?: (?P<searchterm>.+))?', re.I)
#    bot.add_hook('on_urban', urban.on_urban, r':[^!]+![^@]+@[^ ]+ PRIVMSG (?P<target>[^ ]+) :[!@.](urban|ud) (?P<searchterm>.+)(?: #(?P<num>\d\d))?', re.I)
    bot.connect(connect_info['server address'])#, (bindip,0))
    
def on_connect(conn, event):
    print sys.argv[1]
    conn.send('NICK %s' % (sys.argv[2]))
    conn.send('USER %s 0 * :%s' % (sys.argv[2], sys.argv[2]))

def on_welcome(conn, server, nick, welcome_message):
    bot_vars['nick'] = nick
    conn.send('%s %s :id %s' % ('PRIVMSG', 'nickserv', sys.argv[4]))
    conn.send('JOIN #' + sys.argv[1])
    trivia.getCategories()

def on_ping(conn, server):
    conn.send('PONG :' + server)

def on_all(conn, msg):
    msg.split()
    print msg

if __name__ == '__main__':
    main()
    
