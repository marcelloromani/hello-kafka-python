import logging

from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Message

from kafka_client import KafkaClient


class KafkaBasicConsumer(KafkaClient):
    """
    Subscribes to a topic and prints messages as strings.
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str):
        super().__init__()
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)

        self.logger.info("Topic %s", topic_name)

    def print_assignment(self, consumer, partitions):
        self.logger.info("Assignment: %s", partitions)

    def process_msg(self, msg: Message):
        payload = msg.value().decode('utf-8')
        self.logger.info("Received: %s", payload)

    def run(self):
        try:
            while not self.shutdown_requested():
                msg = self._c.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        self.logger.info(
                            "%s %s [%d] reached end at offset %d",
                            msg.topic(),
                            msg.partition(),
                            msg.offset()
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.process_msg(msg)
        finally:
            self.logger.info("Shutdown")
            self._c.close()
