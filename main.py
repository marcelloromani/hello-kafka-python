import logging
import signal
from typing import Optional

import click

import logging_setup
from kafka_basic_consumer import KafkaBasicConsumer
from kafka_basic_producer import KafkaBasicProducer
from kafka_client import KafkaClient
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

_kafka_clients: list[KafkaClient] = []


def register_client(obj: KafkaClient):
    _kafka_clients.append(obj)


def signal_handler(sig, frame):
    logger = logging.getLogger()
    logger.info('You pressed Ctrl+C!')
    for obj in _kafka_clients:
        obj.shutdown()


@click.command("kafka-consumer")
@click.option("-c", "--consumer-type", type=click.Choice(['basic', 'commit']),
              help="Type of Kafka consumer to run")
@click.option("-b", "--batch-size", type=int, default=1,
              help="[Only valid with -c commit] Commit after processing these many message.")
@click.option("-o", "--output-file", help="[Only relevant to consumers] Save messages to file.")
@click.option("-g", "--consumer-group", help="Name of the consumer group to join.")
@click.option("-p", "--producer-type", type=click.Choice(['basic', 'loop']), help="Type of Kafka producer to run.")
@click.option("--count", type=int, help="[Only valid with -p loop] Number of messages to produce.")
@click.option("-t", "--topic-name", required=True, help="Name of the topic to consume.")
@click.option("-m", "--message", help="[Only valid with -p basic] Message to post to the topic.")
@click.option("-l", "--log-level", type=click.Choice(['DEBUG', 'INFO', 'WARN', 'ERROR']), help="Log level")
def main(consumer_type: str, consumer_group: str, producer_type: str, topic_name: str, message: str, count: int,
         batch_size: int, output_file: str, log_level: Optional[str]):
    signal.signal(signal.SIGINT, signal_handler)

    logging_setup.configure("logging_config.json")
    if log_level is not None:
        root_logger = logging.getLogger('root')
        root_logger.setLevel(log_level)

    logger = logging.getLogger()

    # saves messages to file
    message_processor = None
    if output_file is not None:
        message_processor = PersistToTextFileMsgProcessor(output_file)

    if consumer_type == 'basic':
        logger.info(f"Starting consumer type={consumer_type} topic={topic_name}, consumer_group={consumer_group}")
        consumer_conf['group.id'] = consumer_group
        c = KafkaBasicConsumer(consumer_conf, topic_name, message_processor)
        register_client(c)
        c.run()

    elif consumer_type == 'commit':
        logger.info(f"Starting consumer type={consumer_type} topic={topic_name}, consumer_group={consumer_group}")
        consumer_conf['group.id'] = consumer_group
        c = KafkaCommitConsumer(consumer_conf, topic_name, batch_size, message_processor)
        register_client(c)
        c.run()

    elif producer_type == 'basic':
        logger.info(f"Starting producer type={producer_type} topic={topic_name}")
        p = KafkaBasicProducer(producer_conf, topic_name)
        p.send(message)

    elif producer_type == 'loop':
        logger.info(f"Starting producer type={producer_type} topic={topic_name} msg_count={count}")
        p = KafkaLoopProducer(producer_conf, topic_name)
        register_client(p)
        p.send_messages(count)

    else:
        logger.error("No action specified. Please use --help for options.")


if __name__ == '__main__':
    main()
