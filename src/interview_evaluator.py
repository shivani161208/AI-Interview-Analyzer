from .feature_extractor import extract_answer_features
from .answer_evaluator import predict_answer_score


def evaluate_interview_answer(
    question,
    answer,
    skills=None
):
    """
    Complete ML pipeline:

    Question + Answer + Resume Skills
            ↓
    Feature Extraction
            ↓
    ML Score Prediction
    """

    # --------------------------------------------------------
    # 1. Extract features
    # --------------------------------------------------------

    features = extract_answer_features(
        question=question,
        answer=answer,
        skills=skills
    )

    # --------------------------------------------------------
    # 2. Predict score
    # --------------------------------------------------------

    predicted_score, performance_level = (
        predict_answer_score(
            relevance=features["relevance"],
            correctness=features["correctness"],
            clarity=features["clarity"],
            confidence=features["confidence"],
            technical_depth=features["technical_depth"]
        )
    )

    # --------------------------------------------------------
    # 3. Return complete result
    # --------------------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "features": features,
        "predicted_score": predicted_score,
        "performance_level": performance_level
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = (
        "What is machine learning and "
        "how is it used in real-world applications?"
    )

    answer = """
    Machine learning is a branch of artificial intelligence
    where models learn patterns from data. I used Python,
    Pandas and scikit-learn in my project to clean a dataset,
    train classification models and evaluate them using
    accuracy and F1 score. The model was then used to identify
    high-risk customers.
    """

    skills = [
        "Python",
        "Machine Learning",
        "Pandas",
        "Scikit-learn"
    ]

    result = evaluate_interview_answer(
        question=question,
        answer=answer,
        skills=skills
    )

    print("\n===================================")
    print("      AI INTERVIEW EVALUATION")
    print("===================================")

    print("\nQuestion:")
    print(result["question"])

    print("\nML Features:")

    for feature, value in result["features"].items():
        print(f"- {feature}: {value}")

    print("\n-----------------------------------")

    print(
        f"Predicted Score: "
        f"{result['predicted_score']}/100"
    )

    print(
        f"Performance Level: "
        f"{result['performance_level']}"
    )

    print("===================================")