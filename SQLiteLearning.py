import urllib
import twurl
import json
import sqlite3

TWITTER_URL =  'https://api.twitter.com/1.1/friends/list.json'

conn = sqlite3.connect('spider.sqlite3')
cur = conn.cursor()

cur.execute("'CREATE TABLE IF NOT EXISTS Twitter (name TEXT, retrieved INTEGER, friends INTEGER)'")

while True:
    acct = raw_input('Enter a Twitter account, or quit: ')
    if (acct == 'quit') : break
    if (len(acct) < 1):
        cur.execute('SELECT  name FROM Twitter WHERE retrived = 0 LIMIT 1')
        try:
            acct = cur.fetchone()[0]
        except:
            print('No unretrived Twitter accounts found')
            continue

