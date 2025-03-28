from fastapi import APIRouter, status, Depends
from ..database.models import Sector
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/sectors", tags=["Sectors"])

