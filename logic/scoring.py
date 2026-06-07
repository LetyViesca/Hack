"""
Motor de scoring para generar predicciones de churn.
"""

import pandas as pd
import numpy as np
from config import RISK_THRESHOLDS


def calcular_score_riesgo(modelo, X: pd.DataFrame) -> np.ndarray:
    """
    Calcula el score de riesgo (probabilidad) para cada cliente.
    """
    probabilidades = modelo.predict_proba(X)[:, 1]
    return probabilidades


def clasificar_riesgo(score: float) -> str:
    """
    Clasifica el nivel de riesgo basado en el score.
    
    Bajo: 0% - 30%
    Medio: 31% - 60%
    Alto: 61% - 100%
    """
    if score <= RISK_THRESHOLDS['bajo'][1]:
        return 'Bajo'
    elif score <= RISK_THRESHOLDS['medio'][1]:
        return 'Medio'
    else:
        return 'Alto'


def generar_scoring(df: pd.DataFrame, modelo, feature_cols: list) -> pd.DataFrame:
    """
    Genera scoring para todos los clientes.
    """
    scoring = df[['customer_id', 'territorio']].copy()
    
    # Calcular scores
    X_scoring = df[feature_cols]
    scores = calcular_score_riesgo(modelo, X_scoring)
    
    scoring['score_riesgo'] = scores
    scoring['nivel_riesgo'] = scoring['score_riesgo'].apply(clasificar_riesgo)
    
    # Ordenar por score descendente
    scoring = scoring.sort_values('score_riesgo', ascending=False)
    
    return scoring


def contar_por_nivel_riesgo(scoring_df: pd.DataFrame) -> dict:
    """
    Cuenta clientes por nivel de riesgo.
    """
    conteos = scoring_df['nivel_riesgo'].value_counts().to_dict()
    return {
        'alto': conteos.get('Alto', 0),
        'medio': conteos.get('Medio', 0),
        'bajo': conteos.get('Bajo', 0)
    }


def obtener_clientes_alto_riesgo(scoring_df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Obtiene los N clientes con mayor riesgo.
    """
    return scoring_df.nlargest(top_n, 'score_riesgo')
