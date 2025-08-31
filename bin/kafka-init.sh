#!/usr/bin/env bash
set -u -o pipefail

if [[ -d "kafka-storage" ]] ; then
  echo "Storage directory already exists."
  exit 1
fi

echo "Creating Kafka storage directories"
mkdir "kafka-storage"
mkdir "kafka-storage/broker1"
mkdir "kafka-storage/controller"

echo "Generating Kafka cluster id"
/opt/homebrew/bin/kafka-storage random-uuid > kafka-storage/kafka_cluster_id.txt
cat kafka-storage/kafka_cluster_id.txt

export KAFKA_CLUSTER_ID=$(cat kafka-storage/kafka_cluster_id.txt)

echo "Initializing broker storage"
/opt/homebrew/bin/kafka-storage format -t $KAFKA_CLUSTER_ID -c kafka-config/broker.properties

echo "Initializing controller storage"
/opt/homebrew/bin/kafka-storage format -t $KAFKA_CLUSTER_ID --standalone -c kafka-config/controller.properties
