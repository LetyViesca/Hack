# 🗄️ Base de Datos - Especificación

## Esquema

### Tabla: clientes

```sql
CREATE TABLE clientes (
    customer_id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    territorio TEXT NOT NULL,
    fecha_registro DATE NOT NULL,
    estado TEXT DEFAULT 'activo'
);
```

**Descripción**: Información demográfica y de estado del cliente.

### Tabla: transacciones

```sql
CREATE TABLE transacciones (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    fecha_transaccion DATE NOT NULL,
    monto REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);
```

**Descripción**: Historial de compras de cada cliente.

### Tabla: productos_cliente

```sql
CREATE TABLE productos_cliente (
    product_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    fecha_activacion DATE NOT NULL,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);
```

**Descripción**: Productos activos por cliente.

### Tabla: coolers_cliente

```sql
CREATE TABLE coolers_cliente (
    cooler_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);
```

**Descripción**: Cantidad de coolers por cliente.

### Tabla: churn_historico

```sql
CREATE TABLE churn_historico (
    churn_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    fecha_churn DATE,
    churned INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);
```

**Descripción**: Etiqueta histórica de churn (0 = activo, 1 = inactivo).

### Tabla: predicciones

```sql
CREATE TABLE predicciones (
    prediction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    score_riesgo REAL NOT NULL,
    nivel_riesgo TEXT NOT NULL,
    fecha_prediccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);
```

**Descripción**: Registro de predicciones generadas por el modelo.

## Inicialización

```python
from logic.utils import init_database
init_database()
```

## Consultas Comunes

**Clientes activos por territorio:**
```sql
SELECT territorio, COUNT(*) FROM clientes WHERE estado = 'activo' GROUP BY territorio;
```

**Gasto total por cliente:**
```sql
SELECT c.customer_id, c.nombre, SUM(t.monto) as total_gasto
FROM clientes c
LEFT JOIN transacciones t ON c.customer_id = t.customer_id
GROUP BY c.customer_id;
```

**Clientes con alto riesgo:**
```sql
SELECT * FROM predicciones WHERE nivel_riesgo = 'Alto' ORDER BY score_riesgo DESC;
```
