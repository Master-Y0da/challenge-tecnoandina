import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from routes import challenge
from config.config import SessionLocal, engine
from models import alerta

#instancia FastApi
app = FastAPI(name="Servicio-3", description="API para interactuar con influxdb y mysql")

#rutas
app.include_router(challenge.router, prefix="/challenge", tags=["challenge"])


@app.on_event("startup")
def startup_event():

    alerta.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
