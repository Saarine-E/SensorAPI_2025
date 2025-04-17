from fastapi import APIRouter, status, Depends
from ..database.models import Sector, SectorOut
from ..database.database import get_session
from sqlmodel import Session
from ..database import sectors_crud

router = APIRouter(prefix="/sectors", tags=["Sectors"])

@router.get("/", response_model=list[Sector])
def Get_All_Sectors(session: Session = Depends(get_session)):
    return sectors_crud.Get_All_Sectors(session)

@router.get("/{sectorName}", response_model=SectorOut)
def Get_Sector(sectorName: str, session: Session = Depends(get_session)):
    return sectors_crud.Get_Sector(session, sectorName)

@router.post("/", response_model=Sector, status_code=status.HTTP_201_CREATED)
def Create_Sector(sectorName: str, session = Depends(get_session)):
    return sectors_crud.Create_Sector(session, sectorName)