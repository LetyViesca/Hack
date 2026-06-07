"""
Pipeline Completo: De Datos Crudos a Dashboard

Flujo:
1. Cargar datos CSV desde data/raw/
2. Construir tabla maestra
3. Ingeniería de features
4. Entrenar modelo
5. Generar scoring
6. Guardar para dashboard
"""

import sys
from pathlib import Path

# Asegurarse que el path está configurado
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic.utils import cargar_csv, guardar_tabla_maestra, cargar_tabla_maestra
from logic.feature_engineering import (
    crear_tabla_maestra,
    ingenieria_features,
    seleccionar_features_modelo
)
from logic.train_model import (
    preparar_datos_entrenamiento,
    entrenar_modelo,
    guardar_modelo,
    obtener_importancia_features
)
from logic.scoring import generar_scoring, contar_por_nivel_riesgo
from config import DATA_RAW_PATH, MASTER_TABLE_PATH, PROJECT_ROOT

import pandas as pd


def main():
    """Ejecuta el pipeline completo."""
    
    print("=" * 60)
    print("CHURN PREDICTION - PIPELINE COMPLETO")
    print("=" * 60)
    
    # PASO 1: Cargar datos crudos
    print("\n[1/6] Cargando datos crudos...")
    try:
        df_clientes = cargar_csv(str(DATA_RAW_PATH / "clientes.csv"))
        df_transacciones = cargar_csv(str(DATA_RAW_PATH / "transacciones.csv"))
        df_coolers = cargar_csv(str(DATA_RAW_PATH / "coolers.csv"))
        df_churn = cargar_csv(str(DATA_RAW_PATH / "churn.csv"))
        print(f"✓ Clientes: {len(df_clientes)} registros")
        print(f"✓ Transacciones: {len(df_transacciones)} registros")
        print(f"✓ Coolers: {len(df_coolers)} registros")
        print(f"✓ Churn: {len(df_churn)} registros")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("  Asegúrese de que los archivos CSV estén en data/raw/")
        return
    
    # PASO 2: Crear tabla maestra
    print("\n[2/6] Construyendo tabla maestra...")
    df_maestro = crear_tabla_maestra(df_clientes, df_transacciones, df_coolers, df_churn)
    print(f"✓ Tabla maestra: {len(df_maestro)} registros, {len(df_maestro.columns)} columnas")
    guardar_tabla_maestra(df_maestro)
    
    # PASO 3: Ingeniería de features
    print("\n[3/6] Aplicando ingeniería de features...")
    df_features = ingenieria_features(df_maestro)
    df_features = seleccionar_features_modelo(df_features)
    print(f"✓ Features generadas: {len(df_features.columns)} features")
    print(f"✓ Features: {list(df_features.columns)}")
    
    # PASO 4: Entrenar modelo
    print("\n[4/6] Entrenando modelo Random Forest...")
    X, y, encoders = preparar_datos_entrenamiento(df_features)
    modelo, X_train, X_test, y_train, y_test = entrenar_modelo(X, y)
    print(f"✓ Modelo entrenado")
    print(f"✓ Training set: {len(X_train)} muestras")
    print(f"✓ Test set: {len(X_test)} muestras")
    
    # PASO 5: Guardar modelo
    print("\n[5/6] Guardando modelo...")
    ruta_modelo = guardar_modelo(modelo)
    print(f"✓ Modelo guardado en: {ruta_modelo}")
    
    # Mostrar importancia de features
    print("\nImportancia de features (Top 5):")
    importancias = obtener_importancia_features(modelo, X.columns.tolist())
    for idx, row in importancias.head(5).iterrows():
        print(f"  • {row['feature']}: {row['importancia']:.4f}")
    
    # PASO 6: Generar scoring
    print("\n[6/6] Generando scoring...")
    scoring_df = generar_scoring(df_maestro, modelo, X.columns.tolist())
    conteos = contar_por_nivel_riesgo(scoring_df)
    
    print(f"✓ Scoring generado para {len(scoring_df)} clientes")
    print(f"  • Alto riesgo: {conteos['alto']} clientes ({conteos['alto']/len(scoring_df)*100:.1f}%)")
    print(f"  • Medio riesgo: {conteos['medio']} clientes ({conteos['medio']/len(scoring_df)*100:.1f}%)")
    print(f"  • Bajo riesgo: {conteos['bajo']} clientes ({conteos['bajo']/len(scoring_df)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✓ PIPELINE COMPLETADO")
    print("=" * 60)
    print("\nProximos pasos:")
    print("1. Ejecutar el dashboard: streamlit run dashboard/app.py")
    print("2. Revisar clientes en riesgo")
    print("3. Implementar estrategias de retención")
    print("\n")


if __name__ == "__main__":
    main()
