import pytest

from hello_kafka_python.kafka_loop_producer import KafkaLoopProducer

@pytest.fixture(scope="function")
def fxt_kafka_loop_producer() -> KafkaLoopProducer:
    return KafkaLoopProducer({}, "foo", None)

class TestKafkaLoopProducer:

    def test_unique_id_should_not_contain_blanks(self, fxt_kafka_loop_producer):
        assert fxt_kafka_loop_producer._generate_obj_unique_id().find(" ") == -1

    def test_unique_id_should_be_non_empty(self, fxt_kafka_loop_producer):
        assert len(fxt_kafka_loop_producer._generate_obj_unique_id()) > 0
