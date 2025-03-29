from fastapi import APIRouter, status, Depends
from ..database.models import SensorIn, Sensor, SensorOutOne, ErrorHistoryOut, MeasurementIn, Measurement
from ..database.database import get_session
from sqlmodel import Session
from ..database import sensors_crud

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.get("/", response_model=list[Sensor])
def Get_All_Sensors(errorState: bool = None, session: Session = Depends(get_session)):
    return sensors_crud.Get_All_Sensors(session, errorState)

@router.get("/{sensorId}", response_model=SensorOutOne)
def Get_Sensor(sensorId: int, measurementCount: int = 10, startDateTime: str = None, endDateTime: str = None, session: Session = Depends(get_session)):
    return sensors_crud.Get_Sensor(session, sensorId, measurementCount, startDateTime, endDateTime)

@router.get("/{sensorId}/errorhistory", response_model=list[ErrorHistoryOut])
def Get_Sensor_Error_History(sensorId: int, session: Session = Depends(get_session)):
    pass

@router.post("/new", response_model=Sensor, status_code=status.HTTP_201_CREATED)
def Add_Sensor(sensorIn: SensorIn, session: Session = Depends(get_session)):
    return sensors_crud.Add_Sensor(session, sensorIn)

@router.post("/measurement", response_model=Measurement, status_code=status.HTTP_201_CREATED)
def New_Measurement(measurementIn: MeasurementIn, session:Session = Depends(get_session)):
    return sensors_crud.New_Measurement(session, measurementIn)