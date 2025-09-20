import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from PIL import Image
import tempfile
import os

# -------------------------------
# Live Video Lecture
# -------------------------------
st.title("😎 ISMART CLASSROOM")

st.subheader("Live Video Lecture")
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Optionally: low-bandwidth transformations can be applied here
        return frame

webrtc_streamer(key="lecture", video_processor_factory=VideoTransformer)

# -------------------------------
# Slide Upload & Display
# -------------------------------
st.subheader("Lecture Slides")
slide_file = st.file_uploader("Upload slides (images or PDF pages as images)", type=["png", "jpg", "jpeg"])

if slide_file:
    image = Image.open(slide_file)
    st.image(image, caption="Lecture Slide", use_column_width=True)

# -------------------------------
# Audio Lecture Playback
# -------------------------------
st.subheader("Audio Lecture")
audio_file = st.file_uploader("Upload audio file (mp3/wav)", type=["mp3", "wav"])
if audio_file:
    st.audio(audio_file, format="audio/mp3")

# -------------------------------
# Interactive Quiz
# -------------------------------
st.subheader("Interactive Quiz")

# Teacher posts a quiz
with st.expander("Teacher: Post a Quiz"):
    quiz_question = st.text_input("Enter quiz question")
    quiz_option1 = st.text_input("Option 1")
    quiz_option2 = st.text_input("Option 2")
    quiz_option3 = st.text_input("Option 3")
    quiz_option4 = st.text_input("Option 4")
    correct_option = st.selectbox("Select correct option", ["Option 1", "Option 2", "Option 3", "Option 4"])
    
    if st.button("Post Quiz"):
        if all([quiz_question, quiz_option1, quiz_option2, quiz_option3, quiz_option4]):
            st.session_state['quiz'] = {
                "question": quiz_question,
                "options": [quiz_option1, quiz_option2, quiz_option3, quiz_option4],
                "answer": correct_option
            }
            st.success("Quiz posted successfully!")
        else:
            st.error("Please fill in all fields.")

# Student attempts the quiz
if 'quiz' in st.session_state:
    st.subheader("Student: Attempt Quiz")
    st.markdown(f"**Question:** {st.session_state['quiz']['question']}")
    
    student_answer = st.radio(
        "Select your answer:",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        format_func=lambda x: st.session_state['quiz']['options'][int(x.split()[-1]) - 1]
    )
    
    if st.button("Submit Answer"):
        correct_idx = int(st.session_state['quiz']['answer'].split()[-1]) - 1
        if student_answer == f"Option {correct_idx + 1}":
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer: {st.session_state['quiz']['options'][correct_idx]}")
