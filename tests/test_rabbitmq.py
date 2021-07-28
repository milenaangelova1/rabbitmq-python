from src.receive import main
import unittest
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

class RabbitMQ(unittest.TestCase):
    
    def test_rabbitmq(self):

        conn = BlockingConnection(ConnectionParameters(host='localhost'))
        channel = conn.channel()

        # define your consumer
        def on_message(channel, method_frame, header_frame, body):
            message = body.decode()
            # assert your message here
            # asset message == 'value'
            channel.basic_cancel('test-consumer')  # stops the consumer

        # define your publisher
        def publish_message(message):
            channel.basic_publish(exchange='', routing_key='', body=message)
        
        publish_message('some message')
    
    
        
if __name__ == '__main__':
    unittest.main()
    