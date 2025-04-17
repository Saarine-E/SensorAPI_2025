from fastapi import status, HTTPException
from sqlmodel import Session, select
from sqlalchemy import desc
from ..database.models import Sector, SectorOut, Sensor, SensorOutBySector, Measurement
from ..database.measurements_crud import Get_Latest_Measurement

def Get_All_Sectors(session: Session):
    sectors = session.exec(select(Sector)).all() # Run query

    if not sectors: # If none found, return 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [sector.model_dump() for sector in sectors]

def Get_Sector(session: Session, sectorName: str):
    sector = session.exec(select(Sector).where(Sector.name.collate("NOCASE").like(f"%{sectorName}%"))).first()

    if not sector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    sensors = session.exec(select(Sensor).where(Sensor.sectorName == sector.name)).all()

    sensorsOut = [
        SensorOutBySector(
        sensorId= s.sensorId,
        hasError= s.hasError,
        latestMeasurement= Get_Latest_Measurement(session, s.sensorId)
    ) for s in sensors]

    print(sensorsOut)

    return SectorOut(
        name=sector.name,
        sensors=sensorsOut
    )

def Create_Sector(session: Session, sectorName: str):
    sector = Sector(name=sectorName)
    session.add(sector)
    session.commit()
    session.refresh(sector)
    return sector