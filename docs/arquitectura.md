# 🏗️ Arquitectura del Sistema

## Visión General

El sistema está organizado en 4 capas principales:

```
┌─────────────────────────────────────┐
│    DASHBOARD (Streamlit)            │  ← Interfaz de usuario
├─────────────────────────────────────┤
│    MOTOR DE SCORING & PREDICCIÓN    │  ← Lógica de ML
├─────────────────────────────────────┤
│    MOTOR DE FEATURES                │  ← Transformación de datos
├─────────────────────────────────────┤
│    BASE DE DATOS (SQLite)           │  ← Persistencia
└─────────────────────────────────────┘
```

## Componentes

### 1. Base de Datos (database/)

**Schema SQLite** con tablas:
- `clientes`: Información demográfica
- `transacciones`: Historial de compras
- `productos_cliente`: Productos activos
- `coolers_cliente`: Cantidad de coolers
- `churn_historico`: Etiquetas de churn
- `predicciones`: Resultados de scoring

### 2. Datos (data/)

**raw/**: Archivos CSV originales sin procesar
**processed/**: Tabla maestra consolidada para ML

### 3. Lógica de ML (logic/)

- `feature_engineering.py`: Genera features
- `train_model.py`: Entrena Random Forest
- `scoring.py`: Calcula scores de riesgo
- `predict.py`: Predicciones individuales
- `utils.py`: Funciones auxiliares

### 4. Dashboard (dashboard/)

**app.py**: Página principal con KPIs
**pages/**: 5 páginas temáticas

## Flujo de Datos

```
CSV → Tabla Maestra → Feature Engineering → Modelo Entrenado → Scoring → Dashboard
```

## Tecnologías

- **Python 3.9+**
- **Streamlit**: Interfaz web
- **Scikit-Learn**: Modelado (Random Forest)
- **Pandas**: Procesamiento de datos
- **Plotly**: Visualizaciones
- **SQLite**: Base de datos
