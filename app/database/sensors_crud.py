from fastapi import status, HTTPException
from sqlmodel import Session, select
from ..database.models import SensorIn, Sensor, SensorOutOne, Sector, Measurement, ErrorHistory
from ..database.sectors_crud import Create_Sector
from sqlalchemy import desc
from datetime import datetime

def Get_All_Sensors(session: Session, errorState: bool = None):
    query = select(Sensor) # Base query

    if errorState != None: # If errorstate query parameter is used, modify query to include it
        query = query.where(Sensor.hasError == errorState) 
    
    sensors = session.exec(query).all() # Run query

    if not sensors: # If none found, return 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [sensor.model_dump() for sensor in sensors]

def Add_Sensor(session: Session, sensorIn: SensorIn):

    # Look for named sector and create it if it doesnt exist
    sector = session.exec(select(Sector).where(Sector.name == sensorIn.sectorName)).first()
    if not sector:
        sector = Create_Sector(session, sensorIn.sectorName)

    sensor = Sensor.model_validate(sensorIn)
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

def Get_Sensor(session: Session, sensorId: int, measurementCount: int = 10, startDateTime: str = None, endDateTime: str = None):
    
    # Query the sensor
    query = select(Sensor).where(Sensor.sensorId == sensorId)
    sensor = session.exec(query).first()

    if not sensor: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")

    # Query the measurements
    msre_query = select(Measurement).where(Measurement.sensorId == sensorId).order_by(desc(Measurement.datetime))
    if startDateTime and endDateTime: # If start and end are given, add the expression to the query
        msre_query = msre_query.where(Measurement.datetime >= startDateTime, Measurement.datetime <= endDateTime)
    msre_query = msre_query.limit(measurementCount)
    measurements = session.exec(msre_query).all()

    # Compose response model
    return SensorOutOne(
        sensorId=sensor.sensorId,
        sectorId=sensor.sensorSector.sectorId,
        hasError=sensor.hasError,
        measurements=measurements
    )

def Get_Sensor_Error_History(session: Session, sensorId: int):
    query = select(ErrorHistory).where(ErrorHistory.sensorId == sensorId).order_by(desc(ErrorHistory.datetime))
    errors = session.exec(query).all()

    if not errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sensor or errors found")

    return errors

def Change_Sensor_Error_State(session: Session, sensorId: int, newErrorState: bool = True):
    
    # Query the sensor
    sensor = session.exec(select(Sensor).where(Sensor.sensorId == sensorId)).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    
    # Change error state to the given value
    sensor.hasError = newErrorState

    # Create new ErrorHistory object
    timestamp = datetime.now().isoformat()
    error = ErrorHistory(
        sensorId = sensorId,
        errorMode = newErrorState,
        datetime = timestamp,
        )

    # Commit the new ErrorHistory object and the change to the sensor
    session.add(error)
    session.commit()
    session.refresh(error)

    return error

def Get_Error_History(session: Session):
    errors = session.exec(select(ErrorHistory)).all()

    if not errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No error history found")

    # return errors
    return [e.model_dump() for e in errors]