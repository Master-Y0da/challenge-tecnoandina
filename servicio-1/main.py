import uvicorn
import datetime, random, json, time
from fastapi import FastAPI
from pydantic import BaseModel
from config.config import client

app = FastAPI()

@app.on_event("startup")
def startup_event():
    
    client.loop_start()
    
    while True:
        
        time.sleep(60)
        
        client.publish("challenge/dispositivo/rx", 
            json.dumps({
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "value": random.randrange(0, 1001),
                "version": random.choice([1, 2]) 
            }))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
 
