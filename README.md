# 📄 AI Resume Builder

An intelligent resume builder powered by **Groq LLM (Llama 3.3)** with live PDF preview, multiple color templates, and AI-powered modifications — built with Streamlit and ReportLab.

🌐 **Live App:** [Click here to try it](https://smart-resume-builder-ai.streamlit.app)

---

## ✨ Features

- 🎨 **5 Professional Templates** — Classic Blue, Modern Minimal, Creative Purple, Executive Green, Bold Red
- 🤖 **AI Summary Enhancement** — Groq LLM auto-enhances your summary to be ATS-friendly on generate
- 💬 **AI Chat Modifications** — Ask AI to change ANY field: skills, projects, experience, certifications, and more
- 📄 **Live PDF Preview** — See your resume update in real-time inside the browser
- 🔗 **Clickable Links** — LinkedIn, GitHub, project demos, certificates all embedded as live links
- 📥 **Instant PDF Download** — One click to download your resume
- 🏆 Sections: Summary, Skills, Projects, Experience, Education, Certifications, Achievements, Declaration
- 🌈 **Beautiful Pastel UI** — Sky blue, pink, purple, yellow gradient theme

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI framework |
| ReportLab | PDF generation |
| Groq API (Llama 3.3) | AI enhancements and modifications |
| python-dotenv | Environment variable management |

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Sailaja-Kalle/ai-resume-builder.git
cd ai-resume-builder
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at: https://console.groq.com

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Fork this repo
2. Go to https://share.streamlit.io
3. Connect your GitHub and select this repo
4. Under Advanced Settings → Secrets, add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
5. Click Deploy — done!

---

## 📸 How It Works

1. **Choose a template** from 5 color themes
2. **Fill in your details** — personal info, skills, projects, experience, education
3. **Click Generate** — AI enhances your summary automatically
4. **Chat with AI** to modify anything: "Add Docker to skills", "Make bullets more ATS-friendly"
5. **Download PDF** instantly

---

## 🤖 AI Modification Examples

You can ask the AI assistant things like:
- "Make the summary shorter and focused on healthcare AI"
- "Add Docker and Kubernetes to Cloud/DevOps skills"
- "Add a new bullet to project 1 about deployment"
- "Add a new certification: AWS Cloud Practitioner"
- "Make all project bullets more professional"

---

## 📁 Project Structure

```
ai-resume-builder/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── .streamlit/
    └── config.toml     # Streamlit configuration
```

---

## 👩‍💻 Built By

**Sailaja Kalle** — AI Engineer
- LinkedIn: https://linkedin.com/in/sailaja-kalle
- GitHub: https://github.com/Sailaja-Kalle

---


