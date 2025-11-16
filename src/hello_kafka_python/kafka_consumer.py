import json
import logging
from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka import Message

from hello_kafka_python.kafka_client import KafkaClient
from hello_kafka_python.msg_processors import IMsgProcessor


class KafkaConsumer(KafkaClient):
    logger = logging.getLogger()

    def __init__(self, configuration: dict, topic_name: str, msg_processor: Optional[IMsgProcessor]):
        super().__init__()

        self.logger.debug("Consumer configuration: %s", configuration)
        if configuration['group.id'] is None:
            raise ValueError('group.id cannot be None')

        self._msg_processor = msg_processor
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)

        self._msg_stats = {
            "received_count": 0,
            "decode_error_count": 0,
            "processed_count": 0,
            "process_error_count": 0,
            "msg_poll_cycle_time_s": 0,
        }

        self.logger.info("Topic: %s", topic_name)

    def get_msg_stats(self):
        success_msg_count = self._msg_stats["received_count"] - self._msg_stats["decode_error_count"] - self._msg_stats["process_error_count"]
        try:
            msg_per_sec = success_msg_count / self._msg_stats["msg_poll_cycle_time_s"]
        except ZeroDivisionError:
            msg_per_sec = 0
        self._msg_stats["msg_per_sec"] = msg_per_sec
        return self._msg_stats

    def print_assignment(self, consumer, partitions):
        self.logger.info("Assignment: %s", partitions)

    def process_msg(self, msg: Message):
        self._msg_stats["received_count"] += 1
        try:
            payload = msg.value().decode('utf-8')
            self.logger.info("Received: %s", payload)
        except Exception as e:
            self.logger.error("Cannot decode message: %s", e)
            self._msg_stats["decode_error_count"] += 1
            payload = None

        if payload is not None and self._msg_processor is not None:
            try:
                self._msg_processor.post_receive_hook(payload)
                self._msg_stats["processed_count"] += 1
            except Exception as e:
                self.logger.error("Cannot process message: %s", e)
                self._msg_stats["process_error_count"] += 0

    def _perform_shutdown(self):
        self.logger.info("Shutting down")
        self._c.close()
        print("Message stats:\n", json.dumps(self.get_msg_stats(), indent=4))
