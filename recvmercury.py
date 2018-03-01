import pika

#ESTABLISHING CONNECTION WITH RABBITMQ
credentials = pika.PlainCredentials('test', 'test') #username,password for rabbitMq
parameters = pika.ConnectionParameters('172.17.137.155',5672,'amudavhost',credentials)
#credentials = pika.PlainCredentials('amuda', 'amuda2017') #username,password for rabbitMq
#parameters = pika.ConnectionParameters('172.17.137.160',5672,'amudavhost',credentials)
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
		print('AMuDA Lab')
	elif(parts[0]==cse):
		print('CSE department')
channel.basic_consume(recv,queue="mercury",no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
