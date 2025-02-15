from confluent_kafka import Consumer, KafkaError

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'basic_consumer',
    'auto.offset.reset': 'earliest'
}

def run_basic_consumer():

    c = Consumer(conf)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

    c.subscribe(['basic_topic'], on_assign=print_assignment)

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                print(msg.error())
                break

        print('Received message: {}'.format(msg.value().decode('utf-8')))

    c.close()
