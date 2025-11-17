from hello_kafka_python.kafka_client import KafkaClient


def test_shutdown_requested_default():
    obj = KafkaClient()
    assert not obj.shutdown_requested()


def test_should_honour_shutdown_request():
    obj = KafkaClient()
    obj.shutdown()
    assert obj.shutdown_requested()
