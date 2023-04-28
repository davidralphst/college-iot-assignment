from gpiozero import MotionSensor
from datetime import datetime
import subprocess

# databases
import sqlite3
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS intrusion (id INTEGER PRIMARY KEY AUTOINCREMENT, time text)''')
conn.commit()

# util function
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# init devices
pir = MotionSensor(17)

# main loop
while True:
  pir.wait_for_motion()
  print("Intruder detected")
  # write intrusion time etc to database and photo
  subprocess.call(["fswebcam", "../photos/" + get_time() + ".jpg"])
  c.execute("INSERT INTO intrusion VALUES (NULL, ?)", (get_time(),))
  conn.commit()
  pir.wait_for_no_motion()
  print("No intruders")
