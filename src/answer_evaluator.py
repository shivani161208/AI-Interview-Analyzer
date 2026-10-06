from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "answer_evaluation_model.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}\n"
        "Please run train_answer_model.py first."
    )

model = joblib.load(MODEL_PATH)


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


# ============================================================
# PREDICT ANSWER SCORE
# ============================================================

def predict_answer_score(
    relevance: float,
    correctness: float,
    clarity: float,
    confidence: float,
    technical_depth: float
):
    """
    Predict the overall interview answer score.

    Input values should be between 0 and 1.

    Returns:
        predicted_score
        performance_level
    """

    data = pd.DataFrame([{
        "relevance": relevance,
        "correctness": correctness,
        "clarity": clarity,
        "confidence": confidence,
        "technical_depth": technical_depth
    }])

    predicted_score = float(
        model.predict(data)[0]
    )

    # Keep score within 0-100
    predicted_score = max(
        0,
        min(
            100,
            predicted_score
        )
    )

    predicted_score = round(
        predicted_score,
        2
    )

    # --------------------------------------------------------
    # PERFORMANCE LEVEL
    # --------------------------------------------------------

    if predicted_score >= 80:
        performance_level = "Excellent"

    elif predicted_score >= 65:
        performance_level = "Good"

    elif predicted_score >= 40:
        performance_level = "Average"

    else:
        performance_level = "Needs Improvement"

    return (
        predicted_score,
        performance_level
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    score, performance = predict_answer_score(
        relevance=0.90,
        correctness=0.85,
        clarity=0.80,
        confidence=0.85,
        technical_depth=0.90
    )

    print("\n===================================")
    print("       ANSWER EVALUATOR")
    print("===================================")

    print(
        f"Predicted Score: {score}/100"
    )

    print(
        f"Performance Level: {performance}"
    )

    print("===================================")