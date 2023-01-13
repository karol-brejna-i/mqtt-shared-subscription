import logging
import os

from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
import uvicorn

from log_config import get_logger

logger = get_logger()

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
logger.info(f"MQTT_HOST: {MQTT_HOST}")
logger.info(f"MQTT_PORT: {MQTT_PORT}")

# MQTT config
mqtt_config = MQTTConfig(
    host=MQTT_HOST,
    port=MQTT_PORT
)

mqtt = FastMQTT(
    config=mqtt_config
)

app = FastAPI()
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("$share/group1/test")  # subscribing mqtt topic
    logger.info("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    logger.info(f"Received message ({os.getpid()}): {topic}, {payload.decode()}, {qos}, {properties}")


@mqtt.subscribe("dupa")
async def message_to_topic(client, topic, payload, qos, properties):
    logger.info("Received message to specific topic: ", topic, payload.decode(), qos, properties)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    logger.info("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    logger.info("subscribed", client, mid, qos, properties)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/publish")
async def func(message: str = "Test message."):
    logger.info(f"Publishing message ({os.getpid()}): {message}")
    mqtt.publish("test", message)  # publishing mqtt topic

    return {"result": True, "message": "Published"}


if __name__ == "__main__":
    logger.info("Starting server from main.py")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host='0.0.0.0', port=port)
