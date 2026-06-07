"""
Utilidades generales del proyecto.
"""

import pandas as pd
import sqlite3
from pathlib import Path
from config import DB_PATH


def init_database():
    """Inicializa la base de datos SQLite con el esquema."""
    schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
    with sqlite3.connect(DB_PATH) as conn:
        with open(schema_path) as f:
            conn.executescript(f.read())
    print(f"Base de datos inicializada: {DB_PATH}")


def cargar_csv(ruta_csv: str) -> pd.DataFrame:
    """Carga un archivo CSV."""
    return pd.read_csv(ruta_csv)


def guardar_tabla_maestra(df: pd.DataFrame, ruta: Path = None):
    """Guarda la tabla maestra en CSV."""
    if ruta is None:
        from config import MASTER_TABLE_PATH
        ruta = MASTER_TABLE_PATH
    df.to_csv(ruta, index=False)
    print(f"Tabla maestra guardada: {ruta}")


def cargar_tabla_maestra(ruta: Path = None) -> pd.DataFrame:
    """Carga la tabla maestra desde CSV."""
    if ruta is None:
        from config import MASTER_TABLE_PATH
        ruta = MASTER_TABLE_PATH
    if not ruta.exists():
        raise FileNotFoundError(f"Tabla maestra no encontrada: {ruta}")
    return pd.read_csv(ruta)
