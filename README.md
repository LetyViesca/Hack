# Churn Web Dashboard

Predicción de abandono de clientes con Machine Learning.

Una aplicación web interactiva que identifica clientes con riesgo de churn y permite analizar las variables influyentes, territorio y presencia de coolers.

## 🚀 Inicio rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el dashboard
streamlit run dashboard/app.py
```

## 📊 Características

- **Dashboard Ejecutivo**: KPIs generales y resumen de riesgos
- **Clientes en Riesgo**: Lista filtrable de clientes por nivel de riesgo
- **Análisis por Territorio**: Impacto del territorio en el churn
- **Impacto de Coolers**: Relación entre coolers y abandono
- **Predicción Individual**: Score de riesgo para un cliente específico

## 🏗️ Estructura

- `database/`: Esquema y base de datos SQLite
- `data/`: Datos crudos y tabla maestra procesada
- `logic/`: Motor de ML, feature engineering y scoring
- `dashboard/`: Interfaz web con Streamlit
- `docs/`: Documentación técnica

## 📈 Variables clave

El modelo predice churn considerando:
- Tenure (duración como cliente)
- Spend (gasto mensual)
- Productos activos
- Últimas transacciones
- Territorio
- Presencia de coolers

## 🎯 Clasificación de Riesgo

- **Bajo**: 0% - 30%
- **Medio**: 31% - 60%
- **Alto**: 61% - 100%
