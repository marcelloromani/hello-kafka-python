import logging

from confluent_kafka import Consumer, KafkaError


class KafkaBasicConsumer:
    """
    Subscribes to a topic and prints messages as strings.
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str):
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)
        self._close = False

    def print_assignment(self, consumer, partitions):
        self.logger.info('Assignment: %s', partitions)

    def run(self):
        while not self._close:
            msg = self._c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    self.logger.error(msg.error())
                    continue
                else:
                    print(msg.error())
                    break

            self.logger.info('Received: %s', msg.value().decode('utf-8'))

        self.logger.info("Closing consumer")
        self._c.close()

    def close(self):
        self._close = True
