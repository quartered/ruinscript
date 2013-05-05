#!/usr/bin/python

import re, os, commands, sys, random, operator, difflib, sqlite3, urllib, urllib2, urlparse
import parseQuestions

answeredQuestion = True;
category = 'dsadasfsad'
categorySet = True
questionID = 0
answers = []
num = 1
guessCount=0
maxGuesses=10
results = {}
categories = None

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

def getCategories():
    global categories
    con = None
    categories = None
    try:
        con = sqlite3.connect('questions.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT DISTINCT category FROM q')
        categories = cur.fetchall()
    except sqlite3.Error, e:
        print 'Error %s' % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()

def categoryExists(pCategory):
    if any(pCategory.lower() in category[0].lower() for category in categories):
        return True
    else:
        return False

def getDBQuestion(pcategory):
    global questionID
    global category
    global answers
    global answeredQuestion
    question = ''
    con = None
    answers[:] = []
    try:
        con = sqlite3.connect('questions.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if pcategory == 'ALL':
            cur.execute('SELECT * FROM q ORDER BY RANDOM() LIMIT 1')
        else:
            cur.execute('SELECT * FROM q WHERE UPPER(category) = UPPER(\'%s\') ORDER BY RANDOM() LIMIT 1' % (pcategory))
        row = cur.fetchone()
        questionID = row['id']
        category = row['category']
        question = row['question']

        cur.execute('SELECT answer FROM a WHERE questionid = %s' % (questionID))
        rows = cur.fetchall()
        for answer in rows:
            answers.append(answer[0])

    except sqlite3.Error, e:
        print 'Error %s' % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()
    answeredQuestion = False;
    return question

def getQuestion():
    global category
    global answers
    global answeredQuestion
    file = open('/d/q.txt')
    line = random_line(file)
#    line = line.replace('\"','')
    answers = line.split('\t')
    #Remove Topic and question from answer list
    category = answers.pop(0).strip(os.linesep)
    question = answers.pop(0).strip(os.linesep)
    #print len(answers)

    answeredQuestion = False;
    return question

def on_categories(conn, target):
    catString = ", ".join([t[0] for t in categories])
    conn.send('%s %s :%s' % ('PRIVMSG', target, catString))

def on_stop(conn, target):
    global answeredQuestion
    if answeredQuestion == False:
        answeredQuestion = True
        conn.send('%s %s :Stopping.' % ('PRIVMSG', target))

def on_category(conn, target, cat):
    global category
    global categorySet
    if not cat:
        cat = 'ALL'
        categorySet = False;
    if categoryExists(cat) or cat == 'ALL':
        category = cat
        categorySet = True;
        conn.send('%s %s :Changing category.' % ('PRIVMSG', target))
    else:
        conn.send('%s %s :Category doesn\'t exist.' % ('PRIVMSG', target))

def on_add(conn, fullhost, nick, ident, hostname, command, target, filename):
    if '%s@%s' % (ident, hostname) in sys.argv[3:]:
        parseQuestions.parseQuestions(filename)
        getCategories()
        conn.send('%s %s :Adding questions from file: %s' % (command, target, filename))
    else:
        conn.send('%s %s :No.' % (command, target))

def on_delete(conn, fullhost, nick, ident, hostname, command, target, qID):
    if '%s@%s' % (ident, hostname) in sys.argv[3:]:
        try:
            con = sqlite3.connect('questions.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Check if question exists
            cur.execute('SELECT * FROM q WHERE id = %s' % (qID) )
            row = cur.fetchone()
            question = row['question']
            cur.execute('DELETE FROM q WHERE id = %s' % (qID))
            conn.send('%s %s :Question deleted: %s' % (command, target, question))
        except Exception, e:
            print 'Error 3: %s' % (e.args[0])
            conn.send('%s %s :Unable to delete question. Check the ID and try again' % (command, target))
        finally:
            if con:
                con.commit()
                con.close()
                getCategories()
    else:
        conn.send('%s %s :No.' % (command, target))

def on_answer(conn, fullhost, nick, ident, hostname, command, target, qID, newanswer):
    if '%s@%s' % (ident, hostname) in sys.argv[3:]:
        question = ''
        answer = ''
        con = None
        answers = []
        try:
            con = sqlite3.connect('questions.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Check if question exists
            cur.execute('SELECT * FROM q WHERE id = %s' % (qID) )

            row = cur.fetchone()
            questionID = row['id']
            category = row['category']
            question = row['question']
            try:
                cur.execute('SELECT * FROM a WHERE questionid = %s AND lower(answer) = lower(\'%s\')' %(qID, newanswer) )
                row = cur.fetchone()
                answer = row['answer']
                conn.send('%s %s :Answer already exists for \'%s\': %s' % (command, target, question, answer))
                
            except Exception, e:
                try:
                    cur.execute('INSERT INTO a(questionid, answer) VALUES (%s,\'%s\')'% (qID, newanswer))
                    conn.send('%s %s :Adding answer to \'%s\'' % (command, target, question))
                except Exception, e:
                    print 'Error 1: %s' % (e.args[0])
                print 'Error 2: %s' % (e.args[0])
        except Exception, e:
            print 'Error 3: %s' % (e.args[0])
            conn.send('%s %s :Unable to add answer. Check the ID and try again' % (command, target))
        finally:
            if con:
                con.commit()
                con.close()
    else:
        conn.send('%s %s :No.' % (command, target))

def on_score(conn, fullhost, nick, ident, hostname, command, target):
    try:
        s = results[nick]
        leader = max(results.iteritems(), key=operator.itemgetter(1))[0]
        leaderPoints = results[leader]
        if leader == nick:
            conn.send('%s %s :You are currently in the lead with %s' % (command, target, s))
        else:
            conn.send('%s %s :You currently have %s. %s is currently in the lead with %s' % (command, target, s, leader, leaderPoints))
    except:
        conn.send('%s %s :You are currently on 0' % (command, target))

def on_trivia(conn, target, cat):
    global answeredQuestion
    global category
    global categorySet
    global num
    global guessCount
    if not cat or not categorySet:
        cat='ALL'
    else:
        categorySet=True
    print categoryExists(cat)
    print cat
    if answeredQuestion:
        if categoryExists(cat):
            q = getDBQuestion(cat)
            conn.send('%s %s :[%s] %s: %s (%s)' % ('PRIVMSG', target, category, num, q, questionID))
            num += 1
        else:
            conn.send('%s %s :Category doesn\'t exist. Picking one at random.' % ('PRIVMSG', target))
            q = getDBQuestion('ALL')
            conn.send('%s %s :[%s] %s: %s (%s)' % ('PRIVMSG', target, category, num, q, questionID))
            num += 1

        guessCount = 0

def on_next(conn, target, cat):
    global answeredQuestion
    global categorySet

    if answeredQuestion == False:
        answeredQuestion = True
        conn.send('%s %s :Skipping question. Correct answer: %s' % ('PRIVMSG', target, answers[0]))
        if not cat or categorySet:
            on_trivia(conn, target, category)
        else:
            on_trivia(conn, target, cat)

def on_answercheck(conn, fullhost, nick, ident, hostname, command, target, message):
    global answeredQuestion
    global guessCount
    #print category
    if not answeredQuestion:
        if guessCount == maxGuesses:
            answeredQuestion = True
            conn.send('%s %s :No one got it. The answer was: %s' % (command, target, answers[0]))
            on_trivia(conn, target, category)

        guessCount += 1
        for answer in answers:
            if answer is not None:
                #print difflib.SequenceMatcher(None, answer.lower(), message.lower()).ratio()
                if message.lower() == answer.lower():
                    if nick not in results:
                        results[nick] = 1
                    else:
                        results[nick] += 1
                    conn.send('%s %s :Correct %s, the answer was %s. Your score is now %s ' % (command, target, nick, answers[0], results[nick]))
                    answeredQuestion = True
                    on_trivia(conn, target, category)
