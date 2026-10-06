import pandas as pd
import re


def load_skills(skill_file):
    """
    Load skills from skills.csv.
    """

    skills_df = pd.read_csv(skill_file)

    required_columns = {"skill", "category"}

    missing_columns = required_columns - set(skills_df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns in skills.csv: {missing_columns}"
        )

    return skills_df


def normalize_text(text):
    """
    Convert text into a normalized lowercase form.
    """

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(resume_text, skill_file):
    """
    Extract unique skills found in the resume.
    """

    skills_df = load_skills(skill_file)

    resume_text = normalize_text(resume_text)

    detected_skills = []

    for skill in skills_df["skill"].dropna().unique():

        skill_normalized = normalize_text(skill)

        # Escape special regex characters
        pattern = r"\b" + re.escape(skill_normalized) + r"\b"

        if re.search(pattern, resume_text):
            detected_skills.append(skill)

    return detected_skills