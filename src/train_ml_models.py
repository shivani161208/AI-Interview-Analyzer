from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "relevance_training_data.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("Loading training data...")

df = pd.read_csv(DATA_FILE)

print(f"Dataset shape: {df.shape}")
print("\nColumns:")
print(df.columns.tolist())


# --------------------------------------------------
# FEATURES AND TARGET
# --------------------------------------------------

FEATURES = [
    "skill_overlap",
    "semantic_similarity",
    "experience_years",
    "keyword_match"
]

TARGET = "relevant"


X = df[FEATURES]
y = df[TARGET]


# --------------------------------------------------
# BASIC VALIDATION
# --------------------------------------------------

if y.nunique() < 2:
    raise ValueError(
        "The 'relevant' column must contain at least two classes."
    )

print("\nTarget distribution:")
print(y.value_counts())


# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = Pipeline([
    ("scaler", StandardScaler()),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

print("\nTraining relevance model...")

model.fit(X_train, y_train)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n-----------------------------------")
print("MODEL EVALUATION")
print("-----------------------------------")

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

model_path = MODEL_DIR / "relevance_model.pkl"

joblib.dump(model, model_path)

print("-----------------------------------")
print(f"Model saved successfully:")
print(model_path)
print("-----------------------------------")