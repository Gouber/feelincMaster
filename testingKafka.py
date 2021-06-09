from kafka import KafkaConsumer

def testingKafkaFunction():
    consumer = KafkaConsumer('quickstart-events',
                             auto_offset_reset = 'earliest',
                             )

    for msg in consumer:
        print(msg)