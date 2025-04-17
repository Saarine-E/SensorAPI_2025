from fastapi import status, HTTPException
from sqlmodel import Session, select
from ..database.models import Sensor, MeasurementIn, Measurement
from datetime import datetime
from sqlalchemy import desc

def New_Measurement(session: Session, measurementIn: MeasurementIn):
    sensor = session.exec(select(Sensor).where(Sensor.sensorId == measurementIn.sensorId)).first()

    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    if sensor.hasError == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot send measurements from a sensor that's in an error state")
    
    measure = Measurement.model_validate(measurementIn)
    measure.datetime = datetime.now().isoformat()
    
    session.add(measure)
    session.commit()
    session.refresh(measure)
    return measure

def Get_Latest_Measurement(session: Session, sensorId: int):
    query = select(Measurement).where(Measurement.sensorId == sensorId).order_by(desc(Measurement.datetime)).limit(1)
    measurement = session.exec(query).first()
    
    if not measurement:
        return Measurement(
            sensorId=sensorId
        ).model_dump()

    return measurement.model_dump()