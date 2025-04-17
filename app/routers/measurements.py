from fastapi import APIRouter, status, Depends
from ..database.models import MeasurementIn, Measurement
from ..database.database import get_session
from sqlmodel import Session
from ..database import measurements_crud

router = APIRouter(prefix="/measurement", tags=["Measurements"])

@router.post("/", response_model=Measurement, status_code=status.HTTP_201_CREATED)
def New_Measurement(measurementIn: MeasurementIn, session:Session = Depends(get_session)):
    return measurements_crud.New_Measurement(session, measurementIn)