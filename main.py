import os

from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from log_config import get_logger

import paho.mqtt.client as mqtt

logger = get_logger()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
logger.info(f"MQTT_HOST: {MQTT_HOST}")
logger.info(f"MQTT_PORT: {MQTT_PORT}")

MQTT_GROUP = os.getenv("MQTT_GROUP", "group1")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test")
SUBSCRIBE_TOPIC = f"$share/{MQTT_GROUP}/{MQTT_TOPIC}"
logger.info(f"MQTT_GROUP: {MQTT_GROUP}, MQTT_TOPIC: {MQTT_TOPIC}")
logger.info(f"SUBSCRIBE_TOPIC: {SUBSCRIBE_TOPIC}")


def on_connect(client, userdata, flags, rc, costam):
    logger.info("on_connect")
    logger.info("Connected with {client}, {userdata}, {flags}, {rc}, {costam}")
    # mqtt_client.subscribe(SUBSCRIBE_TOPIC)


def on_disconnect(client, userdata, flags, rc=0):
    logger.debug("DisConnected result code " + str(rc))
    client.loop_stop()


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


mqtt_client = mqtt.Client(protocol=mqtt.MQTTv5)
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_connect = on_connect
mqtt_client._on_message = on_message
mqtt_client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
# mqtt_client.connect_async()

logger.info("before loop start")
mqtt_client.loop_start()
logger.info("after loop start")
app = FastAPI()


def tick():
    logger.info("tick")
    # mqtt_client
    result = mqtt_client.publish(MQTT_TOPIC, "tick", qos=1)
    logger.info(f"publish result: {result}")
    # mqtt_client.single(topic, payload=None, qos=0, retain=False, hostname="localhost",
    #        port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    #        protocol=mqtt.MQTTv311, transport="tcp")


#     mqtt.publish(MQTT_TOPIC, 'tick')


@app.on_event('startup')
async def init_data():
    logger.info("Starting the scheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()


# @mqtt.on_connect()
# def connect(client, flags, rc, properties):
#     logger.info("Connected to MQTT Broker!")
#     mqtt.client.subscribe(SUBSCRIBE_TOPIC)  # subscribing mqtt topic
#     logger.info(f"Connected: {client}, {flags}, {rc}, {properties}")


# @mqtt.on_message()
# async def message(client, topic, payload, qos, properties):
#     logger.info(f"Received message ({os.getpid()}): {topic}, {payload.decode()}, {qos}, {properties}")


# @mqtt.subscribe("dupa")
# async def message_to_topic(client, topic, payload, qos, properties):
#     logger.info("Received message to specific topic: ", topic, payload.decode(), qos, properties)


# @mqtt.on_subscribe()
# def subscribe(client, mid, qos, properties):
#     logger.info(f"subscribed {client}, {mid}, {qos}, {properties}")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/publish")
# async def func(message: str = "Test message."):
#     logger.info(f"Publishing message ({os.getpid()}): {message}")
#     mqtt.publish(MQTT_TOPIC, message)

#     return {"result": True, "message": "Published"}


if __name__ == "__main__":
    logger.info("Starting server from main.py")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host='0.0.0.0', port=port)
