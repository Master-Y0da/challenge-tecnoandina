from config.config import Base
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, Enum
import datetime as dt

class Alerta(Base):
    __tablename__ = "alertas"

    id_alerta = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=None)
    value = Column(Float, default=None)
    version = Column(Integer, default=None)
    type = Column(Enum("BAJA", "MEDIA", "ALTA"), default=None)
    sended = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.now())
    updated_at = Column(DateTime, default=dt.datetime.now())

