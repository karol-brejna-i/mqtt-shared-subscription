# Shared Subscriptions - MQTT 5

We need to use the MQTT 5 protocol to use shared subscriptions.
(https://www.hivemq.com/blog/mqtt5-essentials-part7-shared-subscriptions/). 


## How do Shared Subscriptions work?
    Shared subscriptions are an MQTT v5 feature that allows MQTT clients to share the same subscription on the broker. 
    In standard MQTT subscriptions, each subscribing client receives a copy of each message that is sent to that topic. 
    In a shared subscription, all clients that share the same subscription in the same subscription group receive messages 
    in an alternating fashion. This mechanism is sometimes called client load balancing, since the message 
    load of a single topic is distributed across all subscribers.

(source: https://www.hivemq.com/blog/mqtt5-essentials-part7-shared-subscriptions/)

Shared subscriptions use the following topic structure: $share/**GROUPID**/**TOPIC**

The shared subscription consists of 3 parts:

- A static shared subscription identifier ($share)
- A group identifier
- The actual topic subscriptions (may include wildcards)

A concrete example for such a subscriber would be:
`$share/my-shared-subscriber-group/myhome/groundfloor/+/temperature.`


## Experiment
Let's see if it works. We'll use [mosquitto_sub and mosquitto_pub in docker](mosquitto-in-docker.md) to test it.


Start multiple subscribers (in separate terminals or/and using tmux):
```bash
export TOPIC_NAME="test" 
export TOPIC_GROUP="g1"
docker run -it --net=host eclipse-mosquitto mosquitto_sub --protocol-version mqttv5 --id "consumer-$(uuidgen)" -q 1 -h localhost -t "\$share/$TOPIC_GROUP/$TOPIC_NAME"
```

And then publish some messages:
```bash
export TOPIC_NAME="test" 
docker run -it --net=host eclipse-mosquitto mosquitto_pub  --protocol-version mqttv5  -i pub1 -q 1 -h localhost -t $TOPIC_NAME -m "Hello World"
```

Publish multiple messages:
```bash
export TOPIC_NAME="test" 
for i in {1..100}; do docker run -it --net=host eclipse-mosquitto mosquitto_pub --protocol-version mqttv5 --id "publisher-$i" -h localhost -t $TOPIC_NAME -m "message $i"; done
```

You may try to put some of them [in parallel](publish.sh):
```bash
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
```