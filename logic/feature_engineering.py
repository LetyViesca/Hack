"""
Feature Engineering para el modelo de churn.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def crear_tabla_maestra(df_clientes: pd.DataFrame, 
                       df_transacciones: pd.DataFrame,
                       df_coolers: pd.DataFrame,
                       df_churn: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida múltiples tablas en una tabla maestra única.
    """
    # Iniciar con tabla de clientes
    master = df_clientes.copy()
    
    # Agregar estadísticas de transacciones
    trans_stats = df_transacciones.groupby('customer_id').agg({
        'monto': ['sum', 'mean', 'count'],
        'fecha_transaccion': 'max'
    }).reset_index()
    
    trans_stats.columns = ['customer_id', 'total_spend', 'avg_spend', 'num_transacciones', 'ultima_transaccion']
    master = master.merge(trans_stats, on='customer_id', how='left')
    
    # Agregar información de coolers
    coolers_agg = df_coolers.groupby('customer_id').agg({'cantidad': 'sum'}).reset_index()
    coolers_agg.columns = ['customer_id', 'coolers_count']
    master = master.merge(coolers_agg, on='customer_id', how='left')
    
    # Agregar información de churn
    master = master.merge(df_churn[['customer_id', 'churned']], on='customer_id', how='left')
    
    return master


def ingenieria_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera features para el modelo.
    """
    features = df.copy()
    
    # Convertir fechas si es necesario
    if 'fecha_registro' in features.columns:
        features['fecha_registro'] = pd.to_datetime(features['fecha_registro'])
    if 'ultima_transaccion' in features.columns:
        features['ultima_transaccion'] = pd.to_datetime(features['ultima_transaccion'])
    
    # Calcular tenure en meses
    if 'fecha_registro' in features.columns:
        features['tenure_months'] = (datetime.now() - features['fecha_registro']).dt.days / 30
    else:
        features['tenure_months'] = 0
    
    # Días desde última transacción
    if 'ultima_transaccion' in features.columns:
        features['dias_sin_transaccion'] = (datetime.now() - features['ultima_transaccion']).dt.days
    else:
        features['dias_sin_transaccion'] = 9999
    
    # Feature binaria: tiene coolers
    if 'coolers_count' in features.columns:
        features['tiene_coolers'] = (features['coolers_count'] > 0).astype(int)
    else:
        features['tiene_coolers'] = 0
    
    # Llenar NaN
    features['total_spend'] = features['total_spend'].fillna(0)
    features['avg_spend'] = features['avg_spend'].fillna(0)
    features['num_transacciones'] = features['num_transacciones'].fillna(0)
    features['coolers_count'] = features['coolers_count'].fillna(0)
    features['churned'] = features['churned'].fillna(0)
    
    return features


def seleccionar_features_modelo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Selecciona las features necesarias para el modelo.
    """
    features_necesarias = [
        'customer_id',
        'territorio',
        'tenure_months',
        'total_spend',
        'avg_spend',
        'num_transacciones',
        'dias_sin_transaccion',
        'coolers_count',
        'tiene_coolers',
        'churned'
    ]
    
    # Filtrar solo las que existen
    features_disponibles = [f for f in features_necesarias if f in df.columns]
    
    return df[features_disponibles]
