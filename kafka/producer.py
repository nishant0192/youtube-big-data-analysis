from confluent_kafka import Producer
import json

producer_config = {'bootstrap.servers': 'localhost:9092'}

def produce_to_kafka(topic, data):
    producer = Producer(producer_config)
    for record in data:
        producer.produce(topic, value=json.dumps(record))
        producer.flush()
