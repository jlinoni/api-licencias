from pydantic import BaseModel
from datetime import date

class Conductor(BaseModel):
    nombres: str
    edad: int
    direccion: str

class Licencia(BaseModel):
    conductor_id: int
    tipo: str
    fecha_expedicion: date
    fecha_expiracion: date
    numero: str

class LicenciaUpdate(BaseModel):
    fecha_expiracion: date