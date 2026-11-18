"""SDK DataForge Studio: reusable preprocessing functions (no Streamlit imports).

The project prepares features; it DOES NOT train or evaluate a model.
"""
from __future__ import annotations

import html
import io
import logging
import re
import time
import uuid

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# The students already learned this! Each run also uses its own in-memory handler.
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def clean_text(value) -> str:
    """Basic English review normalization. Retains negations such as 'not'."""
    if pd.isna(value) or not str(value).strip():
        return ""
    text = html.unescape(str(value))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    return " ".join(text.lower().split())


def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Column": df.columns,
            "Data Type": [str(t) for t in df.dtypes],
            "Missing": [int(df[c].isna().sum()) for c in df.columns],
            "Missing %": [round(df[c].isna().mean() * 100, 2) for c in df.columns],
            "Unique": [int(df[c].nunique(dropna=True)) for c in df.columns],
        }
    )


def outlier_flags(series: pd.Series) -> int:
    """Count potential IQR outliers; flag only, never automatically delete."""
    x = pd.to_numeric(series, errors="coerce").dropna()
    if len(x) < 4:
        return 0
    q1, q3 = x.quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr == 0:
        return 0
    return int(((x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)).sum())


def build_pipeline(numeric: list[str], categorical: list[str], text_col: str | None):
    """ColumnTransformer: each feature type receives the correct transformer."""
    transformers = []
    if numeric:
        transformers.append((
            "numbers",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
                ("scaler", StandardScaler()),
            ]),
            numeric,
        ))
    if categorical:
        transformers.append((
            "categories",
            Pipeline([
                ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]),
            categorical,
        ))
    if text_col:
        transformers.append((
            "reviews",
            TfidfVectorizer(max_features=200, ngram_range=(1, 2)),
            text_col,
        ))
    if not transformers:
        raise ValueError("Select at least one feature before running.")
    return ColumnTransformer(transformers, remainder="drop", sparse_threshold=1.0)


def prepare_reference(df: pd.DataFrame, numeric: list[str], categorical: list[str], text_col: str | None):
    """Type conversion/cleaning independent of Streamlit. Imputation occurs in Pipeline."""
    data = df.copy()
    for col in numeric:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    for col in categorical:
        data[col] = data[col].astype("string").fillna("Unknown").astype(str)
    if text_col:
        data[text_col] = data[text_col].map(clean_text)
    return data


def run_pipeline(df: pd.DataFrame, numeric: list[str], categorical: list[str], text_col: str | None = None):
    """Run reference-data preprocessing with captured per-run logging."""
    selected = list(numeric) + list(categorical) + ([text_col] if text_col else [])
    if len(selected) != len(set(selected)):
        raise ValueError("Each column must have one role only.")
    if not selected:
        raise ValueError("Select at least one feature column.")
    if not set(selected).issubset(df.columns):
        raise ValueError("Selected columns do not exist in the dataset.")
    if df.empty:
        raise ValueError("Dataset has no rows.")

    output = io.StringIO()
    logger = logging.getLogger("sdk_dataforge." + uuid.uuid4().hex)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler(output)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(handler)
    start = time.perf_counter()
    try:
        logger.info("STEP 1/6 · Loaded %s rows × %s columns", *df.shape)
        dup = int(df.duplicated().sum())
        if dup:
            logger.warning("Found %s exact duplicate rows (review before deleting)", dup)
        miss = int(df[selected].isna().sum().sum())
        if miss:
            logger.warning("Found %s missing cells in selected features", miss)
        else:
            logger.info("No missing cells in selected features")

        logger.info("STEP 2/6 · Data cleaning and type conversion started")
        prepared = prepare_reference(df, numeric, categorical, text_col)
        logger.info("Created readable cleaned preview; original data kept unchanged")

        for col in numeric:
            outliers = outlier_flags(prepared[col])
            if outliers:
                logger.warning("IQR flagged %d possible outliers in '%s' (not deleted)", outliers, col)
        if text_col:
            empty = int(prepared[text_col].eq("").sum())
            logger.info("STEP 3/6 · NLP cleaned '%s'; %d empty/blank reviews", text_col, empty)
            if prepared[text_col].eq("").all():
                raise ValueError("The text column has no usable text. Choose another column.")
        else:
            logger.info("STEP 3/6 · NLP skipped (no text feature selected)")

        logger.info("STEP 4/6 · Building ColumnTransformer")
        if numeric:
            logger.info("Numeric: median imputation → StandardScaler: %s", ", ".join(numeric))
        if categorical:
            logger.info("Categorical: fill Unknown → OneHotEncoder: %s", ", ".join(categorical))
        if text_col:
            logger.info("Text: TF-IDF (1–2 grams, max 200 features): %s", text_col)
        transformer = build_pipeline(numeric, categorical, text_col)

        logger.info("STEP 5/6 · fit_transform() on reference data")
        matrix = transformer.fit_transform(prepared)
        values = matrix.data if hasattr(matrix, "tocsr") else np.asarray(matrix)
        if not np.isfinite(values).all():
            raise ValueError("Feature matrix contains NaN or infinity.")
        names = transformer.get_feature_names_out().tolist()
        logger.info("Matrix validated: %d rows × %d numerical features", *matrix.shape)
        logger.info("STEP 6/6 · Finished successfully in %.2f seconds", time.perf_counter() - start)

        return {
            "cleaned": prepared,
            "matrix": matrix,
            "pipeline": transformer,
            "features": names,
            "logs": output.getvalue(),
            "missing_before": miss,
            "duplicates": dup,
            "seconds": time.perf_counter() - start,
            "roles": (list(numeric), list(categorical), text_col),
        }
    except Exception:
        logger.exception("FAILED · Check dataset/schema before retrying")
        raise
    finally:
        logger.removeHandler(handler)
        handler.close()


def transform_new_batch(fitted_pipeline, batch: pd.DataFrame, numeric: list[str], categorical: list[str], text_col: str | None):
    """Use the learned vocabulary, categories and scaler on a same-schema batch."""
    required = list(numeric) + list(categorical) + ([text_col] if text_col else [])
    missing = sorted(set(required) - set(batch.columns))
    if missing:
        raise ValueError(f"New batch is missing columns: {missing}")
    data = prepare_reference(batch, numeric, categorical, text_col)
    return fitted_pipeline.transform(data)
