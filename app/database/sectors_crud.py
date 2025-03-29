from fastapi import status, HTTPException
from sqlmodel import Session, select
from ..database.models import SectorIn, Sector

def Create_Sector(session: Session, sectorName: str):
    sector = Sector(name=sectorName)
    session.add(sector)
    session.commit()
    session.refresh(sector)
    return sector