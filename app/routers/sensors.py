from fastapi import APIRouter, status, Depends
from ..database.models import SensorIn, SensorOut, SensorOutOne, Section, ErrorHistoryOut
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.get("/", response_model=list[SensorOut])
def get_all_sensors(errorState: bool = None, session: Session = Depends(get_session)):
    pass

@router.get("/{sensorId}", response_model=SensorOutOne)
def get_sensor(sensorId: int, measurementCount: int = 10, session: Session = Depends(get_session)):
    pass

@router.get("/{sensorId}/statehistory", response_model=list[ErrorHistoryOut])
def get_sensor_state_history(sensorId: int, session: Session = Depends(get_session)):
    pass