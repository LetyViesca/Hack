-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    customer_id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    territorio TEXT NOT NULL,
    fecha_registro DATE NOT NULL,
    estado TEXT DEFAULT 'activo'
);

-- Tabla de transacciones
CREATE TABLE IF NOT EXISTS transacciones (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    fecha_transaccion DATE NOT NULL,
    monto REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos_cliente (
    product_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    fecha_activacion DATE NOT NULL,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);

-- Tabla de coolers
CREATE TABLE IF NOT EXISTS coolers_cliente (
    cooler_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);

-- Tabla de churn (histórico)
CREATE TABLE IF NOT EXISTS churn_historico (
    churn_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    fecha_churn DATE,
    churned INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);

-- Tabla de predicciones
CREATE TABLE IF NOT EXISTS predicciones (
    prediction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    score_riesgo REAL NOT NULL,
    nivel_riesgo TEXT NOT NULL,
    fecha_prediccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);
