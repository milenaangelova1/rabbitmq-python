import pika, sys, os, json

def worker_1(param):
    if param == True:
        print("Task 1 executed successfully.")
    else:
        print("Task 1 execution failed.")

    return param

def worker_2():
    print("Task 2 executed.")
    return True

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='queue_message')
    
    def callback(ch, method, properties, body):
        response = json.loads(body)
        task = response['task']
        if task == 'task_1':
            # add the param
            # message should be true
            message = worker_1(response['param'])
        elif task == 'task_2':
            # message should be false
            param = worker_2()
            response['param'] = param
    
        print(message)
    channel.basic_consume(queue='queue_message', on_message_callback=callback, auto_ack=True)
    
    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    