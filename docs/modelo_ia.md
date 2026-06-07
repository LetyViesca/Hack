# 🤖 Modelo de IA - Predicción de Churn

## Objetivo

Predecir la probabilidad de que un cliente abandone el servicio (churn) en el próximo período.

## Algoritmo

**Random Forest Classifier**

- Árboles: 100
- Profundidad máxima: 10
- Random state: 42
- Validación: 80/20 split

## Features Utilizadas

### Comportamiento

- **tenure_months**: Meses como cliente
- **total_spend**: Gasto total acumulado
- **avg_spend**: Gasto promedio mensual
- **num_transacciones**: Cantidad de compras
- **dias_sin_transaccion**: Días desde última compra

### Contexto

- **territorio**: Región geográfica
- **coolers_count**: Cantidad de coolers
- **tiene_coolers**: Flag binario de coolers

## Variables Más Importantes

1. **Dias sin transacción** (Inactividad)
2. **Gasto total** (Historial de compras)
3. **Tenure** (Lealtad)
4. **Territorio** (Ubicación)
5. **Coolers** (Producto complementario)

## Umbrales de Riesgo

| Rango | Clasificación | Acción |
|-------|---------------|--------|
| 0-30% | 🟢 Bajo | Monitoreo rutinario |
| 31-60% | 🟡 Medio | Seguimiento regular |
| 61-100% | 🔴 Alto | Contacto urgente |

## Métricas de Desempeño

- **Accuracy**: Precisión general
- **ROC-AUC**: Capacidad discriminatoria
- **Recall**: Detección de casos positivos

## Actualización del Modelo

Reentrenar cada trimestre con nuevos datos:
```python
from logic.train_model import entrenar_modelo, guardar_modelo
# Cargar nuevos datos
X, y, encoders = preparar_datos_entrenamiento(df)
modelo, X_train, X_test, y_train, y_test = entrenar_modelo(X, y)
guardar_modelo(modelo)
```

## Limitaciones

- Requiere datos históricos de al menos 6 meses
- Sesgo potencial por territorio
- No considera factores externos (economía, competencia)
- Necesita datos limpios y sin valores faltantes
