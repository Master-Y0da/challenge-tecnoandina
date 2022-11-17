from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from pydantic import constr
from config.config import influxdb_conn
from models.alerta import Alerta
from datetime import datetime
from utils.dependencies import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from validadores.alertas import AlertaSearch, AlertaType
import os


router = APIRouter()


@router.post("/process")
async def process_challenge(version: int, timeSearch: constr(regex=r"^[1-9]\d*[mhd]{1}$"), db: Session = Depends(get_db)):

    query_api = influxdb_conn.query_api()
    query = f'from(bucket:"{os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")}")|> range(start: -{timeSearch})|> filter(fn: (r) => r._measurement == "dispositivos") |> filter(fn: (r) => r.version == "{version}")|> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")'
    result = query_api.query(org=os.getenv("DOCKER_INFLUXDB_INIT_ORG"), query=query)
    
    if not result:
        return JSONResponse(status_code=422, content={"status": "No se pudo procesar los paramatros"})

    results = [record.values for table in result for record in table.records]

    estados ={"1": {"800": "ALTA", "500": "MEDIA","200": "BAJA"},"2": {"200": "ALTA", "500": "MEDIA", "800": "BAJA"}}

    registros = []
    gen = None
    tipo = ''

    for item in results:
        if item["version"] == '1':
            gen = (v for k, v in estados[item["version"]].items() if item["value"] > int(k))
        elif item["version"] == '2':
            gen = (v for k, v in estados[item["version"]].items() if item["value"] < int(k))

        try:
            tipo = next(gen)
        except StopIteration:
            pass

        registros.append(Alerta(datetime=datetime.fromtimestamp(item["timestamp"]), value=item["value"], 
            version=item["version"], type=tipo, sended=False, created_at=datetime.now(), updated_at=datetime.now()))

    try:
        db.bulk_save_objects(registros)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "Error al guardar los datos"})
    finally:
        db.commit()

    return JSONResponse(status_code=200, content={"status": "Ok"})


@router.post("/search", response_model=List[AlertaSearch], status_code=200)
def search_alerts(version: int, type: Optional[AlertaType] = None, sended: Optional[bool] = None, db: Session = Depends(get_db)):

    query = db.query(Alerta).filter(Alerta.version == version)

    if type:
        query = query.filter(Alerta.type == type)

    if sended:
        query = query.filter(Alerta.sended == sended)
    
    try:
        result = query.all()
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "Error al consultar los datos"})

    return result


@router.post("/send")
async def send_alerts(version: int, type: AlertaType, db: Session = Depends(get_db)):
    
    query = db.query(Alerta).filter(Alerta.version == version, Alerta.type == type, Alerta.sended == False)

    try:
        result = query.all()
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "Error al consultar los datos"})

    for item in result:
        item.sended = True
        item.updated_at = datetime.now()

    try:
        db.bulk_save_objects(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "Error al actualizar los datos"})
    finally:
        db.commit()

    return JSONResponse(status_code=200, content={"status": "Ok"})
   
