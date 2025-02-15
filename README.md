# Launch kafka installed with homebrew on macOS

Run these commands in two different terminals:

```shell
$ /opt/homebrew/bin/zookeeper-server-start /opt/homebrew/etc/zookeeper/zoo.cfg
```

```shell
$ /opt/homebrew/bin/kafka-server-start /opt/homebrew/etc/kafka/server.properties 
```

# Python prerequisites

```shell
$ make venv
$ source .venv/bin/activate
$ make requirements
```

# Topic with 1 partition

## Create topic

```shell
$ /opt/homebrew/bin/kafka-topics --create --topic hello_kafka --bootstrap-server localhost:9092
```

## Describe topic

This is just to verify the metadata of the topic. It is not scritcly required.

```shell
$ /opt/homebrew/bin/kafka-topics --bootstrap-server localhost:9092 --topic hello_kafka --describe
```

## Single consumer

```shell
$ python main.py -c basic -t hello_kafka -g "group1"
```

### Send a message to the topic

```shell
$ python main.py -p basic -t hello_kafka -m "Hello, Kafka!"
```

### Result

The consumer receives and prints the message.

## Two consumers, same consumer group

In one terminal, run:
```shell
$ python main.py -c basic -t hello_kafka -g "group_1"
```

In another terminal, run:
```shell
$ python main.py -c basic -t hello_kafka -g "group_1"
```

### Send a message to the topic

```shell
$ python main.py -p basic -t hello_kafka -m "Hello, Kafka!"
```

### Result

Only one of the consumers will print the message.

## Two consumers, different consumer groups (fan-out == 2)

In one terminal, run:
```shell
$ python main.py -c basic -t hello_kafka -g "group_1"
```

In another terminal, run:
```shell
$ python main.py -c basic -t hello_kafka -g "group_2"
```

### Send a message to the topic

```shell
$ python main.py -p basic -t hello_kafka -m "Hello, Kafka!"
```

### Result

Both consumers get the message.

# Topic with 2 partitions

```shell
$ /opt/homebrew/bin/kafka-topics --bootstrap-server localhost:9092 --create --topic hello_kafka_2 --partitions 2
```

## Two consumers, same consumer group

In one terminal, run:
```shell
$ python main.py -c basic -t hello_kafka_2 -g "group_1"
```

In another terminal, run:
```shell
$ python main.py -c basic -t hello_kafka_2 -g "group_1"
```

### Send messages to the topic

Run this multiple times:

```shell
$ python main.py -p basic -t hello_kafka -m "Hello, Kafka!"
```

### Result:

Messages get to the different consumers in a round-robin-ish fashion.

### Improved visualisation of message distribution among clients

```shell
$ python main.py -p loop -t hello_kafka_2 --count 100000
```

# Kafka commands reference

## Create a topic

```shell
$ /opt/homebrew/bin/kafka-topics --bootstrap-server localhost:9092 --create --topic <topic_name> --partitions <num>
```

## Delete a topic

```shell
$ /opt/homebrew/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic <topic_name>
```
