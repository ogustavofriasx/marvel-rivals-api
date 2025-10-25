from .database.db import Base, engine   
from .routers.personagem_route import router as personagens_router
from .routers.jogador_route import router as jogadores_router
from .routers.partida_route import router as partidas_router  
from .routers.ranking_route import router as ranking_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(personagens_router)
app.include_router(jogadores_router)
app.include_router(partidas_router)
app.include_router(ranking_router)

@app.get('/')
def root():
    return {"message": "Welcome to the Marvel Rivals API!"}