from fastapi import FastAPI, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.exc import IntegrityError
from typing import Optional
from seu_modulo_de_modelos import Sessao, Atleta

app = FastAPI()

# Adicionar query parameters nos endpoints
@app.get("/atletas/")
async def get_atletas(nome: Optional[str] = Query(None), cpf: Optional[str] = Query(None)):
    with Sessao() as sessao:
        query = sessao.query(Atleta)
        if nome:
            query = query.filter(Atleta.nome == nome)
        if cpf:
            query = query.filter(Atleta.cpf == cpf)
        return paginate(query)

# Customizar response de retorno de endpoints
@app.get("/atletas/all", response_model=Page[Atleta])
async def get_all_atletas():
    with Sessao() as sessao:
        query = sessao.query(Atleta).options(load_only("nome", "centro_treinamento", "categoria"))
        return paginate(query)

# Manipular exceção de integridade dos dados
@app.post("/atletas/")
async def create_atleta(atleta: AtletaCreate):
    with Sessao() as sessao:
        novo_atleta = Atleta(**atleta.dict())
        sessao.add(novo_atleta)
        try:
            sessao.commit()
            return novo_atleta
        except IntegrityError as e:
            sessao.rollback()
            raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

# Adicionar paginação
add_pagination(app)
