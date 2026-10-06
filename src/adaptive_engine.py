def get_next_difficulty(score, current_difficulty):
    """
    Decide the difficulty of the next interview question
    based on the candidate's previous answer score.
    """

    if not isinstance(score, (int, float)):
        return current_difficulty

    difficulties = [
        "Beginner",
        "Medium",
        "Advanced"
    ]

    if current_difficulty not in difficulties:
        current_difficulty = "Medium"

    current_index = difficulties.index(
        current_difficulty
    )

    # ---------------------------------------------
    # Excellent performance
    # ---------------------------------------------

    if score >= 80:

        next_index = min(
            current_index + 1,
            len(difficulties) - 1
        )

    # ---------------------------------------------
    # Good performance
    # ---------------------------------------------

    elif score >= 65:

        next_index = current_index

    # ---------------------------------------------
    # Needs improvement
    # ---------------------------------------------

    elif score >= 40:

        next_index = max(
            current_index - 1,
            0
        )

    # ---------------------------------------------
    # Poor performance
    # ---------------------------------------------

    else:

        next_index = max(
            current_index - 1,
            0
        )

    return difficulties[next_index]


def get_adaptive_message(score, next_difficulty):
    """
    Generate a simple explanation for the
    difficulty adaptation.
    """

    if score >= 80:

        return (
            f"Strong performance! "
            f"The next question will be "
            f"{next_difficulty} level."
        )

    elif score >= 65:

        return (
            f"Good performance. "
            f"We will continue with "
            f"{next_difficulty} level."
        )

    elif score >= 40:

        return (
            f"Your answer can be improved. "
            f"The next question will be "
            f"{next_difficulty} level."
        )

    else:

        return (
            f"Let's strengthen the fundamentals. "
            f"The next question will be "
            f"{next_difficulty} level."
        )