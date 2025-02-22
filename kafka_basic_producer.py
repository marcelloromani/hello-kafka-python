import logging
from typing import Optional

from confluent_kafka import Producer

from kafka_client import KafkaClient
from msg_processors import IMsgProcessor


class KafkaBasicProducer(KafkaClient):
    """
    Sends a string to a topic.
    Flushes after every send.
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str, msg_processor: Optional[IMsgProcessor]):
        super().__init__()
        self._p = Producer(configuration)
        self._topic_name = topic_name
        self._msg_processor = msg_processor
        self.logger.info("Topic: %s", topic_name)

    def send(self, msg: str):
        if self._msg_processor is not None:
            self._msg_processor.pre_send_hook(msg)

        self._p.produce(self._topic_name, msg)

        if self._msg_processor is not None:
            self._msg_processor.post_send_hook(msg)

        self._p.flush()
