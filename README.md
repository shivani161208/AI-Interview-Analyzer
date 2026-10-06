# AI Interview Analyzer

An AI-powered interview practice and evaluation system designed to simulate technical interviews, analyze candidate answers, and provide personalized performance feedback.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://ai-interview-analyzer-ky6cyrtxmbfnph9mg5mu8k.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/shivani161208/AI-Interview-Analyzer)

## Live Application

**AI Interview Analyzer – Streamlit**

https://ai-interview-analyzer-ky6cyrtxmbfnph9mg5mu8k.streamlit.app/

The application provides an interactive interview environment where candidates can select a role, upload their resume, answer technical questions, and receive AI-based evaluation and feedback.

---

## Overview

The **AI Interview Analyzer** is a machine learning based interview preparation platform developed as a college mini project.

The system combines:

- Resume skill extraction
- Role-based interview questions
- Adaptive interview difficulty
- Mock interview simulation
- Voice answer support
- Machine learning based answer evaluation
- Performance scoring
- Personalized feedback
- Interview analytics
- Admin dashboard

The main objective is to provide candidates with a structured environment to practice technical interviews and understand their strengths and areas for improvement.

---

## Key Features

### 1. Resume Skill Extraction

Candidates can upload their resume in PDF format.

The system extracts text from the resume and identifies relevant technical skills using a predefined skills dataset.

**Example skills:**

- Python
- C++
- Java
- SQL
- Machine Learning
- Data Structures
- Pandas
- Docker
- APIs
- DBMS

---

### 2. Role-Based Interview Questions

Questions are generated according to the selected technical role.

Supported roles include:

- AI Engineer
- Backend Developer
- Data Analyst
- Data Scientist
- Frontend Developer
- Full Stack Developer
- Java Developer
- Machine Learning Engineer
- Python Developer
- Software Developer

---

### 3. Adaptive Interview

The interview can dynamically adjust the difficulty of upcoming questions based on the candidate's performance.

Difficulty levels:

- Beginner
- Medium
- Advanced

This allows the system to create a more personalized interview experience.

---

### 4. Mock Interview

The application provides a structured mock interview consisting of multiple technical questions.

For every question, the candidate receives:

- Question
- Topic
- Skill
- Difficulty
- Answer input
- AI evaluation
- Score
- Performance level
- Feedback

---

### 5. Voice Answer Support

Candidates can answer interview questions using voice input.

The system converts the spoken response into text and passes the transcript to the answer evaluation pipeline.

---

### 6. Machine Learning Based Answer Evaluation

The system extracts multiple features from the candidate's answer:

- Relevance
- Correctness
- Clarity
- Confidence
- Technical Depth

These features are passed to a trained machine learning model to generate an overall answer score.

---

### 7. Performance Analysis

Each answer receives an overall score between **0 and 100**.

Performance levels include:

| Score | Performance |
|------:|-------------|
| 80–100 | Excellent |
| 65–79 | Good |
| 40–64 | Average |
| 0–39 | Needs Improvement |

---

### 8. Personalized Feedback

The system analyzes the candidate's response and provides feedback such as:

- Strengths
- Areas for improvement
- Answer quality
- Technical depth
- Relevance
- Clarity
- Confidence

This helps candidates understand how they can improve their interview responses.

---

### 9. Admin Dashboard

The project includes an administrator dashboard for viewing interview analytics.

The admin can view:

- Total interviews
- Average score
- Best score
- Performance distribution
- Score history
- Candidate interview records
- Individual interview answers
- Answer-level performance

Interview history is restricted to the administrator.

---

## Machine Learning Pipeline

The answer evaluation pipeline follows these major steps:

```text
Candidate Answer
       ↓
Text Preprocessing
       ↓
Feature Extraction
       ↓
Relevance
Correctness
Clarity
Confidence
Technical Depth
       ↓
Machine Learning Model
       ↓
Predicted Score
       ↓
Performance Level
       ↓
Personalized Feedback
