import signal
from typing import Optional

import click

from kafka_basic_consumer import KafkaBasicConsumer
from kafka_basic_producer import KafkaBasicProducer
from kafka_commit_consumer import KafkaCommitConsumer
from kafka_loop_producer import KafkaLoopProducer

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'REPLACE_ME',
    'auto.offset.reset': 'earliest',
}

_consumer_obj: Optional[KafkaBasicConsumer] = None


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    if _consumer_obj is not None:
        # Cleanly disconnect consumer instead of relying on timeouts
        _consumer_obj.close()


@click.command("kafka-consumer")
@click.option("-c", "--consumer-type", type=click.Choice(['basic', 'commit']),
              help="Type of Kafka consumer to run")
@click.option("-g", "--consumer-group", help="Name of the consumer group to join")
@click.option("-p", "--producer-type", type=click.Choice(['basic', 'loop']), help="Type of Kafka producer to run")
@click.option("-t", "--topic-name", required=True, help="Name of the topic to consume")
@click.option("-m", "--message", help="Message to post to the topic")
@click.option("--count", type=int, help="[Only valid with -p looper] Number of messages to produce.")
def main(consumer_type: str, consumer_group: str, producer_type: str, topic_name: str, message: str, count: int):
    global _consumer_obj
    signal.signal(signal.SIGINT, signal_handler)

    if consumer_type == 'basic':
        print(f"Starting consumer of type {consumer_type} with topic {topic_name}, consumer group {consumer_group}")
        consumer_conf['group.id'] = consumer_group
        c = KafkaBasicConsumer(consumer_conf, topic_name)
        _consumer_obj = c
        c.run()

    elif consumer_type == 'commit':
        print(f"Starting consumer of type {consumer_type} with topic {topic_name}, consumer group {consumer_group}")
        consumer_conf['group.id'] = consumer_group
        c = KafkaCommitConsumer(consumer_conf, topic_name)
        _consumer_obj = c
        c.run()

    elif producer_type == 'basic':
        print(f"Starting producer of type {producer_type} with topic {topic_name}")
        p = KafkaBasicProducer(producer_conf, topic_name)
        p.send(message)

    elif producer_type == 'loop':
        print(f"Starting producer of type {producer_type} with topic {topic_name} for {count} messages")
        p = KafkaLoopProducer(producer_conf, topic_name)
        p.send_messages(count)

    else:
        print("No action specified. Please use --help for options.")


if __name__ == '__main__':
    main()
