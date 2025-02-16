import logging
from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka import Message

from kafka_client import KafkaClient
from msg_processors import IMsgProcessor


class KafkaConsumer(KafkaClient):
    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str, msg_processor: Optional[IMsgProcessor]):
        super().__init__()

        self._msg_processor = msg_processor
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)

        self.logger.info("Topic: %s", topic_name)

    def print_assignment(self, consumer, partitions):
        self.logger.info("Assignment: %s", partitions)

    def process_msg(self, msg: Message):
        payload = msg.value().decode('utf-8')
        self.logger.info("Received: %s", payload)
        if self._msg_processor is not None:
            self._msg_processor.process(payload)
