# 🎨 Mock-ups del Dashboard

## Layout General

### Página 1: Dashboard Ejecutivo

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Dashboard de Predicción de Churn                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Navegación]  [EDA]  [Modelo]  [Scoring]  [Predicción]   │
│                                                             │
│  ┌─────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │Total    │Tasa      │Alto      │Medio     │Bajo      │  │
│  │10,500   │8.2%      │Riesgo    │Riesgo    │Riesgo    │  │
│  │         │          │1,680     │3,500     │5,320     │  │
│  └─────────┴──────────┴──────────┴──────────┴──────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Distribución de Riesgo                              │  │
│  │                                                       │  │
│  │   [Alto]  [Medio]  [Bajo]                           │  │
│  │    16%      33%      51%                             │  │
│  │   🔴        🟡       🟢                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Variables Más Importantes                           │  │
│  │                                                       │  │
│  │  ▓▓▓▓▓▓▓▓▓▓ Inactividad        (0.28)               │  │
│  │  ▓▓▓▓▓▓▓▓ Gasto Total         (0.24)               │  │
│  │  ▓▓▓▓▓▓▓ Tenure              (0.18)               │  │
│  │  ▓▓▓▓▓▓ Territorio           (0.15)               │  │
│  │  ▓▓▓▓▓ Coolers              (0.15)               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Página 2: Clientes en Riesgo

```
┌─────────────────────────────────────────────────────────────┐
│  🚨 Clientes en Riesgo                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Nivel: Todos ▼] [Territorio: Todos ▼] [Top: 20 ▼]      │
│                                                             │
│  ┌──────┬───────────┬──────────┬──────────────┐           │
│  │ ID   │Territorio │ Score    │ Nivel        │           │
│  ├──────┼───────────┼──────────┼──────────────┤           │
│  │45023 │ Norte     │ 0.89     │ 🔴 Alto      │           │
│  │34891 │ Sur       │ 0.87     │ 🔴 Alto      │           │
│  │52104 │ Este      │ 0.85     │ 🔴 Alto      │           │
│  │29847 │ Centro    │ 0.78     │ 🔴 Alto      │           │
│  │...   │ ...       │ ...      │ ...          │           │
│  └──────┴───────────┴──────────┴──────────────┘           │
│                                                             │
│  📊 Estadísticas:                                          │
│  Clientes mostrados: 20 | Score promedio: 0.82            │
│                                                             │
│  [📥 Descargar CSV]                                        │
└─────────────────────────────────────────────────────────────┘
```

### Página 3: Análisis por Territorio

```
┌─────────────────────────────────────────────────────────────┐
│  🗺️ Análisis por Territorio                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Seleccionar Territorio: Norte ▼]                        │
│                                                             │
│  ┌───────────────────┬────────────────────┐              │
│  │Tasa Churn Real    │Score Riesgo Promedio              │
│  │                   │                    │              │
│  │  Norte: 12.5%     │  Norte: 0.68       │              │
│  │  Sur:   8.3%      │  Sur:   0.52       │              │
│  │  Este:  15.2%     │  Este:  0.73       │              │
│  │  Centro: 6.1%     │  Centro: 0.45      │              │
│  │  Oeste: 11.8%     │  Oeste: 0.65       │              │
│  └───────────────────┴────────────────────┘              │
│                                                             │
│  Ranking de Territorios:                                  │
│  🥇 Centro (6.1%)  🥈 Sur (8.3%)  🥉 Oeste (11.8%)       │
└─────────────────────────────────────────────────────────────┘
```

### Página 4: Análisis de Coolers

```
┌─────────────────────────────────────────────────────────────┐
│  ❄️ Impacto de Coolers                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┬────────────────────────┐        │
│  │Con Coolers: 6.2%     │Sin Coolers: 9.8%       │        │
│  │Clientes: 3,200       │Clientes: 7,300         │        │
│  │                      │                        │        │
│  │✅ Coolers REDUCEN    │❌ Sin coolers tienen   │        │
│  │   churn 37%          │    mayor riesgo        │        │
│  └──────────────────────┴────────────────────────┘        │
│                                                             │
│  Impacto por Territorio:                                  │
│  ┌────────────────────────────────────────┐              │
│  │    Con Coolers    │    Sin Coolers     │              │
│  │ Norte:     7%     │ Norte:     18%     │              │
│  │ Sur:       5%     │ Sur:        9%     │              │
│  │ Este:      8%     │ Este:      21%     │              │
│  └────────────────────────────────────────┘              │
│                                                             │
│  💡 Recomendación: Promover coolers como estrategia      │
│     de retención                                          │
└─────────────────────────────────────────────────────────────┘
```

### Página 5: Predicción Individual

```
┌─────────────────────────────────────────────────────────────┐
│  👤 Predicción Individual                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Seleccionar Cliente: 45023 ▼]                           │
│                                                             │
│  Datos del Cliente:                                        │
│  ┌────────────────┬────────────────┬────────────────┐    │
│  │ ID: 45023      │ Territorio:    │ Coolers: 0     │    │
│  │                │ Norte          │ Meses: 14      │    │
│  └────────────────┴────────────────┴────────────────┘    │
│                                                             │
│  Predicción:                                              │
│  ┌────────────────────────────────────────────┐          │
│  │ Score: 89%  │  Nivel: 🔴 ALTO RIESGO      │          │
│  │ ████████░░░░░░░░░░░░░░░░ (89%)             │          │
│  └────────────────────────────────────────────┘          │
│                                                             │
│  Recomendaciones:                                         │
│  1. ✅ Contactar urgentemente al cliente                  │
│  2. ✅ Ofrecimiento de incentivos especiales             │
│  3. ✅ Asignación de ejecutivo dedicado                  │
│                                                             │
│  Información Detallada:                                   │
│  • Gasto Total: $12,500                                  │
│  • Gasto Promedio: $850/mes                              │
│  • Transacciones: 14                                     │
│  • Días sin compra: 45 ⚠️                                │
└─────────────────────────────────────────────────────────────┘
```

## Colores Estándar

- 🟢 **Bajo Riesgo**: #00cc00 / Verde
- 🟡 **Medio Riesgo**: #ffaa00 / Naranja
- 🔴 **Alto Riesgo**: #ff4444 / Rojo
- 📊 **Gráficos**: Escala degradada

## Elementos de Interacción

- **Selectores**: Filtrado de datos
- **Descarga**: Exportar a CSV
- **Zoom**: Gráficos interactivos
- **Hover**: Información detallada
