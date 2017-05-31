import mysql.connector

cnx = mysql.connector.connect(user="garvit@usrgeoloc", password='GHOSTman@1997', host="usrgeoloc.mysql.database.azure.com", port=3306, database='location')

cnx.close()
