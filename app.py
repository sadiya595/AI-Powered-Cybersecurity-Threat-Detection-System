import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------
# Session State
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# UI CONFIG
# -------------------------------
st.set_page_config(page_title="AI Threat Detection Dashboard", layout="wide")

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ffffff;
}
.card {
    padding: 20px;
    border-radius: 10px;
    background-color: #1e1e1e;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    margin-bottom: 15px;
}
.badge {
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: bold;
    color: white;
    display: inline-block;
}
.low { background-color: #2ecc71; }
.medium { background-color: #f1c40f; color: black; }
.high { background-color: #e67e22; }
.critical { background-color: #e74c3c; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Helper Functions
# -------------------------------


def get_badge(level):
    level = level.lower()
    if level == "low":
        return '<span class="badge low">Low</span>'
    elif level == "medium":
        return '<span class="badge medium">Medium</span>'
    elif level == "high":
        return '<span class="badge high">High</span>'
    elif level == "critical":
        return '<span class="badge critical">Critical</span>'
    else:
        return '<span class="badge">Unknown</span>'


def extract_threat_level(response_text):
    levels = ["Low", "Medium", "High", "Critical"]
    for level in levels:
        if level.lower() in response_text.lower():
            return level
    return "Unknown"


def confidence_score(level):
    mapping = {
        "Low": 25,
        "Medium": 50,
        "High": 75,
        "Critical": 95,
        "Unknown": 10
    }
    return mapping.get(level, 10)


def analyze_threats(text_input):
    system_prompt = """
    You are a cybersecurity threat detection assistant.

    Analyze the input and classify it into:
    - Phishing
    - Malware
    - Ransomware
    - Insider Threat
    - Benign
    - Suspicious

    Also provide:
    - Threat Level: Low / Medium / High / Critical
    - Reasoning
    - Indicators of compromise
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_input}
        ],
        temperature=0.3,
        max_completion_tokens=1024,
        top_p=0.9,
        stream=False
    )

    return completion.choices[0].message.content


def generate_pdf(input_text, result_text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica", 10)
    c.drawString(30, 750, "AI Threat Detection Report")

    text_object = c.beginText(30, 720)
    text_object.textLine("Input:")
    text_object.textLines(input_text)
    text_object.textLine("\nAnalysis:")
    text_object.textLines(result_text)

    c.drawText(text_object)
    c.save()

    buffer.seek(0)
    return buffer


# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "History", "About"])

# -------------------------------
# DASHBOARD PAGE
# -------------------------------
if page == "Dashboard":
    st.title("🛡️ AI Threat Detection Dashboard")

    user_input = st.text_area("Enter suspicious text or email:", height=150)

    col1, col2 = st.columns(2)

    with col1:
        analyze_btn = st.button("🚨 Analyze")

    with col2:
        clear_btn = st.button("🧹 Clear History")

    if clear_btn:
        st.session_state.history = []
        st.success("History cleared")

    if analyze_btn and user_input.strip():
        with st.spinner("Analyzing..."):
            result = analyze_threats(user_input)

        threat_level = extract_threat_level(result)
        score = confidence_score(threat_level)

        st.session_state.history.append({
            "Input": user_input,
            "Threat Level": threat_level,
            "Score": score
        })

        badge = get_badge(threat_level)

        st.markdown("## 🔍 Result")

        st.markdown(f"""
        <div class="card">
            <h4>Threat Level: {badge}</h4>
            <p><b>Confidence Score:</b> {score}%</p>
            <progress value="{score}" max="100" style="width:100%"></progress>
            <pre style="white-space: pre-wrap; color: #ddd;">{result}</pre>
        </div>
        """, unsafe_allow_html=True)

        pdf_file = generate_pdf(user_input, result)
        st.download_button("📄 Download Report", pdf_file,
                           file_name="threat_report.pdf")

    # Chart
    st.subheader("📊 Threat Distribution")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.bar_chart(df["Threat Level"].value_counts())
    else:
        st.info("No data yet")

# -------------------------------
# HISTORY PAGE
# -------------------------------
elif page == "History":
    st.title("📜 Analysis History")

    if st.session_state.history:
        for item in st.session_state.history:
            badge = get_badge(item["Threat Level"])
            st.markdown(f"""
            <div class="card">
                <b>Input:</b><br>{item['Input']}<br><br>
                <b>Threat Level:</b> {badge}<br>
                <b>Score:</b> {item['Score']}%
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No history available")

# -------------------------------
# ABOUT PAGE
# -------------------------------
elif page == "About":
    st.title("ℹ️ About This Project")
    st.markdown("""
    This AI-powered cybersecurity dashboard:
    - Detects phishing, malware, ransomware, and insider threats
    - Uses Groq LLM for analysis
    - Provides confidence scoring
    - Maintains session-based threat history
    - Visualizes threat distribution
    - Generates downloadable PDF reports
    """)
