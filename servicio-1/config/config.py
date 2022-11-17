import paho.mqtt.client as mqtt
import os


# MQTT CONECCION

client = mqtt.Client()
client.connect(os.getenv("DOCKER_LOCALHOST_IP") , 1883, 60)


