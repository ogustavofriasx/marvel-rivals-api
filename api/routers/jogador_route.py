from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db, Jogador, vitorias_jogadores_personagens, estatisticas_jogadores

router = APIRouter(prefix="/jogadores", tags=["jogadores"])

@router.get("/")
def get_jogadores(db: Session = Depends(get_db)):
    jogadores = db.query(Jogador).all()
    return jogadores

@router.get("/jogador/{jogador_nome}")
def get_jogador_por_nome(jogador_nome: str, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter(Jogador.nome.ilike(f"%{jogador_nome}%")).first()

    if not jogador:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return jogador

@router.get("/vitorias/{jogador_nome}")
def get_vitorias_jogador_personagem(jogador_nome: str):
    resultado = [item for item in vitorias_jogadores_personagens if item['nome_jogador'].lower() == jogador_nome.lower()]
    if not resultado:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return resultado

@router.get("/estatisticas")
def get_estatisticas_jogador():
    return estatisticas_jogadores