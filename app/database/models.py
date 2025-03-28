from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import List


### Sensors
class SensorIn(SQLModel):
    sectionId: int = Field(index=True)

class SensorOut(SensorIn, table=True):
    sensorId: int = Field(default=None, primary_key=True)
    hasError: bool = Field(default=False, index=True)

    sensorSection: "Sector" = Relationship(back_populates="sectionSensors")
    sensorMeasurements: "Measurement" = Relationship(back_populates="measuringSensor")
    sensorErrorHistory: "ErrorHistory" = Relationship(back_populates="errorSensor")

class SensorOutOne(BaseModel):
    sensorId: int
    sectionId: int
    hasError: bool
    measurements: List["Measurement"]


### Sections
class Sector(SQLModel, table=True):
    sectionId: int = Field(default=None, primary_key=True)

    sectionSensors: List["SensorOut"] = Relationship(back_populates="sensorSection")


### Other
class Measurement(SQLModel, table=True):
    datetime: str = Field(default=None, primary_key=True)
    temperature: float = Field(default=None)

    measuringSensor: SensorOut = Relationship(back_populates="sensorMeasurements")

class ErrorHistory(SQLModel, table=True):
    datetime: str = Field(default=None, primary_key=True)
    errorMode: bool = Field(index=True)

    errorSensor: "SensorOut" = Relationship(back_populates="sensorErrorHistory")

class ErrorHistoryOut(BaseModel):
    datetime: str
    errorMode: bool