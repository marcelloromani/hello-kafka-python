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
* One consumer receives all the messages.

Consumers 1 and 2 in group1

```shell
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.1 -g "group1" -b 1000 -o consumer-1.txt
$ uv run src/hello_kafka_python/main.py -c commit -t hello.world.1 -g "group1" -b 1000 -o consumer-2.txt
```

Producer:

```shell
$ uv run src/hello_kafka_python/main.py -p loop -t hello.world.1 -m "one partition" --count 100000
```

Verify: one consumer gets all messages

```shell
$ wc -l consumer-1.txt
       0 consumer-1.txt
$ wc -l consumer-2.txt
  100000 consumer-2.txt
```

Verify: total messages

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

Verify: both consumers get a share of the messages

```shell
$ wc -l consumer-1.txt
   50084 consumer-1.txt
$ wc -l consumer-2.txt
   49916 consumer-2.txt
```

Verify: total messages

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
$ cat consumer-1-g1.txt consumer-1-g2.txt | sort -k4 -n | wc -l
```

Result: `200000`

# Scenario summary

* If consumers < partitions, consumers get messages from all partitions.
* If consumers == partitions, each consumer is assigned a partitions, therefore consumers get about the same share of
  messages (e.g. 3 partitions, 3 consumers, each gets ~1/3 of the message)
* If consumers > partitions, all partitions are allocated to a consumer, and the additional consumres remain idle (don't
  receive messages)
* Consumers in the same consumer groups collectively receive all messages

| Scenario                | Number of partitions | Number of consumers in the group | Consumer 1      | Consumer 2      | Consumer 3 |
|-------------------------|----------------------|----------------------------------|-----------------|-----------------|------------|
| consumers == partitions | 1                    | 1                                | all messages    | N/A             | N/A        |
| consumers > parittions  | 1                    | 2                                | all messages    | 0               | N/A        |
| consumers < partitions  | 2                    | 1                                | all messages    | N/A             | N/A        |
| consumers == partitions | 2                    | 2                                | about half msgs | about half msgs | N/A        |
| consumers > partitions  | 2                    | 3                                | about half msgs | about half msgs | 0          |

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
