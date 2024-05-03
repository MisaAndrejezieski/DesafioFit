from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi_pagination import add_pagination, paginate
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# Simulando uma base de dados em memória
db = {
    "atletas": []
}

class Atleta:
    def __init__(self, nome: str, cpf: str, centro_treinamento: str, categoria: str):
        self.nome = nome
        self.cpf = cpf
        self.centro_treinamento = centro_treinamento
        self.categoria = categoria

@app.get("/atletas")
def get_atletas(nome: Optional[str] = Query(None), cpf: Optional[str] = Query(None)):
    atletas_filtrados = [atleta for atleta in db["atletas"] if (nome is None or atleta.nome == nome) and (cpf is None or atleta.cpf == cpf)]
    return paginate(atletas_filtrados)

@app.post("/atletas")
def add_atleta(nome: str, cpf: str, centro_treinamento: str, categoria: str):
    novo_atleta = Atleta(nome, cpf, centro_treinamento, categoria)
    for atleta in db["atletas"]:
        if atleta.cpf == novo_atleta.cpf:
            raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {cpf}")
    db["atletas"].append(novo_atleta)
    return {"mensagem": "Atleta adicionado com sucesso"}

# Adicionando paginação
add_pagination(app)
