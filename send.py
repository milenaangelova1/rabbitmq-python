import pika, json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(queue='queue_message')

for n in range(1, 3):
    param = True
   
    if n == 2:
        param = False
        
    message = { 
        "task": "task_{}",
        "param": param
    }
    message["task"] = message["task"].format(n)
    channel.basic_publish(exchange='', routing_key='queue_message', body=json.dumps(message))
    print("[X] Sent {}".format(message))
connection.close()