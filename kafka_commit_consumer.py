from confluent_kafka import Consumer, KafkaError


class KafkaCommitConsumer:
    """
    Subscribes to a topic and prints messages as strings.
    Disables auto-commit.
    Commits every received message.
    """

    def __init__(self, configuration: dict, topic_name: str):
        configuration['enable.auto.commit'] = False
        self._c = Consumer(configuration)
        self._c.subscribe([topic_name], on_assign=self.print_assignment)
        self._close = False

    def print_assignment(self, consumer, partitions):
        print('Assignment:', partitions)

    def run(self):
        while not self._close:
            msg = self._c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break

            print('Received message: {}'.format(msg.value().decode('utf-8')))
            self._c.commit()

        print("Closing consumer")
        self._c.close()

    def close(self):
        self._close = True
