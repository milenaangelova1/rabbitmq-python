from re import sub
import pika, sys, os, json

class Subscriber:
    """
    Listening for particular message using queues bound with specific keys
    config ([dict]): contains information about host, port, exchange ...
    queue_name ([string]): name of the queue
    """
    def __init__(self, config, queue_name):
        self.__config = config
        self.__queue_name = queue_name
        self.__connection = self.__create_connection()
    
    def __del__(self):
        """
        Close the connection
        """
        self.__connection.close()
        
    def __worker_1(self, param):
        """
        Worker which will print an appropriating message
        Args:
            param ([boolean]): message param

        Returns:
            [boolean]: message param
        """
        if param == True:
            print("Task 1 executed successfully.")
        else:
            print("Task 1 execution failed.")

        return param

    def __worker_2(self):
        """
        Worker which will print a message
      
        Returns:
            [boolean]: always True
        """
        print("Task 2 executed.")
        return True
    
    def __create_connection(self):
        """
        Create new connection
        """
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.__config['host']))

    def __callback(self, ch, method, properties, body):
        """
        Callback function
        Args:
            ch ([type]): channel
            method ([type]): method
            properties ([type]): properties
            body ([type]): body
        """
        response = json.loads(body)
        print(" [x] Received %r" % body.decode())
        task = response['task']
        if task == 'task_1':
            # if it is successful the message should be removed otherwise should be sent to the other worker
            body = "" if self.__worker_1(response['param']) else json.loads(body)
            print(body)
            
        elif task == 'task_2':
            self.__worker_2()
                
    def subscribe(self):
        """
        A method that will wait for a message
        """
        channel = self.__connection.channel()
        
        channel.queue_declare(queue=self.__queue_name)
        
        channel.basic_consume(queue=self.__queue_name, on_message_callback=self.__callback)
        
        print('[*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        
    
    
if __name__ == '__main__':
    try:
        config = {'host':'localhost', 'exchange': ''}
        subscriber = Subscriber(config, queue_name='queue_message')
        subscriber.subscribe()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    