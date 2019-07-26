import os
import uuid

import imghdr
from flask import Flask, request

from producer import ImageProducer

app = Flask('rest_api')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', '/tmp')

image_producer = ImageProducer(
    host=os.environ.get('RABBITMQ_HOST', '127.0.0.1'),
    queue=os.environ.get('RABBITMQ_IMAGE_QUEUE', 'resize_images'),
    images_folder=app.config['UPLOAD_FOLDER']
)

VALID_IMAGE_FORMATS = ['png', 'jpeg', 'jpg', ]


@app.route('/images', methods=['POST'])
def images_endpoint():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['file']

    if imghdr.what(file) not in VALID_IMAGE_FORMATS:
        return {'error': 'Invalid image format'}, 415

    file_uuid = str(uuid.uuid4())
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_uuid))

    image_producer.send_message(file_uuid)

    return {'uuid': file_uuid}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = bool(os.environ.get('DEBUG', False))

    try:
        app.run('0.0.0.0', port=port, debug=debug)
    except Exception as exception:
        print(str(exception))
    finally:
        image_producer.close_connection()
