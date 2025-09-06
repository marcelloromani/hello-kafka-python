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

# Topic with 1 partition

Create a topic with 1 partition
```shell
$ bin/kafka-create-topic.sh hello.world.1 1
```

## Consumers in the same group

Messages are distributed among consumers in the same consumer group.

* Spin up two consumers in the same consumer group
* Each consumer writes the received messages in a text file
* Each file doesn't receive all messages, but collectively they contain all sent messages.

Consumers 1 and 2 in group1
```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.1 -g "group1" -b 1000 -o consumer-1.txt
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.1 -g "group1" -b 1000 -o consumer-2.txt
```

Producer:
```shell
$ uv run src/hello_kafka_python/main.py -p loop -t hello.world.1 -m "one partition" --count 100000
```

Verify
```shell
$ cat consumer-1.txt consumer-2.txt | sort -k4 -n | wc -l
```

Result: `100000`

## Consumers in different groups

All consumer groups get all the messages.

* Spin up two consumer in different consumer groups
* Each consumer writes the received messages in a text file
* Each file contains all messages

Consumer 1 group1
```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.1 -g "group1" -b 1000 -o consumer-1-g1.txt
```

Consumer 1 group2
```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.1 -g "group2" -b 1000 -o consumer-1-g2.txt
```

Verify
```shell
$ cat consumer-1-g1.txt consumer-1-g2.txt| sort -k4 -n | wc -l
```

Result: `200000`

# Topic with 2 partitions

The number of partitions affects the data distribution within the Kafka cluster,
but the single group / multi group semantics are the same.

Create a topic with 2 partitions
```shell
$ bin/kafka-create-topic.sh hello.world.2 2
```

## Consumers in the same group

Consumers 1 and 2 in group1
```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.2 -g "group1" -b 1000 -o consumer-1.txt
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.2 -g "group1" -b 1000 -o consumer-2.txt
```

Producer:
```shell
$ uv run src/hello_kafka_python/main.py -p loop -t hello.world.2 -m "two partitions" --count 100000
```

Verify
```shell
$ cat consumer-1.txt consumer-2.txt | sort -k4 -n | wc -l
```

Result: `100000`

## Consumers in different groups

Consumer 1 group1
```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.2 -g "group1" -b 1000 -o consumer-1-g1.txt
```

Consumer 1 group2
```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.2 -g "group2" -b 1000 -o consumer-1-g2.txt
```

Verify
```shell
$ cat consumer-1-g1.txt consumer-1-g2.txt| sort -k4 -n | wc -l
```

Result: `200000`


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
