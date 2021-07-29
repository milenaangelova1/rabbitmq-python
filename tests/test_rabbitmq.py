import unittest, pika, json
from unittest.mock import MagicMock
from pika import BlockingConnection, ConnectionParameters
from src.subscriber import Subscriber
from src.message import Message

class RabbitMQ(unittest.TestCase):
    def setUp(self) -> None:
        self.__queue_name = "queue_name"
        self.__config = {'host':'localhost', 'exchange': ''}
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.__config['host']))
        self.__channel = self.__connection.channel()
        
    
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
    
    def test_that_consume_on_valid_message_are_consumed_from_the_queue(self):
        # publish a message
        self.__channel.basic_publish(
            exchange=self.__config['exchange'],
            routing_key=self.__queue_name,
            body=json.dumps(Message(1).get_message())
        )

        # see that the message is in the queue
        res = self.__channel.queue_declare(queue=self.__queue_name)
        self.assertEqual(res.method.message_count, 1)

        # accept any message
        message_callback = MagicMock(return_value=True)
        
        consumer = Subscriber(self.__config, self.__queue_name)
        # start consumer
        consumer.start()

        # assert that the queue is empty
        res = self.__channel.queue_declare(queue=self.__queue_name)
        self.assertEqual(res.method.message_count, 0)

        message_callback.assert_called_once()

        # stop the consumer
        consumer.join()
        
if __name__ == '__main__':
    unittest.main()
    