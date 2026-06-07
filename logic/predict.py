"""
Motor de predicción para nuevos clientes o clientes individuales.
"""

import pandas as pd
from logic.train_model import cargar_modelo
from logic.scoring import calcular_score_riesgo, clasificar_riesgo


def predecir_cliente(df_cliente: pd.DataFrame, feature_cols: list):
    """
    Realiza predicción para un cliente específico.
    """
    try:
        modelo = cargar_modelo()
    except:
        raise Exception("Modelo no encontrado. Por favor, entrenar el modelo primero.")
    
    # Validar que el cliente tenga todas las features
    features_faltantes = [col for col in feature_cols if col not in df_cliente.columns]
    if features_faltantes:
        raise ValueError(f"Features faltantes: {features_faltantes}")
    
    # Preparar datos
    X = df_cliente[feature_cols]
    
    # Realizar predicción
    score = calcular_score_riesgo(modelo, X)[0]
    nivel = clasificar_riesgo(score)
    
    return {
        'score_riesgo': score,
        'nivel_riesgo': nivel,
        'probabilidad_churn': f"{score*100:.1f}%"
    }


def generar_reporte_prediccion(customer_id: int, df_cliente: pd.DataFrame, 
                              feature_cols: list, modelo_info: dict = None) -> dict:
    """
    Genera un reporte completo de predicción con explicación.
    """
    prediccion = predecir_cliente(df_cliente, feature_cols)
    
    reporte = {
        'customer_id': customer_id,
        'prediccion': prediccion,
        'factores': {},
        'recomendaciones': []
    }
    
    # Analizar factores de riesgo
    if prediccion['nivel_riesgo'] == 'Alto':
        reporte['recomendaciones'].append("Contactar urgentemente al cliente")
        reporte['recomendaciones'].append("Ofrecimiento de incentivos especiales")
        reporte['recomendaciones'].append("Asignación de ejecutivo dedicado")
    
    elif prediccion['nivel_riesgo'] == 'Medio':
        reporte['recomendaciones'].append("Monitoreo regular")
        reporte['recomendaciones'].append("Ofertas periódicas")
        reporte['recomendaciones'].append("Check-in trimestral")
    
    else:
        reporte['recomendaciones'].append("Continuar monitoreo rutinario")
    
    return reporte
                    
import pandas as pd

# 1. Supongamos que ya tienes tu modelo entrenado y tus predicciones guardadas en 'y_pred'
# Ejemplo: y_pred = modelo.predict(X_test)

# 2. Cargas el archivo de la imagen (el que está incompleto)
df_entrega = pd.read_csv('tu_archivo_incompleto.csv')  # o pd.read_excel si es un .xlsx

# 3. Rellenas la columna 'target' con tus predicciones mapeadas a 0 y 1
df_entrega['target'] = y_pred

# 4. Guardas el archivo final ya completado
df_entrega.to_csv('Entrega_Churn_Completa.csv', index=False)
print("¡Archivo completado y guardado con éxito!")
