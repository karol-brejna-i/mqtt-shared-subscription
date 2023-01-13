#!/usr/bin/env bash

TOPIC_NAME=${1:-topic}
MESSAGE_PREFIX=${2:-message}

echo "Usage: ./publish.sh <<topic name>> <<message prefix>>"
echo 
echo "Sending messages using TOPIC_NAME=$TOPIC_NAME; MESSAGE_PREFIX=$MESSAGE_PREFIX ..."
for i in {1..100}; do 
  docker run --net=host eclipse-mosquitto mosquitto_pub --protocol-version mqttv5 --id "publisher-$i" -h localhost -t $TOPIC_NAME -m "$MESSAGE_PREFIX $i" &
done
echo "Finished."
