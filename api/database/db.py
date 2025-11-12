from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()

Base.prepare(autoload_with=engine)

Personagem = Base.classes.personagem
Habilidade = Base.classes.habilidade
Ataque_basico = Base.classes.ataque_basico
Causa = Base.classes.causa
Dano = Base.classes.dano
HabColab = Base.classes.habilidade_colab
Jogador = Base.classes.jogador


#criei uma view para mostrar tudo sobre a partida
with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM vw_partidas_detalhes_json LIMIT 20"))
        dados = result.mappings().all()

with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM  vw_ranking_abates  LIMIT 20"))
        abates = result.mappings().all()

#total de vitórias por jogador e personagem    
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM vw_vitorias_jogador_personagem ORDER BY id_jogador;"))
    vitorias_jogadores_personagens = result.mappings().all()

#total de abates por personagem
with engine.connect() as conn:
     result = conn.execute(text("SELECT * from vw_total_abates_personagem ORDER BY id_personagem;"))
     abates_personagens = result.mappings().all()

#print(Base.classes.keys())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
