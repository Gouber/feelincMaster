import json

from kafka import KafkaProducer

class Ingester:

    def __init__(self, _topic):
        self.producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'))
        self.topic = _topic


    def ingest(self, msg):
        #print(msg)
        self.producer.send(self.topic, msg)