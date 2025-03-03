import hashlib
import time
from typing import Optional

from kafka_basic_producer import KafkaBasicProducer
from msg_processors import IMsgProcessor


class KafkaLoopProducer(KafkaBasicProducer):
    """
    Sends a number of predefined strings with incrementing index to a topic.
    """

    def __init__(self, configuration: dict, topic_name: str, msg_processor: Optional[IMsgProcessor]):
        super().__init__(configuration, topic_name, msg_processor)
        self._generation = self._generate_obj_unique_id()
        self._close = False

    @staticmethod
    def _generate_obj_unique_id() -> str:
        return hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:8]

    def send_messages(self, msg_count: int):
        for i in range(msg_count):
            self.send(f"[gen: {self._generation}] Message {i}")
            if self.shutdown_requested():
                break
        self.logger.info("Shutdown")
