def calculate_overall_score(analysis_result):
    """
    Calculate the overall interview answer score
    from the result produced by answer_analyzer.py.
    """

    if not isinstance(analysis_result, dict):
        return 0

    # Current answer_analyzer.py directly returns "score"
    score = analysis_result.get("score", 0)

    if isinstance(score, (int, float)):
        return round(float(score), 2)

    return 0


def get_performance_level(score):
    """
    Convert numerical score into a performance level.
    """

    if score >= 80:
        return "Excellent"

    elif score >= 65:
        return "Good"

    elif score >= 40:
        return "Needs Improvement"

    else:
        return "Poor"


def generate_score_report(analysis_result):
    """
    Generate a complete score report.
    """

    overall_score = calculate_overall_score(
        analysis_result
    )

    performance = get_performance_level(
        overall_score
    )

    return {
        "overall_score": overall_score,
        "performance_level": performance
    }