import logging
from timeit import default_timer as timer
from typing import Optional

from confluent_kafka import KafkaError
from confluent_kafka import KafkaException

from hello_kafka_python.kafka_consumer import KafkaConsumer
from hello_kafka_python.msg_processors import IMsgProcessor


class KafkaBasicConsumer(KafkaConsumer):
    """
    Subscribes to a topic and prints messages as strings.
    """

    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str, msg_processor: Optional[IMsgProcessor]):
        super().__init__(configuration, topic_name, msg_processor)

    def run(self):
        try:
            while not self.shutdown_requested():
                poll_start = timer()

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

                    self._msg_stats["msg_poll_cycle_time_s"] += (timer() - poll_start)

        finally:
            self._perform_shutdown()
