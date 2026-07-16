import os
from pathlib import Path


#Variables globales

app_root = None
movimientos = None
catalogo = None


def obtener_ruta_db():
    carpeta_local = Path(os.getenv("LOCALAPPDATA", "")) / "Presupuesto"

    candidatos = [
        carpeta_local / "presupuesto.db",
        carpeta_local / "Presupuesto.db",
    ]

    for candidato in candidatos:
        if candidato.exists():
            return str(candidato)

    return str(candidatos[0])
