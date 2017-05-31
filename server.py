import math
import mysql.connector
import requests
import sched, time

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    
    return d
##############################################################################################################33    
s = sched.scheduler(time.time, time.sleep)
def loccalc(sc):
    cnx = mysql.connector.connect(user="garvit@usrgeoloc", password='GHOSTman@1997', host="usrgeoloc.mysql.database.azure.com", port=3306, database='location')
    #Creating Cursor  
    cursor = cnx.cursor()
    #SQL Query  
    query = ("SELECT id,lat,lon,latf,lonf,radf FROM location,fence ")
    
    #Processing Query 0
    cursor.execute(query)
   
    #Processing for multiple users
    for (id,lat,lon,latf,lonf,radf) in cursor:
        r=distance((float(latf),float(lonf)),(float(lat),float(lon)))
        if(r<(radf/4)):
            prox=1
        elif(r<(radf/2)):
            prox=2
        elif(r>radf):
            prox=3
        #set proximity query
        order=("Update status set proximity=%s  where id=%s")
        #execute the cursor
        cursor = cnx.cursor()
        cursor.execute(order,(prox,id))

    #Commiting any pending transaction to the database.  
    cnx.commit()
    #closing cursor
    cursor.close()
    #closing connection  
    cnx.close()  
    print("cycle successfully completed")  
    s.enter(2, 1, loccalc, (sc,))

s.enter(2, 1, loccalc, (s,))
s.run()