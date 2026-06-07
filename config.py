import os
import sqlite3
from pathlib import Path

# Configuración del proyecto
PROJECT_ROOT = Path(__file__).parent

# Rutas
DB_PATH = PROJECT_ROOT / "database" / "churn.db"
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
MASTER_TABLE_PATH = DATA_PROCESSED_PATH / "tabla_maestra.csv"

# Crear directorios si no existen
DATA_RAW_PATH.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Parámetros del modelo
MODEL_PARAMS = {
    "random_state": 42,
    "test_size": 0.2,
    "n_estimators": 100,
    "max_depth": 10,
}

# Umbrales de riesgo
RISK_THRESHOLDS = {
    "bajo": (0.0, 0.30),
    "medio": (0.31, 0.60),
    "alto": (0.61, 1.0),
}
