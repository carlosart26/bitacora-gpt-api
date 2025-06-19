from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)
app = FastAPI()

class BitacoraEntrada(BaseModel):
    fecha: str
    que_paso: str
    lo_que_pense: str
    lo_que_aprendi: str
    potencial_para_post: str
    etiquetas: list[str] = []
    clasificaciones: list[str] = []

@app.post("/api/save-bitacora")
def guardar_bitacora(entrada: BitacoraEntrada):
    try:
        response = notion.pages.create(**{
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Fecha": {"date": {"start": entrada.fecha}},
                "Idea": {"title": [{"text": {"content": entrada.lo_que_aprendi}}]},
                "Contexto": {"rich_text": [{"text": {"content": f"Qué pasó: {entrada.que_paso}\nLo que pensé: {entrada.lo_que_pense}"}}]},
                "Potencial para post": {"rich_text": [{"text": {"content": entrada.potencial_para_post}}]},
                "Origen": {"rich_text": [{"text": {"content": "GPT"}}]},
                "Etiquetas": {"multi_select": [{"name": tag} for tag in entrada.etiquetas]},
                "Clasificación": {"multi_select": [{"name": clas} for clas in entrada.clasificaciones]},
                "ID de registro": {"rich_text": [{"text": {"content": datetime.now().isoformat()}}]},
            }
        })
        return {"status": "success", "message": "Entrada guardada en Notion"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
