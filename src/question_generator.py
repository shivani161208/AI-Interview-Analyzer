import pandas as pd


def load_questions(csv_path):
    questions_df = pd.read_csv(csv_path)

    required_columns = {
        "question_id",
        "role",
        "topic",
        "skill",
        "difficulty",
        "question"
    }

    missing_columns = required_columns - set(questions_df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns in questions.csv: {missing_columns}"
        )

    return questions_df


def generate_questions(
    role,
    skills,
    csv_path,
    difficulty=None,
    limit=5
):
    questions_df = load_questions(csv_path)

    result = questions_df.copy()

    # -----------------------------
    # Filter by role
    # -----------------------------

    if role:

        role_result = result[
            result["role"].astype(str).str.lower()
            == role.lower()
        ]

        if not role_result.empty:
            result = role_result

    # -----------------------------
    # Filter by candidate skills
    # -----------------------------

    if skills:

        skill_list = [
            str(skill).lower()
            for skill in skills
        ]

        skill_result = result[
            result["skill"].astype(str).str.lower().isin(
                skill_list
            )
        ]

        if not skill_result.empty:
            result = skill_result

    # -----------------------------
    # Filter by difficulty
    # -----------------------------

    if difficulty:

        difficulty_result = result[
            result["difficulty"].astype(str).str.lower()
            == difficulty.lower()
        ]

        if not difficulty_result.empty:
            result = difficulty_result

    # -----------------------------
    # Fallback
    # -----------------------------

    if result.empty:

        result = questions_df.copy()

        if role:

            role_result = result[
                result["role"].astype(str).str.lower()
                == role.lower()
            ]

            if not role_result.empty:
                result = role_result

    # -----------------------------
    # Random questions
    # -----------------------------

    result = result.sample(
        n=min(limit, len(result)),
        random_state=None
    )

    return result.to_dict("records")