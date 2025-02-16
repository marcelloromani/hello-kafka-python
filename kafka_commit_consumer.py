import logging
from timeit import default_timer as timer

from confluent_kafka import Consumer, KafkaError


class KafkaCommitConsumer:
    """
    Subscribes to a topic and prints messages as strings.
    Disables auto-commit.
    Commits every received message.
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str, batch_size: int = 1):
        configuration['enable.auto.commit'] = False
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)
        self._close = False
        self._batch_size = batch_size
        self._max_commit_interval_ms = 100

    def print_assignment(self, consumer, partitions):
        self.logger.info('Assignment: %s', partitions)

    def run(self):
        processed_msgs: int = 0
        last_commit_time: float = timer()
        while not self._close:

            if 0 < processed_msgs < self._batch_size:
                time_since_last_commit_ms = (timer() - last_commit_time) * 1000
                if time_since_last_commit_ms >= self._max_commit_interval_ms:
                    self.logger.info("Commit after %d ms", time_since_last_commit_ms)
                    self._c.commit()
                    processed_msgs = 0
                    last_commit_time = timer()

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
            processed_msgs += 1
            if processed_msgs >= self._batch_size:
                self.logger.info("Commit after %d messages", processed_msgs)
                self._c.commit()
                processed_msgs = 0
                last_commit_time = timer()

        self.logger.info("Closing consumer")
        self._c.close()

    def close(self):
        self._close = True
