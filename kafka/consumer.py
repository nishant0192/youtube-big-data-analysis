from confluent_kafka import Consumer
import json
from storage.mongodb import store_comments

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'youtube_group',
    'auto.offset.reset': 'earliest'
}

def consume_from_kafka(topic):
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        record = json.loads(msg.value().decode('utf-8'))
        store_comments([record])
