import os

import pika


class ImageProducer(object):

    def __init__(self, host: str, queue: str, images_folder: str, username: str = 'guest', password: str = 'guest'):
        self._images_folder = images_folder

        self._credentials = pika.PlainCredentials(username, password)
        self._host = host
        self._queue = queue

        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(self._host, credentials=self._credentials))
            self._channel = self._connection.channel()
            self._channel.queue_declare(self._queue)

    def send_message(self, file_uuid: str):
        self._connect()

        print('Sending image ' + file_uuid + ' message...')

        with open(os.path.join(self._images_folder, file_uuid), 'rb') as file:
            image_bytes = file.read()

        self._channel.basic_publish(exchange='', routing_key=self._queue, body=image_bytes)
        print('Message with image ' + file_uuid + ' sent')

    def close_connection(self):
        self._connection.close()
