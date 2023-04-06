import time
from datetime import datetime

# database
import sqlite3
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# create table if not exists with id and time
c.execute('''CREATE TABLE IF NOT EXISTS intrusion (id INTEGER PRIMARY KEY AUTOINCREMENT, time text)''')

# painful
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

c.execute("INSERT INTO intrusion VALUES (NULL, ?)", (get_time(),))
conn.commit()