# 📖 Manual de Usuario - Dashboard de Churn

## 1. Instalación y Ejecución

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Iniciar el Dashboard

```bash
streamlit run dashboard/app.py
```

El dashboard se abrirá en `http://localhost:8501`

## 2. Navegación

El dashboard tiene 6 secciones principales accesibles desde el menú:

### 📊 Dashboard Ejecutivo (Página Principal)

**Métricas visibles:**
- Total de clientes
- Tasa de churn general
- Clientes por nivel de riesgo (Alto, Medio, Bajo)
- Top 10 variables más importantes

**Uso:** Obtener resumen general y KPIs clave.

### 📈 Dashboard General

Replica de la página principal con focus en visualización.

**Uso:** Análisis profundo de métricas ejecutivas.

### 🚨 Clientes en Riesgo

**Funcionalidades:**
- Filtrar por nivel de riesgo (Todos, Alto, Medio, Bajo)
- Filtrar por territorio
- Ajustar cantidad de clientes a mostrar (10-100)
- Descargar resultados en CSV

**Columnas:**
- Customer ID
- Territorio
- Score Riesgo (probabilidad 0-1)
- Nivel Riesgo (Alto/Medio/Bajo)

**Uso:** Identificar clientes prioritarios para retención.

### 🗺️ Análisis por Territorio

**Visualizaciones:**
- Tasa de churn por territorio (gráfico de barras)
- Score de riesgo promedio por territorio
- Ranking completo de territorios
- Análisis detallado de territorio seleccionado

**Uso:** Identificar territorios con mayor problema.

### ❄️ Impacto de Coolers

**Comparativas:**
- Tasa de churn: Con vs Sin Coolers
- Distribución de clientes
- Análisis por territorio y coolers
- Insights clave sobre impacto

**Uso:** Evaluar efectividad del producto cooler.

### 👤 Predicción Individual

**Funcionalidades:**
- Seleccionar cliente por ID
- Ver datos demográficos
- Obtener score de riesgo individual
- Recibir recomendaciones personalizadas

**Uso:** Tomar decisiones sobre clientes específicos.

## 3. Interpretación de Resultados

### Score de Riesgo

- **0.00 - 0.30**: 🟢 BAJO - Cliente probable mantener
- **0.31 - 0.60**: 🟡 MEDIO - Necesita atención
- **0.61 - 1.00**: 🔴 ALTO - Riesgo inminente

### Acciones Recomendadas

**Riesgo Alto:**
- Contacto inmediato del ejecutivo
- Oferta de incentivos especiales
- Revisión de contrato
- Plan de retención personalizado

**Riesgo Medio:**
- Seguimiento mensual
- Ofertas periódicas
- Análisis de productos
- Mejora de servicio

**Riesgo Bajo:**
- Monitoreo estándar
- Comunicaciones regulares
- Upselling de productos

## 4. Exportación de Datos

### Descargar Reportes

Todos los listados incluyen botón **"📥 Descargar CSV"**

```bash
# Archivo se guarda como:
clientes_riesgo.csv
```

### Uso en Herramientas Externas

Los CSV pueden importarse en:
- Excel / Google Sheets
- CRM (Salesforce, HubSpot)
- Herramientas de BI (Power BI, Tableau)

## 5. Pasos Recomendados para una Sesión Tipo

1. **Inicio**: Revisar Dashboard Ejecutivo
2. **Análisis**: Ver territorios con mayor churn
3. **Identificación**: Listar clientes alto riesgo
4. **Acción**: Seleccionar cliente y obtener predicción
5. **Export**: Descargar lista para el equipo
6. **Seguimiento**: Implementar recomendaciones

## 6. Troubleshooting

### Error: "Tabla maestra no encontrada"

**Solución:**
- Colocar archivo CSV en `data/raw/`
- Ejecutar pipeline de procesamiento

### Error: "Modelo no encontrado"

**Solución:**
- Entrenar el modelo nuevamente
- Verificar que existe archivo en `models/modelo_churn.joblib`

### Dashboard lento

**Solución:**
- Reducir cantidad de datos mostrados
- Usar filtros para acotar búsquedas
- Aumentar memoria disponible

## 7. Contacto y Soporte

Para problemas técnicos:
- Revisar logs en terminal
- Verificar versiones de librerías
- Contactar al equipo de data engineering
