import io

import speech_recognition as sr
import streamlit as st
from streamlit_mic_recorder import mic_recorder


def record_voice_answer():
    """
    Record the candidate's voice using the browser microphone.

    Returns:
        str: Transcribed speech
        None: If no recording was made
    """

    st.markdown(
        "### 🎙️ Speak Your Answer"
    )

    st.caption(
        "Click the microphone, speak clearly, "
        "then stop recording."
    )

    audio = mic_recorder(
        start_prompt="🎙️ Start Speaking",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="voice_answer"
    )

    if audio is None:
        return None

    audio_bytes = audio["bytes"]

    try:

        recognizer = sr.Recognizer()

        audio_file = io.BytesIO(
            audio_bytes
        )

        with sr.AudioFile(
            audio_file
        ) as source:

            recorded_audio = (
                recognizer.record(source)
            )

        text = recognizer.recognize_google(
            recorded_audio,
            language="en-IN"
        )

        return text

    except sr.UnknownValueError:

        st.warning(
            "I could not understand the audio. "
            "Please speak clearly and try again."
        )

        return None

    except sr.RequestError:

        st.error(
            "Speech recognition service is "
            "currently unavailable."
        )

        return None

    except Exception as e:

        st.error(
            f"Voice processing failed: {e}"
        )

        return None


def speak_text(text):
    """
    Make the browser speak the interview question.
    """

    safe_text = (
        str(text)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("\n", " ")
    )

    html = f"""
    <script>

    const text = `{safe_text}`;

    if ("speechSynthesis" in window) {{

        window.speechSynthesis.cancel();

        const utterance =
            new SpeechSynthesisUtterance(text);

        utterance.rate = 0.95;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        window.speechSynthesis.speak(
            utterance
        );
    }}

    </script>
    """

    st.components.v1.html(
        html,
        height=0
    )