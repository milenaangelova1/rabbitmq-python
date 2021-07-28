import pika, json, sys
from message import Message

class Publisher:
    """
    Sends message when data is available with particular routing key
    config ([dict]): contains information about host, port, exchange ...
    queue_name ([string]): name of the queue
    """
    def __init__(self, config, queue_name):
        self.__config = config
        self.__queue_name = queue_name
        self.__connection = self.__create_connection()
    
    def __create_connection(self):
        """
        Create new connection
        """
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.__config['host']))
    
    def publish(self):
        """
        A method that will publish a message.
        """
        channel = self.__connection.channel()
        channel.queue_declare(queue=self.__queue_name)
        for n in range(1, 3):
            param = True
    
            if n == 2:
                param = False
                
            message = Message(param).get_message()
            message["task"] = message["task"].format(n)
            channel.basic_publish(exchange='', routing_key=self.__queue_name, body=json.dumps(message))
            print("[X] Sent {}".format(message))
            
    def __del__(self):
        """
            Close the connection
        """
        self.__connection.close()

def get_arguments():
    if len(sys.argv) < 2:
        print('Wrong number of input arguments! We expect to have two input arguments.')
        sys.exit()
    else:
        queueName = sys.argv[1]
        #key in the form exchange.*
        key = sys.argv[2]
    return queueName, key
   
if __name__ == '__main__':
    config = {'host': 'localhost', 'exchange': ''}
    publisher = Publisher(config, queue_name='queue_message')
    publisher.publish()
    