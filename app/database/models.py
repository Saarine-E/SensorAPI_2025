from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import List


### Sensors
class SensorIn(SQLModel):
    sectorName: str = Field(foreign_key="sector.name")

class Sensor(SensorIn, table=True):
    sensorId: int = Field(default=None, primary_key=True)
    hasError: bool = Field(default=False, index=True)

    sensorSector: "Sector" = Relationship(back_populates="sectorSensors")
    sensorMeasurements: "Measurement" = Relationship(back_populates="measuringSensor")
    sensorErrorHistory: "ErrorHistory" = Relationship(back_populates="errorSensor")

class SensorOutOne(BaseModel):
    sensorId: int
    sectorId: int
    hasError: bool
    measurements: List["Measurement"]

class SensorOutBySector(BaseModel):
    sensorId: int
    hasError: bool
    latestMeasurement: "Measurement"

### Sectors
class SectorIn(SQLModel):
    pass

class Sector(SectorIn, table=True):
    sectorId: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True)

    sectorSensors: List["Sensor"] = Relationship(back_populates="sensorSector")

class SectorOut(BaseModel):
    name: str
    sensors: List["SensorOutBySector"]


### Measurements
class MeasurementIn(SQLModel):
    temperature: float = Field(default=None)
    sensorId: int = Field(foreign_key="sensor.sensorId")

class Measurement(MeasurementIn, table=True):
    measurementId: int = Field(default=None, primary_key=True)
    datetime: str = Field(default=None, index=True)

    measuringSensor: Sensor = Relationship(back_populates="sensorMeasurements")

### Other
class ErrorHistory(SQLModel, table=True):
    datetime: str = Field(default=None, primary_key=True)
    errorMode: bool = Field(index=True)
    sensorId: int = Field(foreign_key="sensor.sensorId")

    errorSensor: "Sensor" = Relationship(back_populates="sensorErrorHistory")

class ErrorHistoryOut(BaseModel):
    datetime: str
    errorMode: bool