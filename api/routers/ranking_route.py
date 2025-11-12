from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db, abates
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

router = APIRouter(prefix="/rank", tags=["rank"])

@router.get("/")
def rank():
    return {"message": "Página de ranking"}

@router.get("/statistics")
def get_rank_mais_abates():
    return abates

@router.get("/statistics/{personagem_nome}")
def get_rank_mais_abates_personagem(personagem_nome: str):

    query = text("""SELECT * FROM vw_top5_abates_por_personagem Where LOWER(nome_personagem) = LOWER(:personagem_nome) ORDER BY total_abates DESC LIMIT 5""")

    with engine.connect() as conn:
            result = conn.execute(query, {"personagem_nome": personagem_nome})
            dados = result.mappings().all()
    return dados