#!/usr/bin/python
import urllib, urllib2, urlparse
from xml.etree import ElementTree 
from xml.dom import minidom

url = 'http://www.youtube.com/watch?v=IKH8vr0oM8g'
#url = 'http://www.youtube.com/watch?v=fOQ_XBDv1XU'
#url = 'http://www.youtube.com/watch?NR=1&feature=endscreen&v=fOQ_XBDv1XU'
#url = 'http://www.youtube.com/watch?v'
searchterm = 'pls work'
def yt_format(tree, showurl):
#    for e in tree.iter():
#        print e.tag
    result = '[\x037 YOUTUBE \x03]' 
#    result += 'Published: %s | ' % (tree.find('{http://www.w3.org/2005/Atom}published').text)
    result += ' Title:\x037 %s' % (tree.find('{http://www.w3.org/2005/Atom}title').text)
    result += ' \x03| Uploader:\x037 %s' % (tree.find('{http://www.w3.org/2005/Atom}author')[0].text)
    result += ' \x03| Duration:\x037 %s' % (tree.find('{http://search.yahoo.com/mrss/}group/{http://gdata.youtube.com/schemas/2007}duration').get('seconds'))
    result += ' \x03| Views:\x037 %s' % (tree.find('{http://gdata.youtube.com/schemas/2007}statistics').get('viewCount'))

    if tree.find('{http://schemas.google.com/g/2005}rating') is not None:
        result += ' \x03| Rating:\x037 %s ' % (tree.find('{http://schemas.google.com/g/2005}rating').get('average'))
        result += '(\x037 %s \x03ratings )' % (tree.find('{http://schemas.google.com/g/2005}rating').get('numRaters'))


    if (showurl == 1):
        result += ' \x03| URL:\x037 https://youtu.be/%s \x03' % (tree.find('{http://search.yahoo.com/mrss/}group/{http://gdata.youtube.com/schemas/2007}videoid').text)

    return result

if __name__ == '__main__':


    parsed = urlparse.urlparse(url)
    if 'v' in urlparse.parse_qs(parsed.query):
        video_id = urlparse.parse_qs(parsed.query)['v'][0]
        data = 'https://gdata.youtube.com/feeds/api/videos/%s?v=2' % (video_id)
        data = 'https://gdata.youtube.com/feeds/api/videos?start-index=1&max-results=1&v=2&q=%s' % (urllib.quote(searchterm))
        print data
        req = urllib2.Request(data)
        response = urllib2.urlopen(req)
        
        tree = ElementTree.parse(response)
        tree = tree.find('{http://www.w3.org/2005/Atom}entry')
        print yt_format(tree,1)

