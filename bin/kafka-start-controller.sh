#!/usr/bin/env bash
set -u -o pipefail

echo "Reading kafka cluster id"
export KAFKA_CLUSTER_ID=$(cat kafka-storage/kafka_cluster_id.txt)

echo "Setting IPv4 as preferred network stack"
export KAFKA_OPTS="-Djava.net.preferIPv4Stack=True"

echo "Starting controller"
/opt/homebrew/bin/kafka-server-start kafka-config/controller.properties
