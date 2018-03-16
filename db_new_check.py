import psycopg2
import pika
import datetime



def dbInsert(tagid,x,y,timestamp):
	try:
		conn = psycopg2.connect("dbname='smartbuilding' port='5432' user='amudalab3' host='172.17.137.160' password='amudalab'")
		#the connection string	
		cur = conn.cursor()		
		cur.execute("INSERT INTO mercury_asset (epc,x,y,time) VALUES (%s,%s,%s,%s)",(tagid,x,y,timestamp))
		print("inserted row into mercury_asset table at ",datetime.datetime.now())
		conn.commit()
		cur.close()
	except:
		print("Connection Failed in attempt to mercury_asset")



def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	data = str(body).split(',')
	a = len(data)
	print(a)
	dbInsert(data[0],data[2],data[1],data[3]) #needed to insert count received from sender
	print(data[0],data[1],data[2],data[3])

credentials = pika.PlainCredentials('amuda', 'amuda2017')
parameters = pika.ConnectionParameters('172.17.137.160',5672,'amudavhost',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare("mercury")
channel.basic_consume(callback, "mercury",no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()






