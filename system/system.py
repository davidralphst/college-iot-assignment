from gpiozero import MotionSensor
from datetime import datetime
import subprocess
import requests

# databases
import sqlite3
conn = sqlite3.connect('../database.db')
c = conn.cursor()

# create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS intrusion (id INTEGER PRIMARY KEY AUTOINCREMENT, time text)''')
conn.commit()

# util functions
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def send_mail():
    return requests.post("https://api.mailgun.net/v3/aa/messages",
                         auth=("api", "key")
                         data={"from": "Security System <mailgun@aa>"
                               "to": ["collegeemail@gmail.com", "mailgun@aa"]
                               "subject": "New Intrusion"
                               "text": "Pain"})
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
  send_mail()   
  pir.wait_for_no_motion()
  print("No intruders")
