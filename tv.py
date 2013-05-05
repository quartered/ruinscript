import urllib2

def on_tvinfo(conn, target,searchterm):
    if searchterm is not None:
        searchterm = searchterm.replace(' ', '%20')
        html = urllib2.urlopen('http://services.tvrage.com/tools/quickinfo.php?show=' + searchterm).read()
        data = html.split('\n')
        z = 0
        
        for x in data:
            y = x.split('@')
            if y[0] == 'Show Name':
                showName = y[1]
            elif y[0] == 'Premiered':
                showPremiered = y[1]
            elif y[0] == 'Started':
                showStarted = y[1]
            elif y[0] == 'Ended':
                if y[1]:
                    showEnded = y[1]
                else:
                    showEnded = 'Still Running'
            elif y[0] == 'Country':
                showCountry = y[1]
            elif y[0] == 'Genres':
                showGenres = y[1]
            elif y[0] == 'Network':
                showNetwork = y[1]
            elif y[0] == 'Airtime':
                showAirTime = y[1]
            elif y[0] == 'Runtime':
                showRunTime = y[1]
    
        conn.send('%s %s :[ TV ] Show Name: %s | Premiered: %s | Started: %s | Ended: %s | Country: %s ' % ('PRIVMSG', target, showName, showPremiered, showStarted, showEnded, showCountry ))
        conn.send('%s %s :Genres: %s | Network: %s | Airtime: %s ' % ('PRIVMSG', target, ', '.join(showGenres.split('|')), showNetwork, showAirTime ))
        
def on_tvnext(conn, target,searchterm):
    if searchterm is not None:
        searchterm = searchterm.replace(' ', '%20')
        html = urllib2.urlopen('http://services.tvrage.com/tools/quickinfo.php?show=' + searchterm).read()
        data = html.split('\n')
        z = 0

    showName,showNextRaw = None, None
        
    for x in data:
        y = x.split('@')
        if y[0] == 'Show Name':
            showName = y[1]
        elif y[0] == 'Next Episode':
            showNextRaw =  y[1]
    if showNextRaw:
        showNext = showNextRaw.split('^')
    else:
        showNext = None

        if not showName:
            conn.send('%s %s :[ TV ] Couldn\'t find a show with that name ' % ('PRIVMSG', target))
        elif not showNext[0]:
            conn.send('%s %s :[ TV ] Next episode is not available ' % ('PRIVMSG', target))
        else:
            conn.send('%s %s :[ TV ] The next episode of %s is %s (%s) on %s' % ('PRIVMSG', target, showName, showNext[1], showNext[0], showNext[2]))

#def last(phenny, input):
#    show = input.split(' ')[1:]
#    show = ' '.join(show)
#    if not show:
#        phenny.reply('Sorry, you did not supply a show name')
#    else:
#        show = show.replace(' ', '%20')
#        html = urllib2.urlopen('http://services.tvrage.com/tools/quickinfo.php?show=' + show).read()
#        data = html.split('\n')
#        z = 0
#    showName,showLastRaw = None, None
#    for x in data:
#            y = x.split('@')
#            if y[0] == 'Show Name':
#                showName = y[1]
#            elif y[0] == 'Latest Episode':
#                showLastRaw =  y[1]
#    if showLastRaw:
#        showLast = showLastRaw.split('^')
#    else:
#        showLast = None
#
#        if not showName:
#            phenny.say('Could not find tv show with that name')
#        elif not showLast[0]:
#            phenny.say('Last episode of not available')
#        else:
#            phenny.say('\002Last -->\002 The last episode of \037' + showName + '\037 was \037' + showLast[1] + '\037 (' + showLast[0] + ') on ' + showLast[2])
#
#last.commands = ['last']
#last.example = '.last House'

