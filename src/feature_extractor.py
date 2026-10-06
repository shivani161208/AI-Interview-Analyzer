import re


# ============================================================
# FEATURE EXTRACTOR
# ============================================================

def normalize_text(text):
    """Convert text into lowercase normalized text."""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# WORD COUNT
# ============================================================

def get_word_count(answer):
    """Return number of words in the answer."""

    words = re.findall(
        r"\b[\w+#.-]+\b",
        answer
    )

    return len(words)


# ============================================================
# KEYWORD MATCH
# ============================================================

def calculate_keyword_match(question, answer):
    """
    Calculate how many important question words
    are present in the answer.
    """

    question = normalize_text(question)
    answer = normalize_text(answer)

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question
        )
    )

    answer_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            answer
        )
    )

    if not question_words:
        return 0.0

    common_words = (
        question_words.intersection(answer_words)
    )

    return round(
        len(common_words) / len(question_words),
        3
    )


# ============================================================
# TECHNICAL DEPTH
# ============================================================

def calculate_technical_depth(answer, skills=None):
    """
    Estimate technical depth from technical terminology
    and candidate skills.
    """

    answer = normalize_text(answer)

    technical_terms = {
        "algorithm",
        "api",
        "database",
        "sql",
        "python",
        "java",
        "c++",
        "machine learning",
        "deep learning",
        "model",
        "classification",
        "regression",
        "neural network",
        "dataset",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "docker",
        "git",
        "rest",
        "backend",
        "frontend",
        "framework",
        "authentication",
        "optimization",
        "accuracy",
        "f1",
        "precision",
        "recall"
    }

    if skills:
        technical_terms.update(
            normalize_text(skill)
            for skill in skills
        )

    matched = 0

    for term in technical_terms:

        if term in answer:
            matched += 1

    # Convert to 0-1 range
    score = min(
        matched / 8,
        1.0
    )

    return round(
        score,
        3
    )


# ============================================================
# CLARITY
# ============================================================

def calculate_clarity(answer):
    """
    Estimate answer clarity using sentence length
    and basic readability signals.
    """

    answer = answer.strip()

    if not answer:
        return 0.0

    sentences = re.split(
        r"[.!?]+",
        answer
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    word_count = get_word_count(answer)

    if word_count == 0:
        return 0.0

    # Very short answers lack explanation
    length_score = min(
        word_count / 60,
        1.0
    )

    # Extremely long sentences can reduce clarity
    sentence_lengths = [
        get_word_count(sentence)
        for sentence in sentences
    ]

    if sentence_lengths:

        average_sentence_length = (
            sum(sentence_lengths)
            / len(sentence_lengths)
        )

        if 8 <= average_sentence_length <= 25:
            sentence_score = 1.0

        elif 5 <= average_sentence_length <= 35:
            sentence_score = 0.8

        else:
            sentence_score = 0.6

    else:
        sentence_score = 0.5

    clarity = (
        length_score * 0.5
        + sentence_score * 0.5
    )

    return round(
        min(clarity, 1.0),
        3
    )


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_confidence(answer):
    """
    Estimate confidence from assertive language,
    first-person ownership and hesitation words.
    """

    answer = normalize_text(answer)

    if not answer:
        return 0.0

    confident_phrases = [
        "i built",
        "i developed",
        "i implemented",
        "i designed",
        "i created",
        "i solved",
        "i analyzed",
        "i used",
        "i achieved",
        "i improved",
        "i successfully"
    ]

    hesitation_phrases = [
        "maybe",
        "perhaps",
        "i think",
        "i guess",
        "probably",
        "not sure",
        "i don't know"
    ]

    confident_count = sum(
        phrase in answer
        for phrase in confident_phrases
    )

    hesitation_count = sum(
        phrase in answer
        for phrase in hesitation_phrases
    )

    score = 0.5

    score += (
        confident_count * 0.08
    )

    score -= (
        hesitation_count * 0.10
    )

    return round(
        max(0.0, min(score, 1.0)),
        3
    )


# ============================================================
# CORRECTNESS
# ============================================================

def calculate_correctness(
    question,
    answer,
    skills=None
):
    """
    Estimate correctness using answer completeness,
    question-answer keyword overlap and technical depth.

    This is a heuristic estimate, not factual verification.
    """

    keyword_match = calculate_keyword_match(
        question,
        answer
    )

    technical_depth = calculate_technical_depth(
        answer,
        skills
    )

    word_count = get_word_count(answer)

    if word_count >= 80:
        completeness = 1.0

    elif word_count >= 50:
        completeness = 0.85

    elif word_count >= 25:
        completeness = 0.70

    elif word_count >= 10:
        completeness = 0.50

    else:
        completeness = 0.25

    correctness = (
        keyword_match * 0.40
        + technical_depth * 0.30
        + completeness * 0.30
    )

    return round(
        min(correctness, 1.0),
        3
    )


# ============================================================
# MAIN FEATURE EXTRACTION
# ============================================================

def extract_answer_features(
    question,
    answer,
    skills=None
):
    """
    Extract the five ML features required by
    answer_evaluation_model.pkl.
    """

    question = str(question)
    answer = str(answer)

    relevance = calculate_keyword_match(
        question,
        answer
    )

    correctness = calculate_correctness(
        question,
        answer,
        skills
    )

    clarity = calculate_clarity(
        answer
    )

    confidence = calculate_confidence(
        answer
    )

    technical_depth = calculate_technical_depth(
        answer,
        skills
    )

    return {
        "relevance": relevance,
        "correctness": correctness,
        "clarity": clarity,
        "confidence": confidence,
        "technical_depth": technical_depth
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

    features = extract_answer_features(
        question,
        answer,
        skills
    )

    print("\n===================================")
    print("       ANSWER FEATURE EXTRACTION")
    print("===================================")

    for feature, value in features.items():

        print(
            f"{feature}: {value}"
        )

    print("===================================")