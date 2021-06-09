from kafka import KafkaConsumer

cons = KafkaConsumer('tweets')

for msg in cons:
    print(msg)

