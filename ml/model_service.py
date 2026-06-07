from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from services.data_service import build_analytics_frame


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Prepara features numéricas y categóricas para ML."""
    feature_cols = [
        "territory",
        "channel",
        "customer_size",
        "total_sales",
        "avg_sales",
        "purchase_frequency",
        "active_months",
        "days_since_purchase",
        "num_transactions",
        "num_coolers",
        "num_doors",
        "num_orders",
        "num_skus",
        "product_substitutions",
        "sales_trend",
        "monthly_variation",
        "recency",
    ]
    X = df[feature_cols].copy()
    y = df["target"].astype(int)
    return X, y, feature_cols


def train_models() -> dict:
    """Entrena RF y Logistic Regression, elige el mejor por F1."""
    df = build_analytics_frame()
    X, y, feature_cols = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    categorical = X.select_dtypes(include=["object"]).columns.tolist()
    numeric = [c for c in X.columns if c not in categorical]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )

    models = {
        "Random Forest": Pipeline(
            [
                ("preprocessor", preprocessor),
                ("model", RandomForestClassifier(n_estimators=180, max_depth=8, random_state=42, n_jobs=-1)),
            ]
        ),
        "Logistic Regression": Pipeline(
            [
                ("preprocessor", preprocessor),
                ("model", LogisticRegression(max_iter=1200, class_weight="balanced")),
            ]
        ),
    }

    metrics = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics[name] = {
            "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0),
            "report": classification_report(y_test, pred, output_dict=True),
            "model": model,
            "feature_cols": feature_cols,
        }

    best_name = max(metrics, key=lambda key: metrics[key]["f1"])
    metrics["best_model"] = best_name
    metrics["best_model_metrics"] = metrics[best_name]
    return metrics


def predict_risk(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna score, nivel y probabilidad para cada cliente."""
    metrics = train_models()
    model = metrics[metrics["best_model"]]["model"]
    X, _, _ = prepare_features(df)

    probabilities = model.predict_proba(X)[:, 1]
    scores = (probabilities * 100).round(1)

    result = df.copy()
    result["score_risk"] = scores
    result["risk_level"] = result["score_risk"].apply(lambda value: "Bajo" if value < 40 else "Medio" if value < 70 else "Alto")
    result["probability_churn"] = probabilities.round(3)
    result["estimated_revenue_at_risk"] = (result["total_sales"] * result["probability_churn"]).round(2)
    return result
