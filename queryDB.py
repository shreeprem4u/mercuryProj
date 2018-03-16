import psycopg2
from time import localtime, strftime
import datetime


def dbInsert1(c,d,e,f):
#	try:
		conn = psycopg2.connect("dbname='smartbuilding' port='5432' user='amudalab3' host='172.17.137.160' password='amudalab'")
		#the connection string	
		cur = conn.cursor()		
		cur.execute("INSERT INTO main_asset (epc,x,y,time,geom) VALUES (%s,%s,%s,%s,ST_SetSRID(ST_MakePoint(%s,%s),4326))",(c,d,e,f,d,e))
		print("inserted row into main_asset table at ",datetime.datetime.now())
		conn.commit()
		cur.close()
#	except:
#		print("Connection Failed in attempt to main_asset")



conn = psycopg2.connect("dbname='smartbuilding' port='5432' user='amudalab3' host='172.17.137.160' password='amudalab'")
cur = conn.cursor()		

cur.execute("SELECT DISTINCT ON (epc) epc,x,y,time FROM mercury_asset ORDER BY epc,time DESC;")
rows = cur.fetchall()
for row in rows:
	time = strftime("%Y-%m-%d %H:%M:%S", localtime())
	dbInsert1(row[0],row[1],row[2],time)
    	print(row)
conn.commit()
cur.close()

