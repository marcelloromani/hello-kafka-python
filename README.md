# Python Kafka playground

Trying Kafka in Python.

## Foreword

How to install Kafka varies among operating systems and is not the focus of this project.

Instructions and scripts for Mac OS are provided out of convenience.

## Install Kafka

At the time of writing (Aug 2025), Homebrew installs Kafka 4.0.0 in Kraft mode.

```shell
$ brew install kafka
```

Kafka scripts are installed in `/opt/homebrew/bin`:

```shell
% ls /opt/homebrew/bin/kafka-*
/opt/homebrew/bin/kafka-acls
/opt/homebrew/bin/kafka-broker-api-versions
/opt/homebrew/bin/kafka-client-metrics
[...]
```

## Initialize a Kafka cluster in the current directory

### Create the storage directories and cluster id

```shell
$ bin/kafka-init.sh
Creating Kafka storage directories
Generating Kafka cluster id
_gxeSOELQHuz7zqkTjeGwA
Initializing broker storage
Formatting metadata directory ./kafka-storage/broker with metadata.version 4.0-IV3.
Initializing controller storage
Formatting dynamic metadata voter directory ./kafka-storage/controller with metadata.version 4.0-IV3.
```

### Launch the controller

*Run this in a new terminal*

```shell
$ bin/kafka-start-controller.sh
Reading kafka cluster id
Setting IPv4 as preferred network stack
Starting controller
[2025-08-31 21:52:38,710] INFO Registered kafka:type=kafka.Log4jController MBean (kafka.utils.Log4jControllerRegistration$)
```

### Launch the broker

*Run this in a new terminal*

```shell
$ bin/kafka-start-broker.sh
Reading kafka cluster id
Setting IPv4 as preferred network stack
Starting broker
[2025-08-31 21:53:47,165] INFO Registered kafka:type=kafka.Log4jController MBean (kafka.utils.Log4jControllerRegistration$)
```

## Scenario 1: topic with 1 partition

### Create topic

```shell
$ /opt/homebrew/bin/kafka-topics kafka-config/broker.properties --bootstrap-server localhost:9092 --topic hello.world.1 --create --partitions 1
WARNING: Due to limitations in metric names, topics with a period ('.') or underscore ('_') could collide. To avoid issues it is best to use either, but not both.
Created topic hello.world.1.
```

Describe the topic just to verify its metadata.

```shell
$ /opt/homebrew/bin/kafka-topics kafka-config/broker.properties --bootstrap-server localhost:9092 --topic hello.world.1 --describe
Topic: hello.world.1	TopicId: O-388YCaQj-FhWHrtJRUuw	PartitionCount: 1	ReplicationFactor: 1	Configs:
	Topic: hello.world.1	Partition: 0	Leader: 1	Replicas: 1	Isr: 1	Elr: 	LastKnownElr:
```

### Single consumer

```shell
$ uv run src/hello_kafka_python/main.py -c basic -t hello.world.1 -g "group1"
```

#### Send a message to the topic

```shell
$ uv run src/hello_kafka_python/main.py -p basic -t hello.world.1 -m "Hello, Kafka"
```

### Two consumers, same consumer group

```shell
$ uv run src/hello_kafka_python/main.py -c basic -t hello.world.1 -g "group_1"
```

```shell
$ uv run src/hello_kafka_python/main.py -c basic -t hello.world.1 -g "group_1"
```

### Send a message to the topic

```shell
$ uv run src/hello_kafka_python/main.py -p basic -t hello.world.1 -m "Hello, Kafka"
```

## Two consumers, different consumer groups (fan-out == 2)

In one terminal, run:
```shell
$ uv run src/hello_kafka_python/main.py -c basic -t hello.world.1 -g "group_1"
```

In another terminal, run:
```shell
$ uv run src/hello.world_python/main.py -c basic -t hello.world.1 -g "group_2"
```

### Send a message to the topic

```shell
$ uv run src/hello_kafka_python/main.py -p basic -t hello.world.1 -m "Hello, Kafka"
```

## Topic with 2 partitions

```shell
$ /opt/homebrew/bin/kafka-topics kafka-config/broker.properties --bootstrap-server localhost:9092 --topic hello.world.2 --create --partitions 2
```

## Two consumers, same consumer group

In one terminal, run:
```shell
$ uv run src/hello_kafka_python/main.py -c basic -t hello.world.2 -g "group_1"
```

In another terminal, run:
```shell
$ uv run src/hello_kafka_python/main.py -c basic -t hello.world_2 -g "group_1"
```

### Send messages to the topic

Run this multiple times:

```shell
$ uv run src/hello_kafka_python/main.py -p basic -t hello.world.2 -m "Hello, Kafka"
```

### Batch send

```shell
$ uv run src/hello_kafka_python/main.py -p loop -t hello.world.2 --count 100000
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

## Describe a topic

```shell
$ /opt/homebrew/bin/kafka-topics --bootstrap-server localhost:9092 --describe --topic <topic_name>
```

 ## List topics

```shell
$ /opt/homebrew/bin/kafka-topics --bootstrap-server localhost:9092 --list
```
