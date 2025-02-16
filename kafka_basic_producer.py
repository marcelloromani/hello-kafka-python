import logging

from confluent_kafka import Producer

from kafka_client import KafkaClient


class KafkaBasicProducer(KafkaClient):
    """
    Sends a string to a topic.
    Flushes after every send.
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str):
        super().__init__()
        self._p = Producer(configuration)
        self._topic_name = topic_name
        self.logger.info("Topic: %s", topic_name)

    def send(self, msg: str):
        self._p.produce(self._topic_name, msg)
        self._p.flush()
