from __future__ import print_function
import time
import mercury
import pika	#FOR RABBITMQ
import math
from datetime import datetime
import socket	#TO GET IP ADDRESS OF THE MACHINE



'''
READER CONFIGURATION : 
ACM0 IS USB PORT VALUE
IN - REGION INDIA
1,2 - ANTENNA PORT NUMBER
GEN2 - PLAN NAME
'''
reader = mercury.Reader("tmr:///dev/ttyACM0")
#reader = mercury.Reader("tmr://172.17.137.155")
reader.set_region("IN")
reader.set_read_plan([1,2], "GEN2")
#print(reader.ip)	

'''
ESTABLISHING CONNECTION WITH RABBITMQ :
test,test - USERNAME AND PASSWORD OF RABBITMQ SERVER
IP ADDR - IP ADDR OF RABBITMQ SERVER
5672 - PORT NUMBER FOR ACCESSING RABBITMQ
amudavhost - VIRTUAL HOST NAME IN RABBITMQ
mercury - QUEUE NAME
'''
credentials = pika.PlainCredentials('test', 'test') #username,password for rabbitMq
parameters = pika.ConnectionParameters('172.17.137.155',5672,'amudavhost',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="mercury")


def display(data):
	print(data)



#FUNCTION DEFINITION
def send(epc,ant,rssi):
	dist =math.pow(10,(-52-rssi)/22.0)	#n=1.8, -52 is RSSI at 1 metre distance from antenna
	timestamp = str(datetime.now())
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #These four lines for getting IP address of the machine
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	msg = ip+","+epc+","+str(ant)+","+str(rssi)+","+str(dist)+","+timestamp
	channel.basic_publish(exchange='', routing_key='mercury', body=msg)
	print("[x] Sent ")
	display(msg)
	

#READING OF TAGS
reader.start_reading(lambda tag: send(tag.epc, tag.antenna, tag.rssi))
time.sleep(0.05)	#need to increase the value for more tags to read. This is for one tag
reader.stop_reading()
