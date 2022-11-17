import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from config.config import client, influxdb_client
import time, os, json
from influxdb_client.client.bucket_api import BucketsApi
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client as influxdb
from datetime import datetime, timezone

app = FastAPI()

def handle_message(client, userdata, message):

    msg = json.loads(message.payload)
    datestamp = datetime.fromisoformat(msg['time'])
    datestamp = datestamp.astimezone(timezone.utc)
    
    insert_msg ={
        "measurement": "dispositivos",
        "tags": { "version": int(msg["version"]) },
        "fields": { "value": int(msg["value"]), "timestamp": datestamp.timestamp() }
    }

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=os.getenv("DOCKER_INFLUXDB_INIT_BUCKET") , record=insert_msg, org=os.getenv("DOCKER_INFLUXDB_INIT_ORG"))


@app.on_event("startup")
def startup_event():
    
    client.loop_start()    
    client.message_callback_add("challenge/dispositivo/rx", handle_message)

    if not BucketsApi(influxdb_client).find_bucket_by_name('system'):
        BucketsApi(influxdb_client).create_bucket(bucket_name=os.getenv("DOCKER_INFLUXDB_INIT_BUCKET"), org=os.getenv("DOCKER_INFLUXDB_INIT_ORG"))

    client.subscribe("challenge/dispositivo/rx")
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
