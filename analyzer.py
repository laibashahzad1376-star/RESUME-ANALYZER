import streamlit as st
import PyPDF2
import re

# -----------------------------
# Important Skills List
# -----------------------------
IMPORTANT_SKILLS = [
    "python", "machine learning", "data analysis",
    "sql", "excel", "communication",
    "teamwork", "problem solving",
    "leadership", "project management"
]

# -----------------------------
# Extract Text from PDF
# -----------------------------
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

# -----------------------------
# Extract Text from TXT
# -----------------------------
def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# -----------------------------
# Clean Text
# -----------------------------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

# -----------------------------
# Analyze Resume
# -----------------------------
def analyze_resume(file):

    if file.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file)
    elif file.name.endswith(".txt"):
        raw_text = extract_text_from_txt(file)
    else:
        return None

    cleaned_text = clean_text(raw_text)

    detected = []
    missing = []

    for skill in IMPORTANT_SKILLS:
        if skill in cleaned_text:
            detected.append(skill)
        else:
            missing.append(skill)

    # Score Calculation
    skill_score = (len(detected) / len(IMPORTANT_SKILLS)) * 70
    word_count = len(cleaned_text.split())

    if 300 <= word_count <= 800:
        length_score = 30
    elif word_count < 300:
        length_score = 15
    else:
        length_score = 20

    final_score = round(min(skill_score + length_score, 100), 2)

    return final_score, detected, missing


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Professional AI Resume Analyzer")
st.write("Upload your Resume (PDF or TXT) to analyze skills and get a strength score.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

if uploaded_file is not None:

    result = analyze_resume(uploaded_file)

    if result is None:
        st.error("Unsupported file format.")
    else:
        score, detected_skills, missing_skills = result

        st.subheader("Resume Strength Score")
        st.success(f"{score}/100")

        st.subheader("Detected Skills")
        if detected_skills:
            st.write(", ".join(detected_skills))
        else:
            st.write("No important skills detected.")

        st.subheader("Missing Important Skills")
        st.write(", ".join(missing_skills))
