import logging
import signal
from typing import Optional

import click

import logging_setup
from kafka_basic_consumer import KafkaBasicConsumer
from kafka_basic_producer import KafkaBasicProducer
from kafka_commit_consumer import KafkaCommitConsumer
from kafka_loop_producer import KafkaLoopProducer
from msg_processors import PersistToTextFileMsgProcessor

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
@click.option("-b", "--batch-size", type=int, default=1,
              help="[Only valid with -c commit] Commit after processing these many message.")
@click.option("--output-file", help="[Only valid with -c commit] Save all messages to this file.")
@click.option("-g", "--consumer-group", help="Name of the consumer group to join.")
@click.option("-p", "--producer-type", type=click.Choice(['basic', 'loop']), help="Type of Kafka producer to run.")
@click.option("--count", type=int, help="[Only valid with -p loop] Number of messages to produce.")
@click.option("-t", "--topic-name", required=True, help="Name of the topic to consume.")
@click.option("-m", "--message", help="[Only valid with -p basic] Message to post to the topic.")
def main(consumer_type: str, consumer_group: str, producer_type: str, topic_name: str, message: str, count: int,
         batch_size: int, output_file: str):
    global _consumer_obj
    signal.signal(signal.SIGINT, signal_handler)

    logging_setup.configure("logging_config.json")

    logger = logging.getLogger()

    if consumer_type == 'basic':
        logger.info(
            f"Starting consumer of type {consumer_type} with topic {topic_name}, consumer group {consumer_group}")
        consumer_conf['group.id'] = consumer_group
        c = KafkaBasicConsumer(consumer_conf, topic_name)
        _consumer_obj = c
        c.run()

    elif consumer_type == 'commit':
        logger.info(
            f"Starting consumer of type {consumer_type} with topic {topic_name}, consumer group {consumer_group}")
        consumer_conf['group.id'] = consumer_group
        msg_proc = None
        if output_file is not None:
            logger.info("Persisting messages to file %s", output_file)
            msg_proc = PersistToTextFileMsgProcessor(output_file)
        c = KafkaCommitConsumer(consumer_conf, topic_name, batch_size, msg_proc)
        _consumer_obj = c
        c.run()

    elif producer_type == 'basic':
        logger.info(f"Starting producer of type {producer_type} with topic {topic_name}")
        p = KafkaBasicProducer(producer_conf, topic_name)
        p.send(message)

    elif producer_type == 'loop':
        logger.info(f"Starting producer of type {producer_type} with topic {topic_name} for {count} messages")
        p = KafkaLoopProducer(producer_conf, topic_name)
        p.send_messages(count)

    else:
        logger.error("No action specified. Please use --help for options.")


if __name__ == '__main__':
    main()
