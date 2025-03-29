from fastapi import status, HTTPException
from sqlmodel import Session, select
from ..database.models import SensorIn, Sensor, Sector, MeasurementIn, Measurement
from ..database.sectors_crud import Create_Sector

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

def Get_Sensor(session: Session, sensorId: int, measurementCount: int = 10):
    pass

def Get_Sensor_Error_History(session: Session, sensorId: int):
    pass


def New_Measurement(session: Session, measurementIn: MeasurementIn):
    sensor = session.exec(select(Sensor).where(Sensor.sensorId == measurementIn.sensorId)).first()

    if sensor.hasError == True: # If the sensor is in an error state, refuse the measurement
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot send measurements to a sensor that's in an error state")
    
    measure = Measurement.model_validate(measurementIn)
    session.add(measure)
    session.commit()
    session.refresh(measure)
    return measure