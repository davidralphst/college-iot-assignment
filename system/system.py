from gpiozero import MotionSensor
from datetime import datetime
from cv2 import *

# databases
import sqlite3
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS intrusion (id INTEGER PRIMARY KEY AUTOINCREMENT, time text)''')
conn.commit()

# painful
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

pir = MotionSensor(17)
cam_port = 0
cam = VideoCapture(cam_port)

while True:
  pir.wait_for_motion()
  print("Intruder detected")
  # write intrusion time etc to database
  result, image = cam.read()
  imwrite("../photos/" + get_time() + ".jpg", image)
  c.execute("INSERT INTO intrusion VALUES (NULL, ?)", (get_time(),))
  conn.commit()
  pir.wait_for_no_motion()
  print("No intruders")
