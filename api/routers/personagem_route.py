from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db, Personagem, Ataque_basico, Habilidade, Causa, Dano, HabColab

router = APIRouter(prefix="/personagens", tags=["personagens"])

@router.get("/")
def get_personagens(db: Session = Depends(get_db)):
    personagens = db.query(Personagem).all()
    return personagens


@router.get("/personagem/{personagem_nome}")
def get_personagem_por_nome(personagem_nome: str, db: Session = Depends(get_db)):
    caracteristicas = db.query(Personagem).filter(Personagem.nome.ilike(f"%{personagem_nome}%")).first()

    ataque = (
        db.query(Ataque_basico)
        .join(Personagem, Personagem.id_ataque_basico == Ataque_basico.id_ataque_basico)
        .filter(Personagem.nome.ilike(f"%{personagem_nome}%"))
        .first()
    )

    ataque_basico = {
    "nome": ataque.nome,
    "dano": ataque.dano,
    "velocidade_ataque": ataque.velocidade_ataque,
    "alcance": ataque.alcance,
    "qtd_municao": ataque.qtd_municao,
    "velocidade_recarga": ataque.velocidade_recarga,
}

    habilidades = (
        db.query(Habilidade, Causa, Dano)
        .outerjoin(Causa, Habilidade.id_habilidade == Causa.id_habilidade)
        .outerjoin(Dano, Causa.id_dano == Dano.id_dano)
        .filter(Habilidade.id_personagem == caracteristicas.id_personagem)
        .all()
    )

    habilidades_detalhadas = []
    for habilidade, causa, dano in habilidades:
        habilidades_detalhadas.append({
            "nome": habilidade.nome,
            "tipo": habilidade.tipo,
            "descricao": habilidade.descricao,
            "causa": {
                "id_causa": getattr(causa, "id_dano", None),
                "id_habilidade": getattr(causa, "id_habilidade", None),
            } if causa else None,
            "dano": {
                "id_dano": getattr(dano, "id_dano", None),
                "flat": getattr(dano, "flat", None),
                "porcent_vida_max": getattr(dano, "porcent_vida_max", None),
                "vida_atual": getattr(dano, "vida_atual", None),
            } if dano else None
        })

    
    habilidade_colab = (
        db.query(HabColab)
        .join(Personagem, HabColab.id_habilidade_colab == Personagem.id_habilidade_colab)
        .filter(Personagem.nome.ilike(f"%{personagem_nome}%"))
        .all()
    )

    personagem = {"Caracteristicas": caracteristicas, "Ataque Principal": ataque_basico, "Habilidades": habilidades_detalhadas, "Habilidades_Colaborativas": habilidade_colab}

    if not caracteristicas:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return personagem