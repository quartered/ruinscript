#!/usr/bin/python

import json, re, urllib, urllib2, colorWrapper

def urban_format(entry, num, totalentries):
    """Formats a dict of urban dictionary data for presentation
    entry -> dict with 'word', 'definition' and 'example' keys
    num -> position of entry in list
    totalentries -> total number of entries in list
    """
    color = colorWrapper.colorWrapper('\x037', '\x03').wrap_color
    max_char = 300
    
    
    total_fmt = totalentries
    if total_fmt == 1:
        total_fmt = '(1 entry)'
    else:
        total_fmt = '(%s entries)' % total_fmt
    
    num_fmt = num
    num_fmt = color('#' + str(num))
    
    word_fmt = entry['word']
    word_fmt = color(word_fmt)
    
    def_fmt = entry['definition']
    def_fmt = re.sub(r'(%s)', color(r'\1'), def_fmt)
    def_fmt = re.sub(r'[\[\]]', r'', def_fmt)
    def_fmt = re.sub(r'[\n\r]+', color(r' |') + ' ', def_fmt[:max_char])
    if len(def_fmt) >= max_char:
        def_fmt += color(' ...')
    
    ex_fmt = entry['example']
    ex_fmt = re.sub(r'(%s)', color(r'\1'), ex_fmt)
    ex_fmt = re.sub(r'[\[\]]', r'', ex_fmt)
    ex_fmt = re.sub(r'[\n\r]+', color(r' |') + ' ', ex_fmt[:max_char])
    if len(ex_fmt) >= max_char:
        ex_fmt += color(' ...')
        
    return {'definition': '[ %s ] %s %s %s Definition: %s' % (color('URBAN'),
                                                              word_fmt,
                                                              total_fmt,
                                                              num_fmt,
                                                              def_fmt),
            'example': '%s %s Example: %s' % (word_fmt, num_fmt, ex_fmt)}
        
def on_urban(conn, target, searchterm, num):
    if searchterm is not None:
        searchterm = urllib.quote(searchterm)
        print searchterm
        try:
            data_string = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=' + searchterm).read()
        except Exception, e:
            print searchterm, '| on_urban error during urlopen:', e
            return
        try:
            decoded = json.loads(data_string)
        except Exception, e:
            print searchterm, '| on_urban error during json decode:', e
            return
        if 'list' in decoded:
            urbandict = decoded['list']
        else:
            print searchterm, '| decoded json contained no "list" element'
            return
        
        if not num:
            num = 1
        else:
            try:
                num = int(num)
            except ValueError:
                num = 1
        if num > len(urbandict):
            num = len(urbandict)
    
        fmt_dict = urban_format(urbandict[num-1], num, len(urbandict))
    
        conn.send('%s %s :%s' % ('PRIVMSG', target, fmt_dict['definition']))
        conn.send('%s %s :%s' % ('PRIVMSG', target, fmt_dict['example']))
