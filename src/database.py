import sqlite3
from pathlib import Path
from datetime import datetime


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = DATABASE_DIR / "interview_history.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():
    """
    Create all required database tables.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # Interview table
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interviews (

            interview_id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_name TEXT NOT NULL,

            role TEXT NOT NULL,

            starting_difficulty TEXT,

            final_score REAL DEFAULT 0,

            final_performance TEXT,

            created_at TEXT NOT NULL

        )
        """
    )

    # -----------------------------------------------------
    # Interview Answers table
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interview_answers (

            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,

            interview_id INTEGER NOT NULL,

            question_number INTEGER,

            question TEXT,

            skill TEXT,

            topic TEXT,

            difficulty TEXT,

            answer TEXT,

            score REAL,

            performance TEXT,

            word_count INTEGER,

            feedback TEXT,

            next_difficulty TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (interview_id)
                REFERENCES interviews(interview_id)

        )
        """
    )

    connection.commit()
    connection.close()


# =========================================================
# CREATE INTERVIEW
# =========================================================

def create_interview(
    candidate_name,
    role,
    starting_difficulty=None,
    difficulty=None
):
    """
    Create a new interview session.

    Both starting_difficulty and difficulty are accepted
    so that the function remains compatible with different
    app.py calls.

    Returns:
        interview_id
    """

    # -----------------------------------------------------
    # Compatibility handling
    # -----------------------------------------------------

    if starting_difficulty is None:
        starting_difficulty = difficulty

    if starting_difficulty is None:
        starting_difficulty = "Beginner"

    # -----------------------------------------------------
    # Create database connection
    # -----------------------------------------------------

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    # -----------------------------------------------------
    # Insert interview
    # -----------------------------------------------------

    cursor.execute(
        """
        INSERT INTO interviews (
            candidate_name,
            role,
            starting_difficulty,
            final_score,
            final_performance,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            candidate_name,
            role,
            starting_difficulty,
            0,
            "Not Completed",
            created_at
        )
    )

    interview_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return interview_id


# =========================================================
# SAVE ANSWER
# =========================================================

def save_answer(
    interview_id,
    question_number,
    question,
    skill,
    topic,
    difficulty,
    answer,
    score,
    performance,
    word_count,
    feedback,
    next_difficulty
):
    """
    Save one interview question and answer.
    """

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    cursor.execute(
        """
        INSERT INTO interview_answers (

            interview_id,
            question_number,
            question,
            skill,
            topic,
            difficulty,
            answer,
            score,
            performance,
            word_count,
            feedback,
            next_difficulty,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            interview_id,
            question_number,
            question,
            skill,
            topic,
            difficulty,
            answer,
            score,
            performance,
            word_count,
            feedback,
            next_difficulty,
            created_at
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# COMPLETE INTERVIEW
# =========================================================

def complete_interview(
    interview_id,
    final_score,
    final_performance
):
    """
    Update an interview with its final score
    and final performance.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE interviews

        SET
            final_score = ?,
            final_performance = ?

        WHERE interview_id = ?
        """,
        (
            final_score,
            final_performance,
            interview_id
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# GET INTERVIEW HISTORY
# =========================================================

def get_interview_history(
    candidate_name=None
):
    """
    Retrieve previous interview sessions.

    If candidate_name is provided:
        Return only that candidate's interviews.

    If candidate_name is None:
        Return all interviews.

    The Admin Dashboard should use None to view
    complete interview history.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if candidate_name:

        cursor.execute(
            """
            SELECT
                interview_id,
                candidate_name,
                role,
                starting_difficulty,
                final_score,
                final_performance,
                created_at

            FROM interviews

            WHERE candidate_name = ?

            ORDER BY created_at DESC
            """,
            (candidate_name,)
        )

    else:

        cursor.execute(
            """
            SELECT
                interview_id,
                candidate_name,
                role,
                starting_difficulty,
                final_score,
                final_performance,
                created_at

            FROM interviews

            ORDER BY created_at DESC
            """
        )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# GET SINGLE INTERVIEW
# =========================================================

def get_interview(
    interview_id
):
    """
    Retrieve one interview by interview ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            interview_id,
            candidate_name,
            role,
            starting_difficulty,
            final_score,
            final_performance,
            created_at

        FROM interviews

        WHERE interview_id = ?
        """,
        (interview_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


# =========================================================
# GET INTERVIEW ANSWERS
# =========================================================

def get_interview_answers(
    interview_id
):
    """
    Retrieve all answers for a particular interview.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            answer_id,
            interview_id,
            question_number,
            question,
            skill,
            topic,
            difficulty,
            answer,
            score,
            performance,
            word_count,
            feedback,
            next_difficulty,
            created_at

        FROM interview_answers

        WHERE interview_id = ?

        ORDER BY question_number ASC
        """,
        (interview_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# GET ALL ANSWERS
# =========================================================

def get_all_answers():
    """
    Retrieve all interview answers.

    Mainly useful for Admin Dashboard
    and analytics.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            a.answer_id,
            a.interview_id,
            i.candidate_name,
            i.role,
            a.question_number,
            a.question,
            a.skill,
            a.topic,
            a.difficulty,
            a.answer,
            a.score,
            a.performance,
            a.word_count,
            a.feedback,
            a.next_difficulty,
            a.created_at

        FROM interview_answers a

        JOIN interviews i
            ON a.interview_id = i.interview_id

        ORDER BY a.created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# DELETE INTERVIEW
# =========================================================

def delete_interview(
    interview_id
):
    """
    Delete an interview and all its answers.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Delete answers first
    cursor.execute(
        """
        DELETE FROM interview_answers
        WHERE interview_id = ?
        """,
        (interview_id,)
    )

    # Delete interview
    cursor.execute(
        """
        DELETE FROM interviews
        WHERE interview_id = ?
        """,
        (interview_id,)
    )

    connection.commit()
    connection.close()


# =========================================================
# DELETE ALL INTERVIEW HISTORY
# =========================================================

def delete_all_interviews():
    """
    Delete all interview answers and interviews.

    Use carefully.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM interview_answers
        """
    )

    cursor.execute(
        """
        DELETE FROM interviews
        """
    )

    connection.commit()
    connection.close()


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

initialize_database()