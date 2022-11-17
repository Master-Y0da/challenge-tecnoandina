from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AlertaSearch(BaseModel):
    version: int
    value: float
    datetime: datetime
    type: str
    sended: bool

    class Config:
        orm_mode = True


class AlertaType(str, Enum):
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    BAJA = "BAJA"
