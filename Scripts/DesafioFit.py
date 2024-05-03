from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi_pagination import add_pagination, paginate
from sqlalchemy.exc import IntegrityError
from pydantic import validator

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

    @validator("cpf")
    def validar_cpf(cls, cpf):
        # Implementar validação de formato de CPF com regex
        if not validar_cpf_regex(cpf):
            raise ValueError("CPF inválido")
        return cpf

@app.get("/atletas")
def get_atletas(nome: Optional[str] = Query(None), cpf: Optional[str] = Query(None)):
    atletas_filtrados = [atleta for atleta in db["atletas"] if (nome is None or atleta.nome == nome) and (cpf is None or atleta.cpf == cpf)]
    return paginate(atletas_filtrados)

@app.post("/atletas")
def add_atleta(nome: str, cpf: str, centro_treinamento: str, categoria: str):
    novo_atleta = Atleta(nome, cpf, centro_treinamento, categoria)

    try:
        # Verificar se atleta com mesmo CPF já existe
        if any(atleta.cpf == novo_atleta.cpf for atleta in db["atletas"]):
            raise HTTPException(status_code=400, detail=f"Já existe um atleta cadastrado com o CPF: {cpf}")

        db["atletas"].append(novo_atleta)
        return {"mensagem": "Atleta adicionado com sucesso"}
    except IntegrityError as e:
        # Tratar erro de integridade do banco de dados
        raise HTTPException(status_code=500, detail="Erro ao adicionar atleta")

add_pagination(app)
