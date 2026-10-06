import streamlit as st
import pandas as pd
import hmac

from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.question_generator import generate_questions

from src.answer_analyzer import analyze_answer
from src.interview_evaluator import evaluate_interview_answer
from src.scoring_engine import generate_score_report

from src.voice_interviewer import record_voice_answer, speak_text

from src.adaptive_engine import (
    get_next_difficulty,
    get_adaptive_message
)

from src.feedback_generator import generate_feedback

from src.database import (
    initialize_database,
    create_interview,
    save_answer,
    complete_interview,
    get_interview_history,
    get_interview_answers
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon=None,
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

initialize_database()


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "questions": [],
    "current_question": 0,
    "answers": [],
    "analysis_results": [],
    "score_reports": [],
    "feedback_results": [],
    "difficulty_history": [],
    "current_difficulty": "Beginner",
    "asked_question_ids": [],
    "interview_id": None,
    "next_difficulty": None,
    "adaptive_message": "",
    "saved_answers": [],

    "candidate_name": "",
    "role": "",
    "resume_text": "",
    "skills": [],

    "voice_transcript": "",
    "voice_question_index": None,
    "voice_prefill_index": None,
    "spoken_question_index": None,

    "interview_mode": "Adaptive Interview",
    "interview_completed": False,

    "admin_logged_in": False
}


for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# ADMIN LOGIN
# ============================================================

def admin_login():

    st.sidebar.markdown("---")
    st.sidebar.subheader("Admin Login")

    username = st.sidebar.text_input(
        "Username",
        key="admin_username"
    )

    password = st.sidebar.text_input(
        "Password",
        type="password",
        key="admin_password"
    )

    if st.sidebar.button(
        "Login",
        use_container_width=True
    ):

        correct_username = str(
            st.secrets.get(
                "ADMIN_USERNAME",
                ""
            )
        )

        correct_password = str(
            st.secrets.get(
                "ADMIN_PASSWORD",
                ""
            )
        )

        username_match = hmac.compare_digest(
            str(username),
            correct_username
        )

        password_match = hmac.compare_digest(
            str(password),
            correct_password
        )

        if username_match and password_match:

            st.session_state.admin_logged_in = True

            st.rerun()

        else:

            st.session_state.admin_logged_in = False

            st.sidebar.error(
                "Invalid username or password."
            )

    return st.session_state.get(
        "admin_logged_in",
        False
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def show_admin_dashboard():

    st.title("Admin Dashboard")

    st.write(
        "Interview analytics and candidate performance records."
    )

    col1, col2 = st.columns([5, 1])

    with col2:

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.admin_logged_in = False

            st.rerun()

    st.markdown("---")

    try:

        history = get_interview_history()

        if not history:

            st.info(
                "No interview records found."
            )

            return

        history_df = pd.DataFrame(history)

        # ====================================================
        # BASIC STATISTICS
        # ====================================================

        total_interviews = len(history_df)

        if "final_score" in history_df.columns:

            scores = pd.to_numeric(
                history_df["final_score"],
                errors="coerce"
            ).dropna()

            if not scores.empty:

                average_score = round(
                    scores.mean(),
                    2
                )

                best_score = round(
                    scores.max(),
                    2
                )

            else:

                average_score = 0
                best_score = 0

        else:

            average_score = 0
            best_score = 0

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Interviews",
                total_interviews
            )

        with col2:

            st.metric(
                "Average Score",
                average_score
            )

        with col3:

            st.metric(
                "Best Score",
                best_score
            )

        # ====================================================
        # SCORE HISTORY
        # ====================================================

        if "final_score" in history_df.columns:

            st.markdown("---")

            st.subheader("Score History")

            chart_df = history_df.copy()

            chart_df["final_score"] = pd.to_numeric(
                chart_df["final_score"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["final_score"]
            )

            if not chart_df.empty:

                st.line_chart(
                    chart_df["final_score"]
                )

        # ====================================================
        # PERFORMANCE DISTRIBUTION
        # ====================================================

        if "performance_level" in history_df.columns:

            st.markdown("---")

            st.subheader(
                "Performance Distribution"
            )

            performance_data = (
                history_df[
                    "performance_level"
                ]
                .value_counts()
            )

            st.bar_chart(
                performance_data
            )

        # ====================================================
        # INTERVIEW HISTORY
        # ====================================================

        st.markdown("---")

        st.subheader(
            "Interview History"
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # INDIVIDUAL INTERVIEW
        # ====================================================

        if "id" in history_df.columns:

            st.markdown("---")

            st.subheader(
                "Interview Details"
            )

            interview_ids = (
                history_df["id"]
                .dropna()
                .tolist()
            )

            if interview_ids:

                selected_interview = st.selectbox(
                    "Select Interview",
                    interview_ids
                )

                try:

                    interview_answers = (
                        get_interview_answers(
                            selected_interview
                        )
                    )

                    if interview_answers:

                        answers_df = pd.DataFrame(
                            interview_answers
                        )

                        st.dataframe(
                            answers_df,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.info(
                            "No answer records found for this interview."
                        )

                except Exception as error:

                    st.error(
                        f"Could not load interview details: {error}"
                    )

    except Exception as error:

        st.error(
            f"Could not load interview history: {error}"
        )


# ============================================================
# INTERVIEW STATE RESET
# ============================================================

def reset_interview_state():

    st.session_state.questions = []
    st.session_state.current_question = 0

    st.session_state.answers = []
    st.session_state.analysis_results = []
    st.session_state.score_reports = []
    st.session_state.feedback_results = []

    st.session_state.difficulty_history = []
    st.session_state.asked_question_ids = []

    st.session_state.interview_id = None

    st.session_state.next_difficulty = None
    st.session_state.adaptive_message = ""

    st.session_state.saved_answers = []

    st.session_state.voice_transcript = ""
    st.session_state.voice_question_index = None
    st.session_state.voice_prefill_index = None
    st.session_state.spoken_question_index = None

    st.session_state.interview_completed = False


# ============================================================
# START INTERVIEW
# ============================================================

def start_interview(
    questions,
    candidate_name,
    role,
    difficulty,
    mode
):

    reset_interview_state()

    st.session_state.questions = questions

    st.session_state.candidate_name = (
        candidate_name
    )

    st.session_state.role = role

    st.session_state.current_difficulty = (
        difficulty
    )

    st.session_state.interview_mode = mode

    st.session_state.asked_question_ids = [
        q.get("question_id")
        for q in questions
        if q.get("question_id") is not None
    ]

    st.session_state.difficulty_history = [
        difficulty
    ]

    interview_id = create_interview(
        candidate_name=candidate_name,
        role=role,
        difficulty=difficulty
    )

    st.session_state.interview_id = interview_id


# ============================================================
# ANSWER EVALUATION
# ============================================================

def evaluate_answer(question, answer):

    ml_result = evaluate_interview_answer(
        question=question["question"],
        answer=answer,
        skills=st.session_state.skills
    )

    text_result = analyze_answer(
        answer
    )

    result = text_result.copy()

    predicted_score = (
        ml_result["predicted_score"]
    )

    performance_level = (
        ml_result["performance_level"]
    )

    result["score"] = predicted_score

    result["predicted_score"] = (
        predicted_score
    )

    result["performance_level"] = (
        performance_level
    )

    result["features"] = (
        ml_result["features"]
    )

    result["ml_features"] = (
        ml_result["features"]
    )

    result["quality"] = (
        performance_level
    )

    result["question"] = (
        question["question"]
    )

    result["answer"] = answer

    return result


# ============================================================
# STORE ANSWER
# ============================================================

def store_answer_result(
    question,
    answer,
    result,
    feedback
):

    report = generate_score_report(
        result
    )

    st.session_state.answers.append(
        answer
    )

    st.session_state.analysis_results.append(
        result
    )

    st.session_state.score_reports.append(
        report
    )

    st.session_state.feedback_results.append(
        feedback
    )

    try:

        save_answer(
            interview_id=st.session_state.interview_id,
            question=question["question"],
            answer=answer,
            score=report["overall_score"],
            performance=report["performance_level"]
        )

    except Exception as error:

        st.warning(
            f"Database save warning: {error}"
        )

    return report


# ============================================================
# RESET VOICE
# ============================================================

def reset_voice_state():

    st.session_state.voice_transcript = ""
    st.session_state.voice_question_index = None
    st.session_state.voice_prefill_index = None
    st.session_state.spoken_question_index = None


# ============================================================
# COMPLETE INTERVIEW
# ============================================================

def finish_interview():

    if st.session_state.interview_completed:

        return

    if not st.session_state.score_reports:

        return

    scores = [
        report["overall_score"]
        for report in st.session_state.score_reports
    ]

    average_score = (
        sum(scores) / len(scores)
    )

    try:

        complete_interview(
            interview_id=st.session_state.interview_id,
            final_score=round(
                average_score,
                2
            )
        )

    except Exception as error:

        st.warning(
            f"Database completion warning: {error}"
        )

    st.session_state.interview_completed = True


# ============================================================
# FINAL RESULT
# ============================================================

def show_final_result():

    if not st.session_state.score_reports:

        return

    scores = [
        report["overall_score"]
        for report in st.session_state.score_reports
    ]

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    if average_score >= 80:

        final_level = "Excellent"

    elif average_score >= 65:

        final_level = "Good"

    elif average_score >= 40:

        final_level = "Average"

    else:

        final_level = "Needs Improvement"

    st.markdown("---")

    st.subheader(
        "Final Interview Result"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Final Score",
            f"{average_score}/100"
        )

    with col2:

        st.metric(
            "Performance",
            final_level
        )

    with col3:

        st.metric(
            "Questions",
            len(scores)
        )

    score_df = pd.DataFrame({
        "Question": [
            f"Question {i + 1}"
            for i in range(len(scores))
        ],
        "Score": scores
    })

    st.subheader(
        "Question-wise Performance"
    )

    st.line_chart(
        score_df.set_index("Question")
    )

    st.subheader(
        "Overall Recommendation"
    )

    if average_score >= 80:

        st.success(
            "Excellent performance. Your answers show strong "
            "technical understanding and communication."
        )

    elif average_score >= 65:

        st.info(
            "Good performance. Focus on improving technical "
            "depth and providing more specific examples."
        )

    elif average_score >= 40:

        st.warning(
            "Your fundamentals are developing. Practice "
            "clearer explanations and structured answers."
        )

    else:

        st.warning(
            "More preparation is recommended. Focus on "
            "fundamentals, technical concepts and structured answers."
        )


# ============================================================
# ADMIN ACCESS
# ============================================================

admin_logged_in = admin_login()


# ============================================================
# ADMIN MODE
# ============================================================

if admin_logged_in:

    show_admin_dashboard()

    st.stop()


# ============================================================
# CANDIDATE APPLICATION
# ============================================================

st.title(
    "AI Interview Analyzer"
)

st.write(
    "AI-powered interview practice system using Machine Learning, "
    "adaptive questioning and automated answer evaluation."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "Interview Settings"
    )

    st.write(
        "Configure your interview before starting."
    )

    st.markdown("---")

    st.subheader(
        "Project Features"
    )

    st.write(
        "Resume Skill Extraction"
    )

    st.write(
        "Role-based Questions"
    )

    st.write(
        "Adaptive Difficulty"
    )

    st.write(
        "Mock Interview"
    )

    st.write(
        "Voice Answer Support"
    )

    st.write(
        "ML Answer Evaluation"
    )

    st.write(
        "Performance Feedback"
    )


# ============================================================
# INTERVIEW MODE
# ============================================================

interview_active = (
    len(st.session_state.questions) > 0
)

interview_mode = st.radio(
    "Select Interview Mode",
    [
        "Adaptive Interview",
        "Mock Interview"
    ],
    horizontal=True,
    disabled=interview_active,
    key="interview_mode_selector"
)

st.session_state.interview_mode = (
    interview_mode
)


# ============================================================
# BASIC DETAILS
# ============================================================

candidate_name = st.text_input(
    "Candidate Name",
    value=st.session_state.candidate_name,
    disabled=interview_active
)


role_options = [
    "AI Engineer",
    "Backend Developer",
    "Data Analyst",
    "Data Scientist",
    "Frontend Developer",
    "Full Stack Developer",
    "Java Developer",
    "Machine Learning Engineer",
    "Python Developer",
    "Software Developer"
]


current_role_index = 0

if st.session_state.role in role_options:

    current_role_index = (
        role_options.index(
            st.session_state.role
        )
    )


role = st.selectbox(
    "Target Role",
    role_options,
    index=current_role_index,
    disabled=interview_active
)


difficulty_options = [
    "Beginner",
    "Medium",
    "Advanced"
]


if (
    st.session_state.current_difficulty
    in difficulty_options
):

    current_difficulty_index = (
        difficulty_options.index(
            st.session_state.current_difficulty
        )
    )

else:

    current_difficulty_index = 0


difficulty = st.selectbox(
    "Starting Difficulty",
    difficulty_options,
    index=current_difficulty_index,
    disabled=interview_active
)


st.session_state.candidate_name = (
    candidate_name
)

st.session_state.role = role


# ============================================================
# RESUME
# ============================================================

st.markdown("---")

st.subheader(
    "Resume and Skills"
)

uploaded_resume = st.file_uploader(
    "Upload your resume PDF",
    type=["pdf"],
    disabled=interview_active
)


# ============================================================
# ADAPTIVE INTERVIEW SETUP
# ============================================================

if interview_mode == "Adaptive Interview":

    if not interview_active:

        if uploaded_resume is not None:

            if st.button(
                "Analyze Resume and Start Adaptive Interview",
                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing resume and generating questions..."
                ):

                    try:

                        resume_text = (
                            extract_text_from_pdf(
                                uploaded_resume
                            )
                        )

                        if not resume_text.strip():

                            st.error(
                                "Could not extract readable text "
                                "from the resume."
                            )

                            st.stop()

                        skills = extract_skills(
                            resume_text,
                            "data/skills.csv"
                        )

                        questions = generate_questions(
                            role=role,
                            skills=skills,
                            csv_path="data/questions.csv",
                            difficulty=difficulty,
                            limit=5
                        )

                        if not questions:

                            st.error(
                                "No questions could be generated."
                            )

                            st.stop()

                        st.session_state.resume_text = (
                            resume_text
                        )

                        st.session_state.skills = (
                            skills
                        )

                        start_interview(
                            questions=questions,
                            candidate_name=candidate_name,
                            role=role,
                            difficulty=difficulty,
                            mode="Adaptive Interview"
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Error while starting interview: {error}"
                        )

        else:

            st.info(
                "Upload your resume PDF to start the Adaptive Interview."
            )


# ============================================================
# MOCK INTERVIEW SETUP
# ============================================================

if interview_mode == "Mock Interview":

    if not interview_active:

        st.info(
            "Mock Interview uses a fixed question sequence. "
            "The difficulty does not change according to your score."
        )

        if uploaded_resume is not None:

            if st.button(
                "Analyze Resume",
                use_container_width=True
            ):

                with st.spinner(
                    "Extracting skills from resume..."
                ):

                    try:

                        resume_text = (
                            extract_text_from_pdf(
                                uploaded_resume
                            )
                        )

                        if not resume_text.strip():

                            st.error(
                                "Could not extract readable text."
                            )

                            st.stop()

                        skills = extract_skills(
                            resume_text,
                            "data/skills.csv"
                        )

                        st.session_state.resume_text = (
                            resume_text
                        )

                        st.session_state.skills = (
                            skills
                        )

                        st.success(
                            f"Resume analyzed successfully. "
                            f"{len(skills)} skills detected."
                        )

                        if skills:

                            st.write(
                                "Detected Skills:",
                                ", ".join(
                                    map(
                                        str,
                                        skills
                                    )
                                )
                            )

                    except Exception as error:

                        st.error(
                            f"Resume analysis failed: {error}"
                        )

        if st.button(
            "Start Mock Interview",
            use_container_width=True
        ):

            with st.spinner(
                "Preparing mock interview..."
            ):

                try:

                    questions = generate_questions(
                        role=role,
                        skills=st.session_state.skills,
                        csv_path="data/questions.csv",
                        difficulty=difficulty,
                        limit=5
                    )

                    if not questions:

                        st.error(
                            "No questions available for this role."
                        )

                        st.stop()

                    start_interview(
                        questions=questions,
                        candidate_name=candidate_name,
                        role=role,
                        difficulty=difficulty,
                        mode="Mock Interview"
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Could not start Mock Interview: {error}"
                    )


# ============================================================
# INTERVIEW
# ============================================================

if interview_active:

    st.markdown("---")

    mode = (
        st.session_state.interview_mode
    )

    if mode == "Adaptive Interview":

        st.header(
            "Adaptive Interview"
        )

        st.caption(
            "The next question difficulty changes according "
            "to your performance."
        )

    else:

        st.header(
            "Mock Interview"
        )

        st.caption(
            "Answer all questions as if you are in a real interview."
        )


    current_index = (
        st.session_state.current_question
    )

    total_questions = len(
        st.session_state.questions
    )

    progress = (
        (current_index + 1)
        / total_questions
    )

    st.progress(
        progress
    )

    st.write(
        f"Question {current_index + 1} of {total_questions}"
    )


    current_question = (
        st.session_state.questions[
            current_index
        ]
    )

    question_text = (
        current_question["question"]
    )

    question_difficulty = (
        current_question.get(
            "difficulty",
            st.session_state.current_difficulty
        )
    )

    question_topic = (
        current_question.get(
            "topic",
            "General"
        )
    )

    question_skill = (
        current_question.get(
            "skill",
            "General"
        )
    )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            f"Difficulty: {question_difficulty}"
        )

    with col2:

        st.info(
            f"Topic: {question_topic}"
        )

    with col3:

        st.info(
            f"Skill: {question_skill}"
        )


    # ========================================================
    # SPEAK QUESTION
    # ========================================================

    if (
        st.session_state.spoken_question_index
        != current_index
    ):

        try:

            speak_text(
                question_text
            )

        except Exception:

            pass

        st.session_state.spoken_question_index = (
            current_index
        )


    st.subheader(
        "Interview Question"
    )

    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #cccccc;
            margin-bottom: 20px;
        ">
            <h3>{question_text}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ANSWER
    # ========================================================

    answer_key = (
        f"answer_{current_index}"
    )

    if answer_key not in st.session_state:

        st.session_state[answer_key] = ""


    if (
        st.session_state.voice_prefill_index
        == current_index
        and st.session_state.voice_transcript
    ):

        st.session_state[answer_key] = (
            st.session_state.voice_transcript
        )

        st.session_state.voice_prefill_index = None


    answer = st.text_area(
        "Your Answer",
        key=answer_key,
        height=180,
        placeholder=(
            "Type your interview answer here..."
        )
    )


    # ========================================================
    # VOICE ANSWER
    # ========================================================

    st.subheader(
        "Voice Answer"
    )

    try:

        voice_result = (
            record_voice_answer()
        )

        if voice_result:

            st.session_state.voice_transcript = (
                voice_result
            )

            st.session_state.voice_question_index = (
                current_index
            )

            st.success(
                "Voice answer captured successfully."
            )

    except Exception as error:

        st.warning(
            f"Voice input is currently unavailable: {error}"
        )


    if (
        st.session_state.voice_transcript
        and
        st.session_state.voice_question_index
        == current_index
    ):

        with st.expander(
            "View Voice Transcript"
        ):

            st.write(
                st.session_state.voice_transcript
            )

        if st.button(
            "Use Voice Answer",
            key=f"use_voice_{current_index}"
        ):

            st.session_state.voice_prefill_index = (
                current_index
            )

            st.rerun()


    # ========================================================
    # ANALYZE ANSWER
    # ========================================================

    st.markdown("---")

    if st.button(
        "Analyze Answer",
        type="primary",
        use_container_width=True,
        key=f"analyze_{current_index}"
    ):

        final_answer = (
            st.session_state.get(
                answer_key,
                ""
            )
            .strip()
        )

        if not final_answer:

            st.warning(
                "Please provide an answer before analysis."
            )

            st.stop()


        with st.spinner(
            "AI is analyzing your answer..."
        ):

            try:

                result = evaluate_answer(
                    question=current_question,
                    answer=final_answer
                )

                feedback = generate_feedback(
                    result
                )

                store_answer_result(
                    question=current_question,
                    answer=final_answer,
                    result=result,
                    feedback=feedback
                )


                if mode == "Adaptive Interview":

                    next_difficulty = (
                        get_next_difficulty(
                            result["score"],
                            st.session_state.current_difficulty
                        )
                    )

                    st.session_state.next_difficulty = (
                        next_difficulty
                    )

                    st.session_state.adaptive_message = (
                        get_adaptive_message(
                            result["score"],
                            next_difficulty
                        )
                    )


                st.rerun()

            except Exception as error:

                st.error(
                    f"Answer analysis failed: {error}"
                )


# ============================================================
# LATEST ANSWER RESULT
# ============================================================

if (
    st.session_state.analysis_results
    and
    st.session_state.current_question
    < len(
        st.session_state.analysis_results
    )
):

    result_index = (
        len(
            st.session_state.analysis_results
        ) - 1
    )

    result = (
        st.session_state.analysis_results[
            result_index
        ]
    )

    report = (
        st.session_state.score_reports[
            result_index
        ]
    )

    feedback = (
        st.session_state.feedback_results[
            result_index
        ]
    )


    st.markdown("---")

    st.header(
        "AI Answer Evaluation"
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Overall Score",
            f"{report['overall_score']}/100"
        )

    with col2:

        st.metric(
            "Performance",
            report["performance_level"]
        )

    with col3:

        st.metric(
            "Word Count",
            result.get(
                "word_count",
                0
            )
        )

    with col4:

        st.metric(
            "ML Score",
            f"{result.get('predicted_score', 0)}/100"
        )


    # ========================================================
    # ML FEATURES
    # ========================================================

    st.subheader(
        "ML Evaluation Features"
    )

    features = result.get(
        "features",
        {}
    )

    feature_columns = st.columns(5)

    feature_names = [
        ("Relevance", "relevance"),
        ("Correctness", "correctness"),
        ("Clarity", "clarity"),
        ("Confidence", "confidence"),
        ("Technical Depth", "technical_depth")
    ]

    for column, (label, key) in zip(
        feature_columns,
        feature_names
    ):

        value = features.get(
            key,
            0
        )

        with column:

            st.metric(
                label,
                f"{value * 100:.1f}%"
            )


    # ========================================================
    # FEEDBACK
    # ========================================================

    st.subheader(
        "AI Feedback"
    )

    overall_feedback = result.get(
        "overall_feedback",
        ""
    )

    if overall_feedback:

        st.write(
            overall_feedback
        )


    strengths = result.get(
        "strengths",
        []
    )

    if strengths:

        st.markdown(
            "### Strengths"
        )

        for strength in strengths:

            st.write(
                f"• {strength}"
            )


    improvements = result.get(
        "improvements",
        []
    )

    if improvements:

        st.markdown(
            "### Areas for Improvement"
        )

        for improvement in improvements:

            st.write(
                f"• {improvement}"
            )


    # ========================================================
    # DETAILED FEEDBACK
    # ========================================================

    if isinstance(
        feedback,
        dict
    ):

        st.subheader(
            "Detailed Interview Feedback"
        )

        summary = feedback.get(
            "summary"
        )

        answer_quality = feedback.get(
            "answer_quality"
        )

        feedback_strengths = feedback.get(
            "strengths",
            []
        )

        feedback_improvements = feedback.get(
            "improvements",
            []
        )

        interview_tip = feedback.get(
            "interview_tip"
        )


        if summary:

            st.write(
                f"Summary: {summary}"
            )


        if answer_quality:

            st.write(
                f"Answer Quality: {answer_quality}"
            )


        if feedback_strengths:

            st.write(
                "Strong Points:"
            )

            for item in feedback_strengths:

                st.write(
                    f"• {item}"
                )


        if feedback_improvements:

            st.write(
                "Improvements:"
            )

            for item in feedback_improvements:

                st.write(
                    f"• {item}"
                )


        if interview_tip:

            st.info(
                f"Interview Tip: {interview_tip}"
            )


    # ========================================================
    # NEXT QUESTION
    # ========================================================

    current_index = (
        st.session_state.current_question
    )

    total_questions = len(
        st.session_state.questions
    )


    if (
        current_index + 1
        < total_questions
    ):

        st.markdown("---")

        mode = (
            st.session_state.interview_mode
        )


        # ====================================================
        # ADAPTIVE MODE
        # ====================================================

        if mode == "Adaptive Interview":

            next_difficulty = (
                st.session_state.next_difficulty
                or
                st.session_state.current_difficulty
            )

            adaptive_message = (
                st.session_state.adaptive_message
            )

            if adaptive_message:

                st.info(
                    adaptive_message
                )

            st.write(
                f"Next Question Difficulty: "
                f"{next_difficulty}"
            )

            if st.button(
                "Next Adaptive Question",
                type="primary",
                use_container_width=True
            ):

                st.session_state.current_question += 1

                st.session_state.current_difficulty = (
                    next_difficulty
                )

                st.session_state.difficulty_history.append(
                    next_difficulty
                )

                reset_voice_state()

                st.rerun()


        # ====================================================
        # MOCK MODE
        # ====================================================

        else:

            st.info(
                "Mock Interview uses a fixed question sequence."
            )

            if st.button(
                "Next Mock Question",
                type="primary",
                use_container_width=True
            ):

                st.session_state.current_question += 1

                reset_voice_state()

                st.rerun()


    else:

        # ====================================================
        # INTERVIEW COMPLETED
        # ====================================================

        finish_interview()

        show_final_result()

        st.markdown("---")

        if st.button(
            "Start New Interview",
            use_container_width=True
        ):

            reset_interview_state()

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI Interview Analyzer | Machine Learning | "
    "Adaptive Interview | Mock Interview"
)