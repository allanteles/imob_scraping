from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS (opcional, útil para acessar via frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega os dados do JSON
with open("imoveis.json", "r", encoding="utf-8") as f:
    dados_imoveis = json.load(f)

@app.get("/")
def home():
    return {"message": "API de Imóveis funcionando"}

@app.get("/imoveis")
def listar_imoveis():
    return dados_imoveis

@app.get("/imoveis/{id}")
def buscar_por_id(id: str):
    for imovel in dados_imoveis:
        if imovel["id"] == id:
            return imovel
    return {"erro": "Imóvel não encontrado"}
