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

class BitacoraEntradaExtendida(BaseModel):
    donde_ocurrio: str
    cuando_ocurrio: str
    con_quien: str
    que_paso: str
    detalle_significativo: str
    que_revelo: str
    que_aprendi: str
    pilar_de_marca: list[str]
    tipo_de_contenido: list[str]
    titulo_sugerido: str

@app.post("/api/save-bitacora-v2")
def guardar_bitacora_v2(entrada: BitacoraEntradaExtendida):
    try:
        response = notion.pages.create(**{
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Contexto breve": {
                    "rich_text": [{
                        "text": {
                            "content": f"Dónde: {entrada.donde_ocurrio}\nCuándo: {entrada.cuando_ocurrio}\nCon quién: {entrada.con_quien}"
                        }
                    }]
                },
                "Anécdota": {
                    "rich_text": [{
                        "text": {
                            "content": entrada.que_paso + "\n\n" + entrada.detalle_significativo
                        }
                    }]
                },
                "Reflexión o Insight": {
                    "rich_text": [{
                        "text": {
                            "content": entrada.que_revelo + "\n" + entrada.que_aprendi
                        }
                    }]
                },
                "Pilar de Marca": {
                    "multi_select": [{"name": pilar} for pilar in entrada.pilar_de_marca]
                },
                "Relación con tu mensaje": {
                    "rich_text": [{
                        "text": {
                            "content": entrada.que_revelo
                        }
                    }]
                },
                "Tipo de contenido": {
                    "multi_select": [{"name": tipo} for tipo in entrada.tipo_de_contenido]
                },
                "Título sugerido": {
                    "rich_text": [{
                        "text": {
                            "content": entrada.titulo_sugerido
                        }
                    }]
                },
                "Origen": {
                    "rich_text": [{
                        "text": {
                            "content": "GPT"
                        }
                    }]
                },
                "ID de registro": {
                    "rich_text": [{
                        "text": {
                            "content": datetime.now().isoformat()
                        }
                    }]
                }
            }
        })
        return {"status": "success", "message": "Entrada guardada en Notion"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
