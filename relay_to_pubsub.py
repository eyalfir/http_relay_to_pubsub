import json
from google.cloud import pubsub_v1
from flask import Flask, request, Response
import sys
import os
import logging

app = Flask('relay_to_pubsub')
publisher = pubsub_v1.PublisherClient()
topic_path = os.environ['TOPIC_PATH']

def callback(f):
    try:
        f.result()
    except RuntimeError:
        app.logger.exception('error publishing')
        sys.exit(1)
    


@app.route('/dev', methods=['POST', 'GET'])
def hello():
    if request.json and 'challenge' in request.json:
        return Response(request.json['challenge'], mimetype="text/plain")
    if request.is_json:
        body = json.dumps(request.json)
    else:
        body = request.get_data(cache=False).decode('utf-8')
    pubsub_payload = {
            'body': body,
            'headers': dict(request.headers),
            'method': request.method
    }
    app.logger.debug(pubsub_payload)
    publisher.publish(topic_path, data=json.dumps(pubsub_payload).encode('utf-8'))
    return '', 200

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
