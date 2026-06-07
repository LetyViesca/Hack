from __future__ import annotations

import numpy as np
import pandas as pd


def generate_demo_dataset(rows: int = 350) -> pd.DataFrame:
    """Genera un dataset de prototipo con variables de negocio y churn realista."""
    rng = np.random.default_rng(42)

    customer_ids = np.arange(1, rows + 1)
    territories = np.array(["Norte", "Centro", "Sur", "Oriente", "Occidente"])
    channels = np.array(["Directo", "Canal Partner", "Retail", "Digital"])
    sizes = np.array(["Enterprise", "SMB", "Mid-Market"])

    data = []
    for customer_id in customer_ids:
        territory = territories[rng.integers(0, len(territories))]
        channel = channels[rng.integers(0, len(channels))]
        size = sizes[rng.integers(0, len(sizes))]

        total_sales = rng.lognormal(mean=10.0, sigma=0.7) * (80 + rng.integers(0, 120))
        num_orders = int(rng.normal(6, 2.5))
        num_orders = max(1, num_orders)
        avg_sales = total_sales / num_orders
        purchase_frequency = max(0.2, min(12.0, num_orders / (1 + rng.integers(0, 8))))
        active_months = int(rng.normal(18, 6))
        active_months = max(1, active_months)
        days_since_purchase = int(rng.gamma(shape=2.2, scale=12))
        num_transactions = max(1, int(num_orders + rng.integers(0, 4)))
        num_coolers = int(rng.poisson(1.2))
        num_doors = int(rng.normal(4.8, 2.0))
        num_skus = int(rng.normal(8, 3))
        substitutions = int(rng.poisson(0.8))
        sales_trend = rng.normal(0.0, 1.0)
        monthly_variation = rng.normal(0.0, 10.0)
        recency = max(0, min(365, int(days_since_purchase + rng.integers(-30, 30))))

        # Señal explícita de churn en función de variables del negocio.
        churn_signal = (
            total_sales < 1200
            or purchase_frequency < 0.8
            or days_since_purchase > 120
            or (territory in {"Sur", "Oriente"} and num_coolers == 0)
        )
        churn_label = int(churn_signal and rng.random() > 0.18)

        data.append(
            {
                "customer_id": int(customer_id),
                "customer_name": f"Cliente {customer_id}",
                "territory": territory,
                "channel": channel,
                "customer_size": size,
                "total_sales": float(round(total_sales, 2)),
                "avg_sales": float(round(avg_sales, 2)),
                "purchase_frequency": float(round(purchase_frequency, 2)),
                "active_months": int(active_months),
                "days_since_purchase": int(days_since_purchase),
                "num_transactions": int(num_transactions),
                "num_coolers": int(num_coolers),
                "num_doors": int(max(1, num_doors)),
                "num_orders": int(num_orders),
                "num_skus": int(max(1, num_skus)),
                "product_substitutions": int(substitutions),
                "sales_trend": float(round(sales_trend, 2)),
                "monthly_variation": float(round(monthly_variation, 2)),
                "recency": int(recency),
                "target": int(churn_label),
            }
        )

    return pd.DataFrame(data)


def build_analytics_frame() -> pd.DataFrame:
    """Construye el dataset analítico para ML y dashboard."""
    return generate_demo_dataset()


def score_to_level(score: float) -> str:
    """Clasifica el riesgo en una escala ejecutiva."""
    if score < 40:
        return "Bajo"
    if score < 70:
        return "Medio"
    return "Alto"
