from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db, dados


router = APIRouter(prefix="/partidas", tags=["partidas"])

@router.get("/")
def get_partidas(db: Session = Depends(get_db)):
   return dados