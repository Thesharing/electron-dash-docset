#!/usr/bin/env python

import os
import sys
import re
import sqlite3
from bs4 import BeautifulSoup


def build_tutorial_index(soup, cursor):
    api = re.compile('tutorial')
    for tag in soup.find_all('a', {'href': api}):
        name = tag.text.strip()

        if len(name) > 0:
            path = tag.attrs['href'].strip()
            if "://" in path:
                continue
            path = subpath + path

            if path.split('#')[0] not in ['index.html']:
                cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                               (name, 'Guide', path))
                print('[Guide] Name: %s, Path: %s' % (name, path))


def build_development_index(soup, cursor):
    api = re.compile('development')
    for tag in soup.find_all('a', {'href': api}):
        name = tag.text.strip()

        if len(name) > 0:
            path = tag.attrs['href'].strip()
            if "://" in path:
                continue
            path = subpath + path

            if path.split('#')[0] not in ['index.html']:
                cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                               (name, 'Guide', path))
                print('[Guide] Name: %s, Path: %s' % (name, path))


def build_module_index(soup, cursor):
    api = re.compile('api')
    for tag in soup.find_all('a', {'href': api}):
        name = tag.text.strip()

        if len(name) > 0:
            path = tag.attrs['href'].strip()
            if "://" in path:
                continue

            if path.split('#')[0] not in ['index.html']:
                cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                               (name, 'Module', path))
                print('[Module] Name: %s, Path: %s' % (name, path))


def build_api_index(base_path, cursor):
    docpath = os.path.join(base_path, 'Documents/docs/api/')
    page = open(os.path.join(docpath, 'index.html'), encoding='utf-8').read()
    soup = BeautifulSoup(page, "html.parser").find('table')
    for tag in soup.find_all('a'):
        name = tag.text.strip()

        if len(name) > 0:
            path_name = tag.attrs['href'].strip()
            if "://" in path_name:
                continue
            path = 'docs/api/' + path_name

            if path.split('#')[0] not in ['index.html']:
                cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                               (name, 'Class', path))
                print('[Class] Name: %s, Path: %s' % (name, path))
                build_sub_api_index(os.path.join(docpath + path_name), cursor)


def build_sub_api_index(path, cursor):
    page = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(page, "html.parser")
    api = re.compile('.+?\..+?\(.+?\)')
    for tag in soup.find_all('a'):
        name = tag.text.strip()
        if len(name) > 0 and api.fullmatch(name) is not None:
            if 'href' in tag.attrs:
                path_name = tag.attrs['href'].strip()
                if '://' in path_name:
                    continue
                full_path = 'docs/api/' + path_name

                if full_path.split('#')[0] not in ['index.html']:
                    cursor.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                                   (name, 'Method', full_path))
                    print('[Method] Name: %s, Path: %s' % (name, full_path))


if __name__ == '__main__':
    # getting the folder where the script lives
    abs_work_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    base_path = os.path.join(abs_work_path, 'output/electron.docset/Contents/Resources/')

    # Set up sqlite db
    db = sqlite3.connect(os.path.join(base_path, 'docSet.dsidx'))
    cursor = db.cursor()

    # Drop search table if it already exists
    try:
        cursor.execute('DROP TABLE searchIndex;')
    except:
        pass

    # Create search table
    cursor.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cursor.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    subpath = 'docs/'
    docpath = base_path + '/Documents/'

    page = open(docpath + 'docs.html', encoding = 'utf-8').read()
    soup = BeautifulSoup(page, "html.parser")

    build_tutorial_index(soup, cursor)
    build_development_index(soup, cursor)
    build_module_index(soup, cursor)
    build_api_index(base_path, cursor)

    # Make db changes permanent
    db.commit()
    db.close()
