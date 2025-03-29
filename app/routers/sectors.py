from fastapi import APIRouter, status, Depends
from ..database.models import Sector, SectorOut
from ..database.database import get_session
from sqlmodel import Session
from ..database import sectors_crud

router = APIRouter(prefix="/sectors", tags=["Sectors"])

@router.get("/{sectorId}", response_model=SectorOut)
def Get_Sector(sectorId: int, session: Session = Depends(get_session)):
    pass

@router.post("/", response_model=Sector, status_code=status.HTTP_201_CREATED)
def Create_Sector(session = Depends(get_session)):
    sectors_crud.Create_Sector(session)

@router.delete("/", status_code=status.HTTP_200_OK)
def Delete_Sector(sectorId: int, session = Depends(get_session)):
    pass