import imghdr
import logging
import os
import uuid

import pika
from PIL import Image

CACHE_IMAGES_FOLDER = os.environ.get('CACHE_IMAGES_FOLDER', '/tmp')
RESIZED_IMAGES_FOLDER = os.environ.get('RESIZED_IMAGES_FOLDER', '/tmp')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_IMAGE_QUEUE = os.environ.get('RABBITMQ_IMAGE_QUEUE', 'resize_images')

logger = logging.getLogger(__file__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
logger.info('Connected to RabbitMQ')

channel = rabbitmq_conn.channel()
channel.queue_declare(queue=RABBITMQ_IMAGE_QUEUE)


def write_image_file(image_bytes):
    file_name = str(uuid.uuid4())

    file_cache_path = os.path.join(CACHE_IMAGES_FOLDER, file_name)

    with open(file_cache_path, 'wb') as file:
        file.write(image_bytes)

    file_name_with_extension = file_name + '.' + imghdr.what(file_cache_path)
    os.rename(file_cache_path, os.path.join(CACHE_IMAGES_FOLDER, file_name_with_extension))

    return file_name_with_extension


def resize_image(image_file_name: str, height: int = 384, width: int = 384):
    size = (height, width)

    cached_image_path = os.path.join(CACHE_IMAGES_FOLDER, image_file_name)

    image = Image.open(cached_image_path)
    image = image.resize(size)

    resized_image_path = os.path.join(RESIZED_IMAGES_FOLDER, image_file_name)
    image.save(resized_image_path)

    return resized_image_path


def image_messages_consumer(channel, method, header, body):
    logger.info('Consuming image message...')

    image_file_name = write_image_file(body)
    resized_image_path = resize_image(image_file_name)

    logger.info('Resized image in ' + resized_image_path)


channel.basic_consume(queue=RABBITMQ_IMAGE_QUEUE, auto_ack=True, on_message_callback=image_messages_consumer)
logger.info('Starting to consume...')
channel.start_consuming()
