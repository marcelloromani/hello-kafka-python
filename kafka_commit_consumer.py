import logging
from timeit import default_timer as timer
from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Message

from kafka_client import KafkaClient
from msg_processors import IMsgProcessor


class KafkaCommitConsumer(KafkaClient):
    """
    Subscribes to a topic and prints messages as strings.
    Disables auto-commit.
    Commits every batch_size messages or every _max_commit_interval_ms (hardcoded to 5000ms).
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str, batch_size: int, msg_processor: Optional[IMsgProcessor]):
        super().__init__()
        configuration['enable.auto.commit'] = False
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)
        self._batch_size = batch_size
        self._max_commit_interval_ms = 5000
        self._msg_processor = msg_processor

        self.logger.info("Topic %s", topic_name)
        self.logger.info("enable.auto.commit: %s", configuration['enable.auto.commit'])
        self.logger.info("Batch size: %d", self._batch_size)
        self.logger.info("Max uncommitted: %d ms", self._max_commit_interval_ms)

    def print_assignment(self, consumer, partitions):
        self.logger.info('Assignment: %s', partitions)

    def process_msg(self, msg: Message):
        payload = msg.value().decode('utf-8')
        self.logger.info("Received: %s", payload)
        if self._msg_processor is not None:
            self._msg_processor.process(payload)

    def run(self):
        try:
            uncommitted_msgs: int = 0
            uncommitted_since: Optional[float] = None
            while not self.shutdown_requested():

                # Commit if we processed an entire batch of messages
                if uncommitted_msgs >= self._batch_size:
                    self.logger.info("Committing %d messages >= batch size %d", uncommitted_msgs, self._batch_size)
                    self._c.commit()
                    uncommitted_msgs = 0
                    uncommitted_since = None

                # Commit if we had uncommitted messages for more than max commit interval
                if uncommitted_since is not None:
                    uncommitted_age_ms = (timer() - uncommitted_since) * 1000
                    if uncommitted_age_ms >= self._max_commit_interval_ms:
                        self.logger.info("Committing %d messages after %d ms >= %d", uncommitted_msgs,
                                         uncommitted_age_ms,
                                         self._max_commit_interval_ms)
                        self._c.commit()
                        uncommitted_msgs = 0
                        uncommitted_since = None

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
                    uncommitted_msgs += 1
                    # Messages cannot stay uncommitted for more than max commit interval milliseconds
                    if uncommitted_since is None:
                        uncommitted_since = timer()
        finally:
            self.logger.info("Shutdown")
            self._c.close()
