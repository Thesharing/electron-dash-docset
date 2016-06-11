#!/usr/bin/env python

import os
import re
import sqlite3
from bs4 import BeautifulSoup


db = sqlite3.connect('electron.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

subpath = 'docs/'
docpath = os.getcwd()+'/electron.docset/Contents/Resources/Documents/'+subpath

page = open(os.path.join(docpath, 'index.html')).read()
soup = BeautifulSoup(page, "html.parser")

any = re.compile('tutorial')
for tag in soup.find_all('a', {'href': any}):
    name = tag.text.strip()
    if len(name) > 0:
        path = tag.attrs['href'].strip()
        path = subpath+'/'+path
        if path.split('#')[0] not in ('index.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Guide', path))
            print 'name: %s, path: %s' % (name, path)

any = re.compile('development')
for tag in soup.find_all('a', {'href': any}):
    name = tag.text.strip()
    if len(name) > 0:
        path = tag.attrs['href'].strip()
        path = subpath+'/'+path
        if path.split('#')[0] not in ('index.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Guide', path))
            print 'name: %s, path: %s' % (name, path)

any = re.compile('api')
for tag in soup.find_all('a', {'href': any}):
    name = tag.text.strip()
    if len(name) > 0:
        path = tag.attrs['href'].strip()
        path = subpath+'/'+path
        if path.split('#')[0] not in ('index.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Module', path))
            print 'name: %s, path: %s' % (name, path)

db.commit()
db.close()
