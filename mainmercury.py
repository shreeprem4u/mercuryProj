from __future__ import print_function
from time import localtime, strftime
import mercury
import pika	#FOR RABBITMQ
import math
import time
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
	

'''
ESTABLISHING CONNECTION WITH RABBITMQ :
test,test - USERNAME AND PASSWORD OF RABBITMQ SERVER(172.17.137.155)(system:ACER2)
amuda,amuda2017 - USERNAME AND PASSWORD OF RABBITMQ SERVER(172.17.137.160)(system:Amuda5036)
IP ADDR - IP ADDR OF RABBITMQ SERVER
5672 - PORT NUMBER FOR ACCESSING RABBITMQ
amudavhost - VIRTUAL HOST NAME IN RABBITMQ
mercury - QUEUE NAME
'''
credentials = pika.PlainCredentials('test', 'test') #username,password for rabbitMq.
parameters = pika.ConnectionParameters('172.17.137.155',5672,'amudavhost',credentials)
#credentials = pika.PlainCredentials('amuda', 'amuda2017') #username,password for rabbitMq.
#parameters = pika.ConnectionParameters('172.17.137.160',5672,'amudavhost',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="mercury")

while('true'):
	dic = {}
	def display(data):
		print(data)


#FUNCTION DEFINITION
	def process(epc,ant,rssi):
		dist =math.pow(10,(-52-rssi)/22.0)	#n=1.8, -52 is RSSI at 1 metre distance from antenna at 90 degree
		timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #These four lines for getting IP address of the machine
		s.connect(("8.8.8.8", 80))
		ip = s.getsockname()[0]
		s.close()
#		dic[epc+","+ip] = ip+","+epc+","+timestamp	#It works perfectly.
		dic[epc] = ip+","+epc+","+timestamp

#READING OF TAGS
	reader.start_reading(lambda tag: process(tag.epc, tag.antenna, tag.rssi))
	time.sleep(1.0)	#need to increase or decrease the value depends on number of tags to read.
#	reader.stop_reading()
	count = len(dic)
	for key, value in dic.iteritems():
		msg = value
		parts = msg.split(",")
		viz = parts[1]+","+"695253.44712"+","+"190577.88868"+","+parts[2]+","+str(count) #epc,(x,y) of antenna,timestamp,number of tags in dictionary
		channel.basic_publish(exchange='', routing_key='mercury', body=viz)
		print("[x] Sent ")
		display(viz)
	reader.stop_reading()

