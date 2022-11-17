import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
import os

#Coneccion a mqtt

client = mqtt.Client()
client.connect(os.getenv("DOCKER_LOCALHOST_IP"), 1883, 60)


#Coneccion a influxdb
influxdb_client = InfluxDBClient(url=os.getenv("DOCKER_INFLUXDB_INIT_HOST") , token=os.getenv("DOCKER_INFLUXDB_INIT_TOKEN"))
