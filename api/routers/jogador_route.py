from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db, Jogador

router = APIRouter(prefix="/jogadores", tags=["jogadores"])

@router.get("/")
def get_jogadores(db: Session = Depends(get_db)):
    jogadores = db.query(Jogador).all()
    return jogadores

@router.get("/jogador/{jogador_nome}")
def get_personagem_por_nome(jogador_nome: str, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter(Jogador.nome.ilike(f"%{jogador_nome}%")).first()

    if not jogador:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return jogador