from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from influxdb_client import InfluxDBClient
import os

#Coneccion a Mysql
DB_URL = f"mysql+mysqlconnector://admin:admin@{os.getenv('DOCKER_LOCALHOST_IP')}:3306/tecnoandina"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


#Coneccion a influxdb
influxdb_conn = InfluxDBClient(url=os.getenv("DOCKER_INFLUXDB_INIT_HOST") , token=os.getenv("DOCKER_INFLUXDB_INIT_TOKEN"))


