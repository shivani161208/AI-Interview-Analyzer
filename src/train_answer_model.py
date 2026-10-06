from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "evaluation_data.csv"
MODEL_FILE = BASE_DIR / "models" / "answer_evaluation_model.pkl"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading evaluation data...")

df = pd.read_csv(DATA_FILE)

print(f"Dataset shape: {df.shape}")

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "relevance",
    "correctness",
    "clarity",
    "confidence",
    "technical_depth"
]

TARGET = "score"


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = FEATURES + [TARGET]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# ============================================================
# PREPARE DATA
# ============================================================

X = df[FEATURES]
y = df[TARGET]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# MODEL
# ============================================================

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "regressor",
        LinearRegression()
    )
])


# ============================================================
# TRAIN
# ============================================================

print("\nTraining answer evaluation model...")

model.fit(
    X_train,
    y_train
)


# ============================================================
# PREDICTION
# ============================================================

predictions = model.predict(X_test)


# ============================================================
# EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n-----------------------------------")
print("ANSWER EVALUATION MODEL")
print("-----------------------------------")

print(
    f"MAE: {mae:.4f}"
)

print(
    f"RMSE: {rmse:.4f}"
)

print(
    f"R2 Score: {r2:.4f}"
)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)


print("\n-----------------------------------")
print("MODEL SAVED SUCCESSFULLY")
print("-----------------------------------")

print(
    MODEL_FILE
)

print("-----------------------------------")