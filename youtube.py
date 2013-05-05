#!/usr/bin/python

import irc, re, os, commands, sys, random, operator, difflib, sqlite3, urllib, urllib2, urlparse
from xml.etree import ElementTree 

def yt_format(tree, showurl):
    result = '[\x037 YOUTUBE \x03]'
#    result += 'Published: %s | ' % (tree.find('{http://www.w3.org/2005/Atom}published').text)
    result += ' Title:\x037 %s' % (tree.find('{http://www.w3.org/2005/Atom}title').text)
    result += ' \x03| Uploader:\x037 %s' % (tree.find('{http://www.w3.org/2005/Atom}author')[0].text)
    result += ' \x03| Duration:\x037 %s' % (tree.find('{http://search.yahoo.com/mrss/}group/{http://gdata.youtube.com/schemas/2007}duration').get('seconds'))
    result += ' \x03| Views:\x037 %s' % (tree.find('{http://gdata.youtube.com/schemas/2007}statistics').get('viewCount'))

    if tree.find('{http://schemas.google.com/g/2005}rating') is not None:
        result += ' \x03| Rating:\x037 %s \x03' % (tree.find('{http://schemas.google.com/g/2005}rating').get('average'))
        result += '(\x037 %s \x03ratings )' % (tree.find('{http://schemas.google.com/g/2005}rating').get('numRaters'))


    if (showurl == 1):
        result += ' \x03| URL:\x037 https://youtu.be/%s \x03' % (tree.find('{http://search.yahoo.com/mrss/}group/{http://gdata.youtube.com/schemas/2007}videoid').text)

    return result

def on_ytsearch(conn, target,searchterm):
    if searchterm is not None:
        data = 'https://gdata.youtube.com/feeds/api/videos?start-index=1&max-results=1&v=2&q=%s' % (urllib.quote(searchterm))
        try:
            req = urllib2.Request(data)
            response = urllib2.urlopen(req)
    
            tree = ElementTree.parse(response)
            tree = tree.find('{http://www.w3.org/2005/Atom}entry')
    
            conn.send('%s %s :%s' % ('PRIVMSG', target, yt_format(tree,1)))
        except Exception, e:
            print 'Error 3: Youtube URL: %s' % (data)

def on_youtube(conn, target,vid):
    data = 'https://gdata.youtube.com/feeds/api/videos/%s?v=2' % (vid)
    try:
        
        req = urllib2.Request(data)
        response = urllib2.urlopen(req)
                    
        tree = ElementTree.parse(response)
        conn.send('%s %s :%s' % ('PRIVMSG', target, yt_format(tree,0)))
    except Exception, e:
        print 'Error 3: Youtube URL: %s' % (data)

if __name__ == '__main__':
    main()
    
