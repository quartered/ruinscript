#!/usr/bin/python

import re, os, commands, sys, random, operator, difflib, sqlite3, urllib2

class parseQuestions:
    def insertQuestion(self, category, question, answers):
        con = None
        try:
            con = sqlite3.connect('questions.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()
    
            row = (category, question)
            cur.execute('INSERT INTO q (category, question) VALUES(?, ?)', row)
            cur.execute('SELECT * FROM q WHERE category = ? AND question = ?', row)
            row = cur.fetchone()
            questionid = row['id']
            for answer in answers:
                print questionid, answer
                row = (questionid, answer)
                cur.execute('INSERT INTO a (questionid, answer) VALUES(?, ?)', row)
    
        except sqlite3.Error, e:
            print 'Error %s' % e.args[0]
            sys.exit(1)
        finally:
            if con:
                con.commit()
                con.close()
    
    def getFileContents(self, filename):
        try:
            f = urllib2.urlopen(filename)
            lines = f.readlines()
            f.close()
            return lines
        except:
            print 'Exception thrown. Are you sure the file exists?'
            return {}
    
    def formatContents(self, line):
        print line
        spl = line.split('/')
        category = spl[1]
        answers = spl[2:-2]
        question = spl[-1].strip('\n\r')
    
        print "[%s] %s: %s" % (category, question, answers)
        self.insertQuestion(category, question, answers)
    def __init__(self, filename):
        print filename
        for line in self.getFileContents(filename):
#            self.formatContents(line.decode('utf-8'))
            self.formatContents(line)

