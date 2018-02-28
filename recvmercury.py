import pika
import json


#ESTABLISHING CONNECTION WITH RABBITMQ
credentials = pika.PlainCredentials('test', 'test') #username,password for rabbitMq
parameters = pika.ConnectionParameters('172.17.137.155',5672,'amudavhost',credentials)
credentials = pika.PlainCredentials('amuda', 'amuda2017') #username,password for rabbitMq
parameters = pika.ConnectionParameters('172.17.137.160',5672,'amudavhost',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare("mercury")





def display(data):
	print(data)


def recv(ch, method, properties, body):
	print(" [x] Received ")
	display(body)
	amuda = '172.17.137.155'
	cse = '172.17.137.160'
	parts = body.split(",")
#	print(parts[0])
	if(parts[0]==amuda):
		vis = parts[1]+","+"695253.44712"+","+"190577.88868"+","+parts[2]
		channel.basic_publish(exchange='', routing_key='mercury', body=vis)
		print('AMuDA Lab')
	elif(parts[0]==cse):
		vis = parts[1]+","+"756919.70624"+","+"212556.37591"+","+parts[2]
		channel.basic_publish(exchange='', routing_key='mercury', body=vis)
		print('CSE department')
channel.basic_consume(recv,queue="mercury",no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
