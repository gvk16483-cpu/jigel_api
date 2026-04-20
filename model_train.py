import argparse
import pandas as pd
import joblib
import numpy as np
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion


# =========================
# LOAD DATA
# =========================

def load_data(path, text_col='text', label_col='label'):
    df = pd.read_csv(path)

    cols_lower = {c.lower(): c for c in df.columns}

    if text_col.lower() in cols_lower:
        text_c = cols_lower[text_col.lower()]
    else:
        raise ValueError("Text column not found")

    if label_col.lower() in cols_lower:
        label_c = cols_lower[label_col.lower()]
    else:
        raise ValueError("Label column not found")

    df = df.dropna(subset=[text_c, label_c])
    df = df.rename(columns={text_c: 'text', label_c: 'label'})
    return df


# =========================
# STRUCTURAL FEATURE ENGINEERING
# =========================

from features import structural_features
# =========================
# TRAIN MODEL
# =========================

def train(data_path, out_model, text_col='text', label_col='label'):
    print("Training started...\n")

    df = load_data(data_path, text_col=text_col, label_col=label_col)
    X = df["text"].astype(str)
    y = df["label"].astype(int)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    tfidf = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1,3),
        stop_words='english'
    )

    structural_transformer = FunctionTransformer(structural_features, validate=False)

    combined_features = FeatureUnion([
        ("tfidf", tfidf),
        ("structural", structural_transformer)
    ])

    pipeline = Pipeline([
        ("features", combined_features),
        ("clf", LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        ))
    ])

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_val)

    print("Accuracy:", accuracy_score(y_val, preds))
    print(classification_report(y_val, preds))

    joblib.dump(pipeline, out_model)
    print(f"\nModel saved to {out_model}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--out', default='model.joblib')
    parser.add_argument('--text-col', default='text')
    parser.add_argument('--label-col', default='label')
    args = parser.parse_args()

    train(args.data, args.out, args.text_col, args.label_col)
