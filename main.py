import os

from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
import uvicorn

app = FastAPI()

# MQTT config
mqtt_config = MQTTConfig(
    host=os.getenv("MQTT_BROKER", "localhost"),
    port=int(os.getenv("MQTT_PORT", 1883))
)


mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("$share/group1/test")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print(f"Received message ({os.getpid()}): {topic}, {payload.decode()}, {qos}, {properties}")


@mqtt.subscribe("dupa")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/publish")
async def func(message: str = "Test message."):
    mqtt.publish("test", message)  # publishing mqtt topic

    return {"result": True, "message": "Published"}


if __name__ == "__main__":
    # read port number from environment variable
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host='0.0.0.0', port=port)
