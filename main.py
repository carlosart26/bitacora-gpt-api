from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BitacoraEntry(BaseModel):
    fecha: str
    donde_ocurrio: str
    cuando_ocurrio: str
    con_quien: str
    que_paso: str
    detalle_significativo: str
    reflexion: str
    aprendizaje: str
    pilar_estrategico: str
    tipo_de_contenido: str
    titulo_sugerido: str
    etiquetas: list[str]
    clasificaciones: list[str]

@app.post("/api/save-bitacora")
async def guardar_bitacora(entry: BitacoraEntry):
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": entry.titulo_sugerido
                        }
                    }
                ]
            },
            "Fecha": {"date": {"start": entry.fecha}},
            "¿Dónde ocurrió?": {"rich_text": [{"text": {"content": entry.donde_ocurrio}}]},
            "¿Cuándo ocurrió?": {"rich_text": [{"text": {"content": entry.cuando_ocurrio}}]},
            "¿Con quién ocurrió?": {"rich_text": [{"text": {"content": entry.con_quien}}]},
            "¿Qué pasó?": {"rich_text": [{"text": {"content": entry.que_paso}}]},
            "Detalle significativo": {"rich_text": [{"text": {"content": entry.detalle_significativo}}]},
            "Reflexión o Insight": {"rich_text": [{"text": {"content": entry.reflexion}}]},
            "Aprendizaje personal": {"rich_text": [{"text": {"content": entry.aprendizaje}}]},
            "Pilar estratégico": {"multi_select": [{"name": tag.strip()} for tag in entry.pilar_estrategico.split(",")]},
            "Tipo de contenido sugerido": {"multi_select": [{"name": tag.strip()} for tag in entry.tipo_de_contenido.split(",")]},
            "Etiquetas": {"multi_select": [{"name": tag} for tag in entry.etiquetas]},
            "Clasificaciones": {"multi_select": [{"name": tag} for tag in entry.clasificaciones]}
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 or response.status_code == 201:
        return {"status": "success", "message": "Entrada guardada en Notion"}
    else:
        return {"status": "error", "message": response.text}
