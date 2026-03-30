# 🛡️ AI-Powered Cybersecurity Threat Detection System

An intelligent cybersecurity dashboard built using Streamlit that leverages AI to detect and analyze potential threats such as deepfakes and suspicious inputs in real-time. The system provides a modern interface for monitoring, analyzing, and evaluating cybersecurity threats using AI-powered insights.

---

## 🚀 Features

- 🔍 Threat detection and analysis interface
- 🤖 AI-powered evaluation using LLMs (Groq API)
- 📊 Interactive and responsive dashboard UI
- ⚡ Real-time input processing and feedback
- 🎯 Modular and scalable architecture
- 🔐 Focus on cybersecurity use cases including deepfake detection

---

## 🧠 Tech Stack

- **Frontend/UI:** Streamlit
- **Backend:** Python
- **AI Integration:** Groq API (LLM-based inference)
- **Environment Management:** python-dotenv
- **Data Processing:** Pandas, NumPy

---

## 📁 Project Structure

AI-Powered-Cybersecurity-Threat-Detection-System/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── models/
├── utils/
└── assets/

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sadiya595/AI-Powered-Cybersecurity-Threat-Detection-System.git
cd AI-Powered-Cybersecurity-Threat-Detection-System

2. Create Virtual Environment
python -m venv venv
3. Activate Virtual Environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the root directory and add your API key:

GROQ_API_KEY=your_api_key_here
▶️ Run the Application
streamlit run app.py

Then open your browser and go to:

http://localhost:8501
🌐 Deployment

This application can be deployed for free using:

Streamlit Cloud
Render
Railway
Hugging Face Spaces
📌 Notes
Do not upload .env file to GitHub
Ensure venv/ is excluded via .gitignore
Keep API keys secure and private
Update requirements.txt when adding new dependencies
🛠️ Future Improvements
Integration of deep learning models for image/video deepfake detection
User authentication and role-based access
Database logging for threat history
Enhanced analytics and visualization dashboard
REST API version of the system
👩‍💻 Author

Sadiya Noor
GitHub: https://github.com/sadiya595
```
