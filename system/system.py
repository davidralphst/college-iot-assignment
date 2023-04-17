from gpiozero import MotionSensor
from datetime import datetime
import pygame.camera
import pygame.image


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
pygame.camera.init()
camlist = pygame.camera.list_cameras()
cam = pygame.camera.Camera(camlist[0], (640, 480))
cam.start()

while True:
  pir.wait_for_motion()
  print("Intruder detected")
  # write intrusion time etc to database
  c.execute("INSERT INTO intrusion VALUES (NULL, ?)", (get_time(),))
  image = cam.get_image()
  pygame.image.save(image, "../photos/" + get_time() + ".jpg")
  conn.commit()
  pir.wait_for_no_motion()
  print("No intruders")
