import psycopg2
import pika
import datetime



def dbInsert(c,d,e,f,g):
	try:
		conn = psycopg2.connect("dbname='smartbuilding' port='5432' user='amudalab3' host='127.0.0.1' password='amudalab'")
		#the connection string
		cur = conn.cursor()		
		cur.execute("INSERT INTO rawdata (epc,rssi,powerlevel,time,antennaid) VALUES (%s,%s,%s,%s,%s)",(c,d,e,f,g))
		#the query to insert into rawdata table
		print("inserted row into rawdata table at ",datetime.datetime.now())
		conn.commit()
		cur.close()
	except:
		print("Connection Failed in attempt to rawdata")

def dbInsert1(c,d,e,f):
	try:
		conn = psycopg2.connect("dbname='smartbuilding' port='5432' user='amudalab3' host='172.17.137.160' password='amudalab'")
		#the connection string	
		cur = conn.cursor()		
		cur.execute("INSERT INTO main_asset (epc,x,y,time,geom) VALUES (%s,%s,%s,%s,ST_SetSRID(ST_MakePoint(%s,%s),4326))",(c,d,e,f,d,e))
		#the query to insert into main_asset table
		print("inserted row into main_asset table at ",datetime.datetime.now())
		conn.commit()
		cur.close()
	except:
		print("Connection Failed in attempt to main_asset")



def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	data = str(body).split(',')
	a = len(data)
	print(a)
	#the raw data is stored in the table rawdata
	if a == 5 :
		dbInsert(data[0],data[2],data[4],data[3],data[1])
		print(data[0],data[2],data[4],data[3],data[1])
	#the location data is stored in the table main_asset
	if a == 4 :
		if data[2] != 'NaN':
			dbInsert1(data[0],data[2],data[1],data[3])
			print(data[0],data[1],data[2],data[3])

#code to consume the data from the rabbitmq server
#parameters = pika.ConnectionParameters('localhost') 
#instead of localhost the ip should to used to connect to the rabbitmq server running in the remote machine

credentials = pika.PlainCredentials('amuda', 'amuda2017')
# ip should to used to connect to the rabbitmq server running in the remote machine
parameters = pika.ConnectionParameters('172.17.137.160',5672,'amudavhost',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare("mercury")
channel.basic_consume(callback, "mercury",no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()






