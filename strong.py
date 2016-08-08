#!/usr/bin/env python3

import sqlite3
from xml.dom import minidom
import random

conn = sqlite3.connect('strongs.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS new_strong_combined (strongs TEXT, greek TEXT, beta TEXT, stnumbers TEXT)')


def data_entry(strongs, greek, beta, stnumbers):
    c.execute('INSERT INTO new_strong_combined VALUES (?, ?, ?, ?)', 
            (strongs, greek, beta, stnumbers))
    conn.commit()


#def dynamic_data_entry():
    

xmldoc = minidom.parse('strongsgreek2.xml')
entries = xmldoc.getElementsByTagName('entries')[0]
entry = entries.getElementsByTagName('entry')
create_table() 

for item in entry:
    try:
        strongs = item.getAttribute('strongs')
        beta = item.getElementsByTagName('greek')[0].getAttribute('BETA')
        greek = item.getElementsByTagName('greek')[0].getAttribute('unicode')
        strong_dev = item.getElementsByTagName('strongs_derivation')[0]
        strongsrefls = []
        try: 
            for i in strong_dev.getElementsByTagName('strongsref'):
                number = i.getAttribute('strongs')
                strongsrefls.append(number)
        except AttributeError:
            continue
        strongsrefls = strongsrefls[::-1]
        refls = ','.join(strongsrefls)
        data_entry(strongs, greek, beta, refls)
    except:
        continue
    
c.close()
conn.close()

