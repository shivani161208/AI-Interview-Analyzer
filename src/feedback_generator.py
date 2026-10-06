def generate_feedback(analysis_result, question=None):
    """
    Generate detailed interview feedback from answer analysis.

    This module does not verify factual correctness.
    It focuses on structure, clarity, detail and interview quality.
    """

    if not isinstance(analysis_result, dict):
        return {
            "summary": "Unable to generate feedback.",
            "strengths": [],
            "improvements": [],
            "interview_tip": "Please provide a valid answer."
        }

    score = analysis_result.get("score", 0)
    word_count = analysis_result.get("word_count", 0)

    cues = analysis_result.get("cues", {})

    strengths = list(
        analysis_result.get("strengths", [])
    )

    improvements = list(
        analysis_result.get("improvements", [])
    )

    # -----------------------------------------
    # Overall Summary
    # -----------------------------------------

    if score >= 80:

        summary = (
            "Excellent interview response. "
            "Your answer demonstrates good structure, "
            "specificity and relevant technical detail."
        )

    elif score >= 65:

        summary = (
            "Good interview response. "
            "The main idea is clear, but adding stronger "
            "examples and measurable outcomes would make it better."
        )

    elif score >= 40:

        summary = (
            "Your answer shows some understanding, "
            "but it needs better structure, explanation "
            "and supporting details."
        )

    else:

        summary = (
            "The answer needs significant improvement. "
            "Try to explain your reasoning, actions and results "
            "more clearly."
        )

    # -----------------------------------------
    # Add Specific Feedback
    # -----------------------------------------

    if not cues.get("context", False):

        improvements.append(
            "Start with the situation or context so the interviewer "
            "understands the problem."
        )

    if not cues.get("action", False):

        improvements.append(
            "Explain what you personally did instead of only "
            "describing the project."
        )

    if not cues.get("result", False):

        improvements.append(
            "End with the result, impact or outcome of your work."
        )

    if not cues.get("technical_detail", False):

        improvements.append(
            "Mention relevant technologies, algorithms or tools "
            "used in the solution."
        )

    if not cues.get("specific_detail", False):

        improvements.append(
            "Add numbers or measurable results when possible."
        )

    # -----------------------------------------
    # Interview Tip
    # -----------------------------------------

    if question:

        question_text = str(question).lower()

        if any(
            word in question_text
            for word in [
                "project",
                "experience",
                "challenge",
                "problem"
            ]
        ):

            interview_tip = (
                "Use the STAR structure: Situation → Task → "
                "Action → Result."
            )

        elif any(
            word in question_text
            for word in [
                "explain",
                "what is",
                "define"
            ]
        ):

            interview_tip = (
                "Start with a clear definition, then explain "
                "how it works and give a practical example."
            )

        else:

            interview_tip = (
                "Give a direct answer first, then support it "
                "with an example or technical explanation."
            )

    else:

        interview_tip = (
            "Keep your answer structured: explain the idea, "
            "your approach and the final result."
        )

    # -----------------------------------------
    # Answer Quality
    # -----------------------------------------

    if word_count < 30:

        answer_quality = "Too brief"

    elif word_count < 60:

        answer_quality = "Moderately detailed"

    elif word_count < 120:

        answer_quality = "Well detailed"

    else:

        answer_quality = "Highly detailed"

    # -----------------------------------------
    # Final Feedback
    # -----------------------------------------

    return {
        "summary": summary,
        "answer_quality": answer_quality,
        "strengths": list(dict.fromkeys(strengths)),
        "improvements": list(dict.fromkeys(improvements)),
        "interview_tip": interview_tip
    }