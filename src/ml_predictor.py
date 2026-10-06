from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# MODEL PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "relevance_model.pkl"


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}\n"
        "Please run train_ml_models.py first."
    )

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

FEATURES = [
    "skill_overlap",
    "semantic_similarity",
    "experience_years",
    "keyword_match"
]


# --------------------------------------------------
# PREDICT RELEVANCE
# --------------------------------------------------

def predict_relevance(
    skill_overlap: int,
    semantic_similarity: float,
    experience_years: float,
    keyword_match: int
):
    """
    Predict whether a candidate's answer/skill
    is relevant to the required skill.

    Returns:
        prediction: 0 or 1
        probability: probability of relevance
    """

    data = pd.DataFrame([{
        "skill_overlap": skill_overlap,
        "semantic_similarity": semantic_similarity,
        "experience_years": experience_years,
        "keyword_match": keyword_match
    }])

    prediction = int(model.predict(data)[0])

    probabilities = model.predict_proba(data)[0]

    # Probability of class 1 (relevant)
    relevance_probability = float(probabilities[1])

    return prediction, relevance_probability


# --------------------------------------------------
# SIMPLE TEST
# --------------------------------------------------

if __name__ == "__main__":

    prediction, probability = predict_relevance(
        skill_overlap=1,
        semantic_similarity=0.80,
        experience_years=2.0,
        keyword_match=1
    )

    print("-----------------------------------")
    print("ML RELEVANCE PREDICTION")
    print("-----------------------------------")

    print(f"Prediction: {prediction}")
    print(f"Relevance Probability: {probability:.4f}")
    print(f"Relevance Percentage: {probability * 100:.2f}%")

    if prediction == 1:
        print("Result: Relevant")
    else:
        print("Result: Not Relevant")