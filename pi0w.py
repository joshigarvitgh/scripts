import mysql.connector
import requests
import sched, time
import time
import RPi.GPIO as gpio


gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
RED=11
yellow=16
GREEN=15
buzzer=7
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
gpio.setup(buzzer,gpio.OUT)

p = sched.scheduler(time.time, time.sleep)
def outp(sc):
    cnx = mysql.connector.connect(user="garvit@usrgeoloc", password='GHOSTman@1997', host="usrgeoloc.mysql.database.azure.com", port=3306, database='location')
    #Creating Cursor  
    cursor = cnx.cursor()
    f=open("user.txt","r")
    t=f.read()
    SQLCommand = ("select id,proximity from status where id=%s")  
    #Processing Query 
    cursor.execute(SQLCommand,(t))
    # Gpio Controll 
    if(proximity==1):
        gpio.output(green,0)
        time.sleep(.3)
        gpio.output(green,1)
        time.sleep(.3)
    if (proximity==2):
        gpio.output(yellow,0)
        time.sleep(.3)
        gpio.output(yellow,1)
        time.sleep(.3)
    elif (proximity==3):
        for i in range(0,3):
            gpio.output(red,0)
            gpio.output(buzzer,0)
            time.sleep(.3)
            gpio.output(buzzer,1)
            gpio.output(red,1)
            time.sleep(.3)
    #Commiting any pending transaction to the database.  
    cnx.commit()
    #closing cursor
    cursor.close()
    #closing connection  
    cnx.close()  
    print("Data Successfully Saved")  
    s.enter(2, 1, outp, (sc,))

P.enter(2, 1, outp, (s,))
p.run()

