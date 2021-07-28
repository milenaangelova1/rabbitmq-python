import pika, json, sys
from message import Message

class Publisher:
    """
    Sends message when data is available with particular routing key
    config ([dict]): contains information about host, port, exchange ...
    queue_name ([string]): name of the queue
    """
    def __init__(self, config, queue_name, key):
        self.__config = config
        self.__queue_name = queue_name
        self.__key = key
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
     
        param = self.__get_param()
        message = Message(param).get_message()
        message["task"] = message["task"].format(self.__key)
        channel.basic_publish(exchange='', routing_key=self.__queue_name, body=json.dumps(message))
        print("[X] Sent {}".format(message))
    
    def __get_param(self):
        if self.__key == 1:
            return True
        elif self.__key == 2:
            return False
        else:
            sys.exit()
    
    def __del__(self):
        """
        Close the connection
        """
        self.__connection.close()

class ConsoleArguments:
    def __init__(self):
        self.__queue_name, self.__key = self.__get_command_line_arguments()
        
    def __get_command_line_arguments():
        """
        Get command line arguments
        Returns:
            [tuple]: queue name and task number
        """
        if len(sys.argv) < 2:
            print('Wrong number of input arguments! We expect to have two input arguments.')
            sys.exit()
        else:
            return sys.argv[1], sys.argv[2]
        
    def get_arguments(self):
        """
        Get command line arguments
        Returns:
            [tuple]: queue_name and task number
        """
        return self.__queue_name, self.__key
        
   
if __name__ == '__main__':
    config = {'host': 'localhost', 'exchange': ''}
    queue_name, key = ConsoleArguments().get_arguments()
    publisher = Publisher(config, queue_name=queue_name, key=key)
    publisher.publish()
    