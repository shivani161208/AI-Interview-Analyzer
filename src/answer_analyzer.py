import re

from .ml_predictor import predict_relevance


# ============================================================
# ANSWER ANALYZER
# ============================================================

def analyze_answer(
    answer: str,
    skill_overlap: int = 0,
    semantic_similarity: float = 0.0,
    experience_years: float = 0.0,
    keyword_match: int = 0
) -> dict:
    """
    Analyze an interview answer using:

    1. Basic text analysis
    2. STAR-style structure
    3. Technical details
    4. Answer length
    5. ML-based relevance prediction

    Note:
    This analyzer evaluates answer quality signals.
    It does not claim to verify factual correctness.
    """

    # --------------------------------------------------------
    # BASIC TEXT ANALYSIS
    # --------------------------------------------------------

    if not isinstance(answer, str):
        answer = str(answer)

    text = answer.strip()
    lower = text.lower()

    words = re.findall(
        r"\b[\w+#.-]+\b",
        lower
    )

    word_count = len(words)

    # --------------------------------------------------------
    # STAR-STYLE CUES
    # --------------------------------------------------------

    context_phrases = (
        "when ",
        "during ",
        "in my project",
        "in our project",
        "the situation",
        "while working",
        "while developing"
    )

    action_phrases = (
        "i built",
        "i created",
        "i used",
        "i implemented",
        "i developed",
        "i analyzed",
        "i designed",
        "i worked",
        "i solved",
        "i applied"
    )

    result_phrases = (
        "result",
        "improved",
        "reduced",
        "increased",
        "saved",
        "achieved",
        "accuracy",
        "performance",
        "efficient"
    )

    technical_phrases = (
        "algorithm",
        "model",
        "database",
        "api",
        "python",
        "c++",
        "sql",
        "machine learning",
        "classification",
        "regression",
        "accuracy",
        "dataset",
        "framework"
    )

    cues = {
        "context": any(
            phrase in lower
            for phrase in context_phrases
        ),

        "action": any(
            phrase in lower
            for phrase in action_phrases
        ),

        "result": any(
            phrase in lower
            for phrase in result_phrases
        ),

        "specific_detail": any(
            char.isdigit()
            for char in text
        ),

        "technical_detail": any(
            phrase in lower
            for phrase in technical_phrases
        )
    }

    # --------------------------------------------------------
    # LENGTH SCORE - 20 MARKS
    # --------------------------------------------------------

    if word_count == 0:
        length_score = 0

    elif word_count < 20:
        length_score = 5

    elif word_count < 50:
        length_score = 10

    elif word_count < 100:
        length_score = 15

    else:
        length_score = 20

    # --------------------------------------------------------
    # STRUCTURE SCORE - 40 MARKS
    # --------------------------------------------------------

    structure_score = (
        sum(cues.values()) / len(cues)
    ) * 40

    # --------------------------------------------------------
    # DETAIL SCORE - 25 MARKS
    # --------------------------------------------------------

    detail_score = 0

    if cues["technical_detail"]:
        detail_score += 15

    if cues["specific_detail"]:
        detail_score += 10

    # --------------------------------------------------------
    # TEXT QUALITY SCORE
    # --------------------------------------------------------

    text_quality_score = (
        length_score
        + structure_score
        + detail_score
    )

    text_quality_score = min(
        round(text_quality_score),
        100
    )

    # --------------------------------------------------------
    # ML RELEVANCE PREDICTION
    # --------------------------------------------------------

    try:

        ml_prediction, ml_probability = predict_relevance(
            skill_overlap=skill_overlap,
            semantic_similarity=semantic_similarity,
            experience_years=experience_years,
            keyword_match=keyword_match
        )

        ml_relevance_score = round(
            ml_probability * 100,
            2
        )

    except Exception as error:

        print(
            f"ML prediction warning: {error}"
        )

        ml_prediction = 0
        ml_relevance_score = 0.0

    # --------------------------------------------------------
    # COMBINED SCORE
    # --------------------------------------------------------

    # 60% answer quality
    # 40% ML relevance

    final_score = (
        (text_quality_score * 0.60)
        + (ml_relevance_score * 0.40)
    )

    final_score = min(
        round(final_score),
        100
    )

    # --------------------------------------------------------
    # QUALITY LEVEL
    # --------------------------------------------------------

    if final_score >= 80:
        quality = "Excellent"

    elif final_score >= 60:
        quality = "Good"

    elif final_score >= 40:
        quality = "Average"

    else:
        quality = "Needs Improvement"

    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    strengths = []

    if word_count >= 50:
        strengths.append(
            "Answer has reasonable detail."
        )

    if cues["context"]:
        strengths.append(
            "Provides context or situation."
        )

    if cues["action"]:
        strengths.append(
            "Explains the actions taken."
        )

    if cues["result"]:
        strengths.append(
            "Mentions outcomes or results."
        )

    if cues["technical_detail"]:
        strengths.append(
            "Contains technical details."
        )

    if cues["specific_detail"]:
        strengths.append(
            "Includes specific measurable details."
        )

    if ml_relevance_score >= 70:
        strengths.append(
            "Answer appears relevant according to the ML model."
        )

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    improvements = []

    if word_count < 30:
        improvements.append(
            "Add more explanation and detail."
        )

    if not cues["context"]:
        improvements.append(
            "Explain the situation or context."
        )

    if not cues["action"]:
        improvements.append(
            "Clearly explain what you personally did."
        )

    if not cues["result"]:
        improvements.append(
            "Mention the result or outcome."
        )

    if not cues["technical_detail"]:
        improvements.append(
            "Include relevant technical details."
        )

    if not cues["specific_detail"]:
        improvements.append(
            "Add measurable or specific details where appropriate."
        )

    if ml_relevance_score < 60:
        improvements.append(
            "Make the answer more relevant to the asked question."
        )

    # --------------------------------------------------------
    # OVERALL FEEDBACK
    # --------------------------------------------------------

    if final_score >= 80:

        overall_feedback = (
            "Strong answer. It contains useful detail, "
            "good structure, and strong relevance."
        )

    elif final_score >= 60:

        overall_feedback = (
            "Good answer, but it can be improved "
            "with more specific details and stronger results."
        )

    elif final_score >= 40:

        overall_feedback = (
            "The answer has some useful information, "
            "but needs better structure, explanation, "
            "and relevance."
        )

    else:

        overall_feedback = (
            "The answer is too brief or lacks important "
            "interview details and relevance."
        )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        # Overall
        "score": final_score,
        "quality": quality,

        # Text analysis
        "text_quality_score": text_quality_score,
        "word_count": word_count,

        # ML analysis
        "ml_prediction": ml_prediction,
        "ml_relevance_score": ml_relevance_score,

        # Detailed analysis
        "cues": cues,
        "strengths": strengths,
        "improvements": improvements,

        # Feedback
        "overall_feedback": overall_feedback
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_answer = """
    In my machine learning project, I built a customer churn
    prediction model using Python and machine learning algorithms.
    I cleaned the dataset using Pandas and trained classification
    models. I compared the models using accuracy and F1 score.
    The final model achieved good performance and helped identify
    high-risk customers.
    """

    result = analyze_answer(
        answer=sample_answer,
        skill_overlap=1,
        semantic_similarity=0.80,
        experience_years=2.0,
        keyword_match=1
    )

    print("\n===================================")
    print("       AI INTERVIEW ANALYZER")
    print("===================================")

    print(
        f"\nOverall Score: "
        f"{result['score']}/100"
    )

    print(
        f"Quality: "
        f"{result['quality']}"
    )

    print(
        f"Word Count: "
        f"{result['word_count']}"
    )

    print(
        f"Text Quality Score: "
        f"{result['text_quality_score']}/100"
    )

    print(
        f"ML Relevance Score: "
        f"{result['ml_relevance_score']}%"
    )

    print(
        f"ML Prediction: "
        f"{result['ml_prediction']}"
    )

    print("\nStrengths:")

    for strength in result["strengths"]:
        print(f"- {strength}")

    print("\nImprovements:")

    for improvement in result["improvements"]:
        print(f"- {improvement}")

    print("\nOverall Feedback:")
    print(result["overall_feedback"])

    print("\n===================================")