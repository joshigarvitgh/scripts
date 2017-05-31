import mysql.connector
import requests
import sched, time
import re


s = sched.scheduler(time.time, time.sleep)
def geolocation(sc):
    cnx = mysql.connector.connect(user="garvit@usrgeoloc", password='GHOSTman@1997', host="usrgeoloc.mysql.database.azure.com", port=3306, database='location')
    #Creating Cursor  
    cursor = cnx.cursor()
    f=open("user.txt","r")
    t=f.read()
    print(t)
    print ("Detecting Location...")
    freegeoip ="http://freegeoip.net/json"
    geo_req = requests.get(freegeoip)
    geo_json = geo_req.json()
    location= [geo_json["latitude"], geo_json["longitude"]]
    #SQL Query  
    SQLCommand = ("Update location set lat=%s,lon=%s  where id=%s")  
    #Processing Query 
    cursor.execute(SQLCommand,(location[0],location[1],t))   
    #Commiting any pending transaction to the database.  
    cnx.commit()
    #closing cursor
    cursor.close()
    #closing connection  
    cnx.close()  
    print("Data Successfully Saved")  
    s.enter(2, 1, geolocation, (sc,))

s.enter(2, 1, geolocation, (s,))
s.run()


