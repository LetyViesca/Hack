"""
Entrenamiento del modelo Random Forest para predicción de churn.
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
from pathlib import Path
from config import MODEL_PARAMS


def preparar_datos_entrenamiento(df: pd.DataFrame):
    """
    Prepara los datos para entrenar el modelo.
    """
    # Separar features y target
    X = df.drop(columns=['customer_id', 'churned'])
    y = df['churned']
    
    # Codificar variables categóricas
    encoders = {}
    for col in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
    
    return X, y, encoders


def entrenar_modelo(X: pd.DataFrame, y: pd.Series):
    """
    Entrena el modelo Random Forest.
    """
    # División train-test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=MODEL_PARAMS['test_size'],
        random_state=MODEL_PARAMS['random_state'],
        stratify=y
    )
    
    # Entrenar modelo
    modelo = RandomForestClassifier(
        n_estimators=MODEL_PARAMS['n_estimators'],
        max_depth=MODEL_PARAMS['max_depth'],
        random_state=MODEL_PARAMS['random_state'],
        n_jobs=-1
    )
    
    modelo.fit(X_train, y_train)
    
    # Evaluar
    y_pred = modelo.predict(X_test)
    y_proba = modelo.predict_proba(X_test)[:, 1]
    
    print("\n=== Reporte de Clasificación ===")
    print(classification_report(y_test, y_pred))
    print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
    
    return modelo, X_train, X_test, y_train, y_test


def guardar_modelo(modelo, ruta: Path = None):
    """Guarda el modelo entrenado."""
    if ruta is None:
        from config import PROJECT_ROOT
        ruta = PROJECT_ROOT / "models" / "modelo_churn.joblib"
    
    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta)
    print(f"Modelo guardado: {ruta}")
    return ruta


def cargar_modelo(ruta: Path = None):
    """Carga el modelo entrenado."""
    if ruta is None:
        from config import PROJECT_ROOT
        ruta = PROJECT_ROOT / "models" / "modelo_churn.joblib"
    
    return joblib.load(ruta)


def obtener_importancia_features(modelo, nombres_features: list) -> pd.DataFrame:
    """
    Obtiene la importancia de las features.
    """
    importancias = modelo.feature_importances_
    df_importancias = pd.DataFrame({
        'feature': nombres_features,
        'importancia': importancias
    }).sort_values('importancia', ascending=False)
    
    return df_importancias
