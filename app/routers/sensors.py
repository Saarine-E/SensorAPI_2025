from fastapi import APIRouter, status, Depends
from ..database.models import SensorIn, Sensor, SensorOutOne, ErrorHistory
from ..database.database import get_session
from sqlmodel import Session
from ..database import sensors_crud

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.get("/", response_model=list[Sensor])
def Get_All_Sensors(errorState: bool = None, session: Session = Depends(get_session)):
    return sensors_crud.Get_All_Sensors(session, errorState)

@router.post("/new", response_model=Sensor, status_code=status.HTTP_201_CREATED)
def Add_Sensor(sensorIn: SensorIn, session: Session = Depends(get_session)):
    return sensors_crud.Add_Sensor(session, sensorIn)

@router.get("/errors", response_model=list[ErrorHistory], status_code=status.HTTP_200_OK)
def Get_Error_History(session: Session = Depends(get_session)):
    return sensors_crud.Get_Error_History(session)

@router.get("/{sensorId}", response_model=SensorOutOne)
def Get_Sensor(sensorId: int, measurementCount: int = 10, startDateTime: str = None, endDateTime: str = None, session: Session = Depends(get_session)):
    return sensors_crud.Get_Sensor(session, sensorId, measurementCount, startDateTime, endDateTime)

@router.patch("/{sensorId}", response_model=ErrorHistory, status_code=status.HTTP_200_OK)
def Change_Sensor_Error_State(sensorId: int, newErrorState: bool = True, session: Session = Depends(get_session)):
    return sensors_crud.Change_Sensor_Error_State(session, sensorId, newErrorState)

@router.get("/{sensorId}/errors", response_model=list[ErrorHistory])
def Get_Sensor_Error_History(sensorId: int, session: Session = Depends(get_session)):
    return sensors_crud.Get_Sensor_Error_History(session, sensorId)