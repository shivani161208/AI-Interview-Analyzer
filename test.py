from src.database import (
    initialize_database,
    create_interview,
    save_answer,
    complete_interview,
    get_interview_history,
    get_interview_answers
)


# Initialize database

initialize_database()


# Create interview

interview_id = create_interview(
    candidate_name="Test Candidate",
    role="Python Developer",
    starting_difficulty="Medium"
)

print(
    "Interview ID:",
    interview_id
)


# Save answer

save_answer(
    interview_id=interview_id,
    question_number=1,
    question="What is Python?",
    skill="Python",
    topic="Programming",
    difficulty="Medium",
    answer=(
        "Python is a high-level programming "
        "language used for software development "
        "and data science."
    ),
    score=75,
    performance="Good",
    word_count=20,
    feedback="Good explanation but add a practical example.",
    next_difficulty="Medium"
)


# Complete interview

complete_interview(
    interview_id=interview_id,
    final_score=75,
    final_performance="Good"
)


# Get history

history = get_interview_history()

print("\nInterview History:")

for interview in history:

    print(interview)


# Get answers

answers = get_interview_answers(
    interview_id
)

print("\nInterview Answers:")

for answer in answers:

    print(answer)