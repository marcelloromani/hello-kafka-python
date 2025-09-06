#!/usr/bin/env bash
set -u -o pipefail

if [[ $# != 2 ]] ; then
  echo "$0 <topic-name> <partition-count>"
  exit 1
fi

TOPIC_NAME=$1
PARTITION_COUNT=$2

/opt/homebrew/bin/kafka-topics kafka-config/broker.properties --bootstrap-server localhost:9092 --topic "${TOPIC_NAME}" --create --partitions "${PARTITION_COUNT}"
