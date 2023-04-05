import RPi.GPIO as GPIO
import time

# database
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

# create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS intrusion (time text)''')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)  # Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)  # L

while True:
  i = GPIO.input(11)
  if i == 0:  # When output from motion sensor is LOW
    print "No intruders", i
    GPIO.output(3, 0)  # Turn OFF LED
    time.sleep(0.1)
  elif i == 1:  # When output from motion sensor is HIGH
    print "Intruder detected", i
    GPIO.output(3, 1)  # Turn ON LED
    time.sleep(0.1)
    # write intrusion time etc to database
    c.execute("INSERT INTO intrusion (time) VALUES (datetime('now'))")
