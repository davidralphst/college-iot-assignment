from gpiozero import MotionSensor
import time
from datetime import datetime

# database
import sqlite3
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS intrusion (id INTEGER PRIMARY KEY AUTOINCREMENT, time text)''')

# painful
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

pir = MotionSensor(17)

while True:
  pir.wait_for_motion()
  print("No intruders")
  time.sleep(0.1)
  pir.wait_for_no_motion()
  print("Intruder detected")
  time.sleep(0.1)
  # write intrusion time etc to database
  c.execute("INSERT INTO intrusion VALUES (NULL, ?)", (get_time(),))
