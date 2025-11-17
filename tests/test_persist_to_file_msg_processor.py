from hello_kafka_python.msg_processors import PersistToTextFileMsgProcessor


def test_should_save_sent_msg(tmp_path):
    output_file = tmp_path / "messages.txt"
    with PersistToTextFileMsgProcessor(output_file) as obj:
        obj.post_send_hook("msg1")
    assert output_file.exists()
    assert output_file.read_text() == "msg1\n"


def test_should_save_received_msg(tmp_path):
    output_file = tmp_path / "messages.txt"
    with PersistToTextFileMsgProcessor(output_file) as obj:
        obj.post_receive_hook("msg1")
    assert output_file.exists()
    assert output_file.read_text() == "msg1\n"
