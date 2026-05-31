import streamlit as st
import sys
sys.path.insert(0, 'D:\\pip-packages')

from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io, os, base64, json
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Quicksand:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }
.stApp {
    background: linear-gradient(135deg, #e8f4fd 0%, #fce4f0 25%, #ede8fa 50%, #fdf6e3 75%, #e8f4fd 100%) !important;
    background-attachment: fixed !important;
}
.block-container {
    background: rgba(255,255,255,0.72); backdrop-filter: blur(12px);
    border-radius: 20px; padding: 2rem 2.5rem !important;
    box-shadow: 0 8px 40px rgba(130,100,180,0.10); border: 1px solid rgba(255,255,255,0.9);
}
h1 { font-family: 'Quicksand', sans-serif !important; font-weight: 800 !important;
     background: linear-gradient(90deg, #5b8dee, #c56cd6);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2rem !important; }
h2, h3 { font-family: 'Quicksand', sans-serif !important; font-weight: 700 !important; color: #5a4a8a !important; }
.stMarkdown h3 {
    background: linear-gradient(90deg, #87ceeb33, #ffb6c133, #d8b4fe33);
    border-left: 4px solid #a78bfa; border-radius: 0 10px 10px 0;
    padding: 8px 16px !important; margin: 16px 0 8px 0 !important; color: #4c3d8f !important;
}
hr { border: none; height: 2px;
     background: linear-gradient(90deg, #87ceeb, #ffb6c1, #d8b4fe, #fde68a);
     border-radius: 2px; margin: 16px 0 !important; opacity: 0.7; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    border-radius: 10px !important; border: 1.5px solid #c4b5fd !important;
    background: rgba(255,255,255,0.9) !important; font-family: 'Nunito', sans-serif !important;
    font-size: 13.5px !important; padding: 8px 12px !important;
    transition: border-color 0.2s, box-shadow 0.2s; box-shadow: 0 2px 8px rgba(167,139,250,0.08);
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #818cf8 !important; box-shadow: 0 0 0 3px rgba(129,140,248,0.18) !important;
}
.stSelectbox > div > div { border-radius: 10px !important; border: 1.5px solid #c4b5fd !important; background: rgba(255,255,255,0.9) !important; }
.stButton > button {
    border-radius: 10px !important; font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important; font-size: 13.5px !important; border: 1.5px solid #c4b5fd !important;
    background: linear-gradient(135deg, #ede9fe, #fce7f3) !important; color: #5b21b6 !important;
    transition: all 0.2s ease !important; padding: 6px 16px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ddd6fe, #fbcfe8) !important; border-color: #a78bfa !important;
    box-shadow: 0 4px 14px rgba(167,139,250,0.28) !important; transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"], button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #818cf8, #c084fc) !important; color: white !important;
    border: none !important; font-size: 15px !important; padding: 10px 24px !important;
    box-shadow: 0 4px 18px rgba(129,140,248,0.35) !important;
}
.stButton > button[kind="primary"]:hover, button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    box-shadow: 0 6px 24px rgba(129,140,248,0.45) !important; transform: translateY(-2px) !important;
}
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #eff6ff, #fdf2f8) !important; border-radius: 10px !important;
    border: 1.5px solid #e0d7ff !important; font-family: 'Quicksand', sans-serif !important;
    font-weight: 700 !important; color: #4c3d8f !important; padding: 10px 16px !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.85) !important; border: 1.5px solid #e0d7ff !important;
    border-top: none !important; border-radius: 0 0 10px 10px !important; padding: 16px !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-family: 'Nunito', sans-serif !important; font-weight: 600 !important;
    color: #5a4a8a !important; font-size: 13px !important;
}
.stCaption { color: #9370bb !important; font-style: italic; font-size: 12px !important; }
.stSuccess { border-radius: 10px !important; background: #f0fdf4 !important; border-left: 4px solid #4ade80 !important; }
.stWarning { border-radius: 10px !important; background: #fffbeb !important; border-left: 4px solid #fbbf24 !important; }
.stError   { border-radius: 10px !important; background: #fef2f2 !important; border-left: 4px solid #f87171 !important; }
.stDownloadButton > button {
    background: linear-gradient(135deg, #86efac, #67e8f9) !important; color: #065f46 !important;
    border: none !important; border-radius: 10px !important; font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important; box-shadow: 0 4px 14px rgba(110,231,183,0.35) !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #4ade80, #22d3ee) !important;
    box-shadow: 0 6px 20px rgba(110,231,183,0.45) !important; transform: translateY(-1px) !important;
}
.stSpinner > div { border-top-color: #a78bfa !important; }
div[data-testid="column"] > div:hover { transform: translateY(-2px); transition: transform 0.2s; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1e9ff; border-radius: 3px; }
::-webkit-scrollbar-thumb { background: linear-gradient(#c4b5fd, #fbcfe8); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "step": "template", "template": None, "pdf_bytes": None, "chat_history": [],
        "personal": {
            "name": "Sailaja Kalle", "phone": "+91 7207082372",
            "email": "kallesailaja83@gmail.com", "location": "Bangalore, India",
            "linkedin": "https://linkedin.com/in/sailaja-kalle",
            "github": "https://github.com/Sailaja-Kalle"
        },
        "summary": "AI Engineer with hands-on experience building production-level AI/ML projects — all live and deployed on cloud. Currently working as AI Trainee at INFOSTATS Private Limited. Passionate about building AI solutions that solve real-world problems in healthcare.",
        "skills": [
            {"category": "AI / GenAI",        "details": "LLMs (Llama 3.3, Groq, Gemini), RAG Pipelines, Prompt Engineering, Agentic AI, LangChain, LangGraph, MCP Servers"},
            {"category": "Machine Learning",   "details": "Scikit-learn, Random Forest, Decision Tree, KNN, Logistic Regression, XGBoost, PCA, Hyperparameter Tuning, Model Evaluation"},
            {"category": "NLP & Voice",        "details": "NLP Pipelines, Sentiment Analysis, NER, ChromaDB, Whisper STT, gTTS, Multilingual AI"},
            {"category": "OCR",                "details": "Tesseract, pytesseract, OpenCV, PDF2Image, Poppler"},
            {"category": "Backend / APIs",     "details": "FastAPI, REST APIs, SQLAlchemy, SQLite, PostgreSQL, Swagger, Docker"},
            {"category": "Frontend / UI",      "details": "Streamlit, Gradio, Jinja2, Interactive Dashboards, Voice UI"},
            {"category": "Cloud / DevOps",     "details": "Render, Streamlit Cloud, HuggingFace Spaces, Azure Data Factory, Microsoft Fabric"},
            {"category": "BI / Analytics",     "details": "Power BI, Tableau, Advanced Excel, MySQL, SQL Server, Data Warehousing"},
            {"category": "Programming",        "details": "Python, SQL, Git, GitHub"},
            {"category": "Dev Tools",          "details": "VS Code, Postman, Jupyter Notebook, Docker"},
        ],
        "projects": [
            {"name": "Clinical Decision Support System", "tech": "Python, FastAPI, Streamlit, Groq LLM, RandomForest, SQLite, MCP Servers",
             "status": "Live & Deployed", "links": [{"label": "Live Dashboard", "url": ""}, {"label": "GitHub", "url": ""}],
             "bullets": ["Built full-stack AI system with FastAPI backend + Streamlit dashboard for real-time patient risk assessment.",
                         "Developed 6 AI agents powered by Groq LLM for Triage, Risk, Diagnosis, Alert, Summary, and Orchestration.",
                         "Trained 5+ ML algorithms; RandomForest selected with 90% accuracy for 3-class risk prediction."]},
            {"name": "AI-Powered Multilingual Healthcare Assistant", "tech": "Python, Streamlit, Groq LLM, RAG, ChromaDB, gTTS, Whisper",
             "status": "Live", "links": [{"label": "Live App", "url": ""}, {"label": "GitHub", "url": ""}],
             "bullets": ["Built multilingual AI healthcare assistant (Telugu, English, Hindi) for rural India.",
                         "Voice input (STT) + audio output (TTS); RAG pipeline with ChromaDB.",
                         "Real-time hospital finder using OpenStreetMap API + emergency detection with 108 helpline alerts."]},
        ],
        "experience": [
            {"title": "AI & ML Trainee", "company": "INFOSTATS Private Limited, Bangalore",
             "duration": "March 2026 - Present", "cert_link": "",
             "bullets": ["Hands-on with Excel, SQL, Power BI, Python, Azure Data Factory, NLP, Machine Learning, Agentic AI, LangChain.",
                         "Built 4+ production AI/ML projects: LLM-powered agents, RAG pipelines, OCR systems, FastAPI backends."]},
            {"title": "Data Analyst Intern", "company": "AI Variant",
             "duration": "May 2025 - Feb 2026", "cert_link": "",
             "bullets": ["Built 5+ interactive sales dashboards in Power BI and Tableau.",
                         "Delivered KPI reports from 3+ real-world datasets including Adventure Works, Zomato Analytics."]},
        ],
        "education": [
            {"degree": "B.Tech CSE (6-Year Integrated)", "institution": "RGUKT - RK Valley (IIIT)", "score": "CGPA: 9.0", "year": "2021-2025", "proof_link": ""},
            {"degree": "PUC (Intermediate)",              "institution": "RGUKT - RK Valley (IIIT)", "score": "CGPA: 9.9", "year": "2019-2021", "proof_link": ""},
            {"degree": "SSC (10th Grade)",                "institution": "A.P Model School",          "score": "CGPA: 10/10","year": "2018-2019","proof_link": ""},
        ],
        "certifications": [
            {"name": "Python to GenAI Course Completion - Udemy",           "link": ""},
            {"name": "Data Analytics Course Completion - ExcelR Institute",  "link": ""},
            {"name": "Data Engineering Course Completion - PVR Cloud Tech",  "link": ""},
            {"name": "Cloud Computing - Top 5% - NPTEL",                     "link": ""},
            {"name": "Data Analytics Certificate - NASSCOM",                 "link": ""},
        ],
        "achievements": [
            {"text": "Dr. A.P.J. Abdul Kalam Vidya Puraskar (Prathibha Award) 2019 - Govt. of AP for SSC Excellence.", "link": ""}
        ],
        "declaration": "I hereby declare that all the information provided in this resume is true to the best of my knowledge and belief.",
        "decl_name": "K.Sailaja",
        "decl_place": "Bangalore",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

TEMPLATES = {
    1: {"name":"Classic Blue",    "emoji":"🔵","tag":"#1a237e","sec":"#00695c","acc":"#b71c1c","desc":"Professional dark-blue & teal - your original style"},
    2: {"name":"Modern Minimal",  "emoji":"⚫","tag":"#111111","sec":"#444444","acc":"#111111","desc":"Clean black & white - sleek, ATS-friendly"},
    3: {"name":"Creative Purple", "emoji":"🟣","tag":"#4a148c","sec":"#f9a825","acc":"#880e4f","desc":"Bold purple with gold accents - stands out"},
    4: {"name":"Executive Green", "emoji":"🟢","tag":"#1b5e20","sec":"#558b2f","acc":"#e65100","desc":"Corporate forest green - formal"},
    5: {"name":"Bold Red",        "emoji":"🔴","tag":"#b71c1c","sec":"#37474f","acc":"#c62828","desc":"Striking red & charcoal - assertive"},
}

def label_row(label, key, wtype="text", value="", placeholder="", height=80):
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"<div style='padding-top:8px;font-weight:600;font-size:13px;color:#444'>{label}</div>", unsafe_allow_html=True)
    with c2:
        if wtype == "text":
            return st.text_input("", value=value, placeholder=placeholder, key=key, label_visibility="collapsed")
        elif wtype == "textarea":
            return st.text_area("", value=value, placeholder=placeholder, key=key, height=height, label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════════════════
# PDF BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_pdf(tid):
    t  = TEMPLATES[tid]
    TC = t["tag"]; SC = t["sec"]; AC = t["acc"]
    P  = colors.HexColor(TC); S = colors.HexColor(SC); LG = colors.HexColor('#f5f5f5')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm)
    story = []

    def ps(n, **kw): return ParagraphStyle(n, **kw)

    # ALL STYLES - Helvetica-Bold throughout
    sec_s  = ps('sc', fontSize=11, fontName='Helvetica-Bold', textColor=P, spaceBefore=8, spaceAfter=2)
    body_s = ps('b',  fontSize=9,  fontName='Helvetica-Bold', leading=14, spaceAfter=3)
    bul_s  = ps('bu', fontSize=9,  fontName='Helvetica-Bold', leading=13, leftIndent=10, spaceAfter=2)
    bblu_s = ps('bb', fontSize=10, fontName='Helvetica-Bold', textColor=P, spaceAfter=1, spaceBefore=4)

    # FIXED: Technologies and Links - Helvetica-Bold, same font as entire resume
    teal_s = ps('te', fontSize=9,  fontName='Helvetica-Bold', textColor=S, spaceAfter=2)
    link_s = ps('lk', fontSize=8.5,fontName='Helvetica-Bold', textColor=P, spaceAfter=3)

    def section(title):
        story.append(Paragraph(title, sec_s))
        story.append(HRFlowable(width="100%", thickness=1, color=P, spaceAfter=4))

    p = st.session_state.personal

    # HEADER
    from reportlab.lib.enums import TA_RIGHT
    hdr_name = ps('hn', fontSize=20, fontName='Helvetica-Bold', alignment=TA_CENTER,
                  textColor=P, leading=24, spaceAfter=2, spaceBefore=0)
    hdr_tag  = ps('ht', fontSize=7.5, fontName='Helvetica-Bold', alignment=TA_CENTER,
                  textColor=P, leading=10, spaceAfter=2, spaceBefore=0)
    hdr_con  = ps('hc', fontSize=8.5, fontName='Helvetica-Bold', alignment=TA_CENTER,
                  leading=12, spaceAfter=2, spaceBefore=0)

    story.append(Paragraph(p['name'].upper(), hdr_name))
    story.append(Paragraph(
        "AI  |  Machine Learning  |  GenAI  |  NLP  |  Agentic AI  |  Data Analytics  |  Microsoft Fabric", hdr_tag))
    story.append(Paragraph(f"{p['phone']}  |  {p['email']}  |  {p['location']}", hdr_con))
    ln = p['linkedin'].replace('https://','').replace('http://','')
    gh = p['github'].replace('https://','').replace('http://','')
    story.append(Paragraph(
        f'<a href="{p["linkedin"]}" color="{TC}"><u>{ln}</u></a>'
        f'  |  '
        f'<a href="{p["github"]}"  color="{TC}"><u>{gh}</u></a>', hdr_con))
    story.append(HRFlowable(width="100%", thickness=1.5, color=P, spaceAfter=5))

    # SUMMARY
    section("PROFESSIONAL SUMMARY")
    story.append(Paragraph(st.session_state.summary, body_s))

    # SKILLS
    section("TECHNICAL SKILLS")
    skill_rows = []
    for sk in st.session_state.skills:
        if sk.get('category','').strip():
            skill_rows.append([
                Paragraph(sk['category'], ps('sk', fontSize=9, fontName='Helvetica-Bold', textColor=S, leading=13)),
                Paragraph(sk['details'],  ps('sv', fontSize=9, fontName='Helvetica-Bold', leading=13))
            ])
    if skill_rows:
        tbl = Table(skill_rows, colWidths=[3.8*cm, 14*cm])
        tbl.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),
            ('BOX',(0,0),(-1,-1),0.5,colors.grey),
            ('INNERGRID',(0,0),(-1,-1),0.25,colors.lightgrey),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white, LG]),
        ]))
        story.append(tbl)

    # PROJECTS
    section("PROJECTS")
    for i, proj in enumerate(st.session_state.projects, 1):
        if not proj.get('name','').strip(): continue

        proj_title = Paragraph(f"{i}. {proj['name']}", bblu_s)
        status_val = proj.get("status","").strip()
        if status_val:
            status_para = Paragraph(
                f'<font color="{AC}"><b>{status_val}</b></font>',
                ps('st', fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor(AC),
                   alignment=TA_RIGHT, spaceAfter=1, spaceBefore=4))
            proj_row = Table([[proj_title, status_para]], colWidths=[13.5*cm, 4.3*cm])
            proj_row.setStyle(TableStyle([
                ('VALIGN',       (0,0),(-1,-1),'MIDDLE'),
                ('ALIGN',        (1,0),(1,0),  'RIGHT'),
                ('LEFTPADDING',  (0,0),(-1,-1), 0),
                ('RIGHTPADDING', (0,0),(-1,-1), 0),
                ('TOPPADDING',   (0,0),(-1,-1), 4),
                ('BOTTOMPADDING',(0,0),(-1,-1), 1),
            ]))
            story.append(proj_row)
        else:
            story.append(proj_title)

        # FIXED: Technologies - Helvetica-Bold, matching entire resume font
        if proj.get('tech'):
            story.append(Paragraph(f"<b>Technologies :</b> {proj['tech']}", teal_s))

        # FIXED: Links - Helvetica-Bold, matching entire resume font
        valid_links = [l for l in proj.get('links',[]) if l.get('label') and l.get('url','').startswith('http')]
        if valid_links:
            parts = [f'<a href="{l["url"]}" color="{TC}"><u>{l["label"]}</u></a>' for l in valid_links]
            story.append(Paragraph("<b>Links :</b> " + " | ".join(parts), link_s))

        for b in proj.get('bullets', []):
            if b.strip():
                story.append(Paragraph(f"* {b.strip()}", bul_s))

    # EXPERIENCE
    section("WORK EXPERIENCE")
    for exp in st.session_state.experience:
        if not exp.get('title','').strip(): continue

        cert_para = Paragraph('', ps('empty', fontSize=9, fontName='Helvetica-Bold'))
        if exp.get('cert_link','').startswith('http'):
            cert_para = Paragraph(
                f'<a href="{exp["cert_link"]}" color="{TC}"><u>View Certificate</u></a>',
                ps('cert', fontSize=8.5, fontName='Helvetica-Bold', textColor=P, alignment=TA_RIGHT))

        dur_para = Paragraph(
            exp.get('duration',''),
            ps('dur', fontSize=9, fontName='Helvetica-Bold',
               textColor=colors.HexColor('#555555'), alignment=TA_RIGHT))

        title_para = Paragraph(f"{exp['title']} | {exp['company']}", bblu_s)
        right_cell = Table([[cert_para], [dur_para]], colWidths=[5.5*cm])
        right_cell.setStyle(TableStyle([
            ('ALIGN',  (0,0),(-1,-1),'RIGHT'),
            ('VALIGN', (0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',  (0,0),(-1,-1), 0),
            ('RIGHTPADDING', (0,0),(-1,-1), 0),
            ('TOPPADDING',   (0,0),(-1,-1), 0),
            ('BOTTOMPADDING',(0,0),(-1,-1), 0),
        ]))

        exp_row = Table([[title_para, right_cell]], colWidths=[12.3*cm, 5.5*cm])
        exp_row.setStyle(TableStyle([
            ('VALIGN',       (0,0),(-1,-1),'TOP'),
            ('ALIGN',        (1,0),(1,0),  'RIGHT'),
            ('LEFTPADDING',  (0,0),(-1,-1), 0),
            ('RIGHTPADDING', (0,0),(-1,-1), 0),
            ('TOPPADDING',   (0,0),(-1,-1), 4),
            ('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ]))
        story.append(exp_row)
        for b in exp.get('bullets', []):
            if b.strip():
                story.append(Paragraph(f"* {b.strip()}", bul_s))

    # EDUCATION
    section("EDUCATION")
    hps = ps('eh', fontSize=9, fontName='Helvetica-Bold', textColor=P)
    edu_rows = [[Paragraph(h, hps) for h in ['Qualification','Institution','Score','Year','Proof']]]
    for edu in st.session_state.education:
        if not edu.get('institution','').strip(): continue
        eps = ps('er', fontSize=9, fontName='Helvetica-Bold')
        proof = Paragraph(
            f'<a href="{edu["proof_link"]}" color="{TC}"><u>View</u></a>'
            if edu.get("proof_link","").startswith("http") else edu.get("proof_link",""), eps)
        edu_rows.append([
            Paragraph(edu['degree'], eps), Paragraph(edu['institution'], eps),
            Paragraph(edu['score'], eps),  Paragraph(edu['year'], eps), proof
        ])
    if len(edu_rows) > 1:
        et = Table(edu_rows, colWidths=[4.5*cm, 6*cm, 2.5*cm, 3*cm, 1.8*cm])
        et.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce6f7')),
            ('FONTSIZE',(0,0),(-1,-1),9),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),
            ('LEFTPADDING',(0,0),(-1,-1),6),
            ('BOX',(0,0),(-1,-1),0.5,colors.grey),
            ('INNERGRID',(0,0),(-1,-1),0.25,colors.lightgrey),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LG]),
        ]))
        story.append(et)

    # CERTIFICATIONS
    section("CERTIFICATIONS")
    for cert in st.session_state.certifications:
        if not cert.get('name','').strip(): continue
        name_para = Paragraph(f"* {cert['name']}", bul_s)
        if cert.get('link','').startswith('http'):
            link_para = Paragraph(
                f'<a href="{cert["link"]}" color="{TC}"><u>View Certificate</u></a>',
                ps('cl', fontSize=8.5, fontName='Helvetica-Bold', textColor=P, alignment=TA_RIGHT))
            row = Table([[name_para, link_para]], colWidths=[15*cm, 2.8*cm])
            row.setStyle(TableStyle([
                ('VALIGN',       (0,0),(-1,-1),'MIDDLE'),
                ('ALIGN',        (1,0),(1,0),  'RIGHT'),
                ('LEFTPADDING',  (0,0),(-1,-1), 0),
                ('RIGHTPADDING', (0,0),(-1,-1), 0),
                ('TOPPADDING',   (0,0),(-1,-1), 1),
                ('BOTTOMPADDING',(0,0),(-1,-1), 1),
            ]))
            story.append(row)
        else:
            story.append(name_para)

    # ACHIEVEMENTS
    section("ACHIEVEMENTS")
    for ach in st.session_state.achievements:
        text = ach.get("text","").strip() if isinstance(ach, dict) else ach.strip()
        link = ach.get("link","").strip() if isinstance(ach, dict) else ""
        if not text: continue
        name_para = Paragraph(f"* {text}", bul_s)
        if link.startswith("http"):
            link_para = Paragraph(
                f'<a href="{link}" color="{TC}"><u>View</u></a>',
                ps('al', fontSize=8.5, fontName='Helvetica-Bold', textColor=P, alignment=TA_RIGHT))
            row = Table([[name_para, link_para]], colWidths=[15*cm, 2.8*cm])
            row.setStyle(TableStyle([
                ('VALIGN',       (0,0),(-1,-1),'MIDDLE'),
                ('ALIGN',        (1,0),(1,0),  'RIGHT'),
                ('LEFTPADDING',  (0,0),(-1,-1), 0),
                ('RIGHTPADDING', (0,0),(-1,-1), 0),
                ('TOPPADDING',   (0,0),(-1,-1), 1),
                ('BOTTOMPADDING',(0,0),(-1,-1), 1),
            ]))
            story.append(row)
        else:
            story.append(name_para)

    # DECLARATION
    section("DECLARATION")
    story.append(Paragraph(f'* {st.session_state.declaration}', bul_s))
    story.append(Spacer(1, 14))

    from reportlab.lib.enums import TA_RIGHT
    story.append(Paragraph(st.session_state.decl_name,
        ps('sig', fontSize=9, fontName='Helvetica-Bold', textColor=P, alignment=TA_RIGHT)))
    story.append(Paragraph(st.session_state.decl_place,
        ps('pl',  fontSize=9, fontName='Helvetica-Bold', alignment=TA_RIGHT)))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

# ══════════════════════════════════════════════════════════════════════════════
# PDF PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
def show_pdf_preview(pdf_bytes):
    try:
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(pdf_bytes, dpi=150)
        for img in images:
            st.image(img, use_column_width=True)
    except Exception as e:
        b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" '
            f'width="100%" height="750px" style="border:1px solid #ddd;border-radius:8px;"></iframe>',
            unsafe_allow_html=True)
        st.warning(f"Preview fallback: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# AI FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def ai_enhance_summary():
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content":
                f"Enhance this resume summary to be professional and ATS-friendly. "
                f"Keep it 3-4 sentences. Return ONLY the enhanced text, nothing else.\n\n{st.session_state.summary}"}],
            max_tokens=300)
        st.session_state.summary = resp.choices[0].message.content.strip()
    except Exception as e:
        st.warning(f"AI enhancement skipped: {e}")

def ai_apply_modification(user_request):
    resume_json = {
        "personal": st.session_state.personal, "summary": st.session_state.summary,
        "skills": st.session_state.skills, "projects": st.session_state.projects,
        "experience": st.session_state.experience, "education": st.session_state.education,
        "certifications": st.session_state.certifications, "achievements": st.session_state.achievements,
        "declaration": st.session_state.declaration,
        "decl_name": st.session_state.decl_name, "decl_place": st.session_state.decl_place,
    }
    prompt = f"""You are a resume editor. The user wants this change applied to their resume:

USER REQUEST: "{user_request}"

CURRENT RESUME JSON:
{json.dumps(resume_json, indent=2)}

Apply the requested change to the resume JSON. Rules:
- Only change what the user asked. Leave everything else exactly as is.
- Keep all keys and structure identical.
- For skills, projects, experience, certifications, achievements - they are lists; keep the list structure.
- Return ONLY the updated JSON, no explanation, no markdown fences.
"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000)
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    updated = json.loads(raw)
    for key in ["personal","summary","skills","projects","experience",
                "education","certifications","achievements","declaration","decl_name","decl_place"]:
        if key in updated:
            st.session_state[key] = updated[key]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TEMPLATE SELECTION
# ══════════════════════════════════════════════════════════════════════════════
def page_template():
    st.title("📄 AI Resume Builder")
    st.subheader("Step 1 - Choose Your Resume Template")
    st.divider()
    cols = st.columns(5)
    for i, (tid, t) in enumerate(TEMPLATES.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="border:2px solid {t['tag']};border-radius:10px;padding:12px;background:#fff;min-height:190px;">
              <div style="background:{t['tag']};color:white;padding:7px;border-radius:5px;font-size:11px;
                          font-weight:bold;text-align:center;margin-bottom:10px;">{t['name'].upper()}</div>
              <div style="background:{t['tag']}33;height:8px;border-radius:3px;margin:5px 0;"></div>
              <div style="background:{t['sec']}44;height:5px;border-radius:3px;margin:4px 0;width:80%;"></div>
              <div style="background:{t['tag']}18;height:4px;border-radius:3px;margin:4px 0;width:60%;"></div>
              <div style="background:{t['sec']}25;height:4px;border-radius:3px;margin:6px 0;"></div>
              <div style="background:{t['tag']}18;height:3px;border-radius:3px;margin:3px 0;width:90%;"></div>
              <div style="background:{t['tag']}18;height:3px;border-radius:3px;margin:3px 0;width:70%;"></div>
              <div style="margin-top:8px;font-size:9px;color:#777;text-align:center;">{t['desc']}</div>
            </div>""", unsafe_allow_html=True)
            st.write("")
            if st.button(f"{t['emoji']} Select", key=f"tpl_{tid}", use_container_width=True):
                st.session_state.template = tid
                st.session_state.step = "form"
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FORM
# ══════════════════════════════════════════════════════════════════════════════
def page_form():
    t = TEMPLATES[st.session_state.template]
    st.title(f"📄 AI Resume Builder - {t['emoji']} {t['name']}")
    if st.button("← Change Template"):
        st.session_state.step = "template"; st.rerun()
    st.divider()

    st.markdown("### 👤 Personal Information")
    p = st.session_state.personal
    c1, c2 = st.columns(2)
    with c1:
        name     = label_row("Full Name",   "p_name",    value=p.get("name",""))
        phone    = label_row("Phone",       "p_phone",   value=p.get("phone",""))
        email    = label_row("Email",       "p_email",   value=p.get("email",""))
    with c2:
        location = label_row("Location",    "p_loc",     value=p.get("location",""))
        linkedin = label_row("LinkedIn URL","p_linkedin", value=p.get("linkedin",""))
        github   = label_row("GitHub URL",  "p_github",  value=p.get("github",""))
    st.divider()

    st.markdown("### 📝 Professional Summary")
    summary = label_row("Summary", "p_summary", wtype="textarea", height=100, value=st.session_state.summary)
    st.divider()

    st.markdown("### 🛠️ Technical Skills")
    st.caption("Left = Skill Category name | Right = Skills (comma separated)")
    skills_data = st.session_state.skills
    for i, sk in enumerate(skills_data):
        c1, c2, c3 = st.columns([2, 4, 0.4])
        with c1:
            skills_data[i]["category"] = st.text_input("Category", value=sk.get("category",""),
                key=f"sk_cat_{i}", placeholder="e.g. AI / GenAI")
        with c2:
            skills_data[i]["details"] = st.text_input("Skills", value=sk.get("details",""),
                key=f"sk_det_{i}", placeholder="e.g. Python, FastAPI, LLMs...")
        with c3:
            st.write(""); st.write("")
            if st.button("🗑️", key=f"sk_del_{i}") and len(skills_data) > 1:
                skills_data.pop(i); st.rerun()
    if st.button("➕ Add Skill Category"):
        skills_data.append({"category":"","details":""}); st.rerun()
    st.divider()

    st.markdown("### 🚀 Projects")
    projects_data = st.session_state.projects
    for i, proj in enumerate(projects_data):
        with st.expander(f"Project {i+1}: {proj.get('name','') or 'New Project'}", expanded=(i==0)):
            c1, c2 = st.columns(2)
            with c1:
                projects_data[i]["name"] = label_row("Project Name", f"pr_name_{i}",
                    value=proj.get("name",""), placeholder="e.g. Clinical Decision Support System")
                projects_data[i]["tech"] = label_row("Technologies", f"pr_tech_{i}",
                    value=proj.get("tech",""), placeholder="e.g. Python, FastAPI, Groq LLM")
            with c2:
                status_opts = ["Live & Deployed","Live","In Progress","Completed",""]
                cur = proj.get("status","Live")
                projects_data[i]["status"] = st.selectbox("Status", status_opts,
                    index=status_opts.index(cur) if cur in status_opts else 1, key=f"pr_status_{i}")

            st.markdown("**🔗 Project Links**")
            links = proj.get("links", [{"label":"","url":""}])
            for j, lnk in enumerate(links):
                lc1, lc2, lc3 = st.columns([2, 3, 0.4])
                with lc1:
                    links[j]["label"] = st.text_input("Link Name", value=lnk.get("label",""),
                        key=f"pr_ln_{i}_{j}", placeholder="e.g. Live Dashboard")
                with lc2:
                    links[j]["url"] = st.text_input("URL", value=lnk.get("url",""),
                        key=f"pr_lu_{i}_{j}", placeholder="https://...")
                with lc3:
                    st.write(""); st.write("")
                    if st.button("🗑️", key=f"pr_ld_{i}_{j}") and len(links) > 1:
                        links.pop(j); st.rerun()
            if st.button("➕ Add Link", key=f"pr_la_{i}"):
                links.append({"label":"","url":""}); st.rerun()
            projects_data[i]["links"] = links

            st.markdown("**📝 Description Bullets**")
            bullets = proj.get("bullets", [""])
            for j, b in enumerate(bullets):
                bc1, bc2 = st.columns([6, 0.4])
                with bc1:
                    bullets[j] = st.text_input(f"Point {j+1}", value=b,
                        key=f"pr_b_{i}_{j}", placeholder="Describe what you built/achieved...")
                with bc2:
                    st.write(""); st.write("")
                    if st.button("🗑️", key=f"pr_bd_{i}_{j}") and len(bullets) > 1:
                        bullets.pop(j); st.rerun()
            if st.button("➕ Add Bullet", key=f"pr_ba_{i}"):
                bullets.append(""); st.rerun()
            projects_data[i]["bullets"] = bullets

            if st.button(f"🗑️ Remove Project {i+1}", key=f"pr_del_{i}") and len(projects_data) > 1:
                projects_data.pop(i); st.rerun()
    if st.button("➕ Add Another Project"):
        projects_data.append({"name":"","tech":"","status":"Live",
                               "links":[{"label":"","url":""}],"bullets":[""]}); st.rerun()
    st.divider()

    st.markdown("### 💼 Work Experience")
    exp_data = st.session_state.experience
    for i, exp in enumerate(exp_data):
        with st.expander(f"Experience {i+1}: {exp.get('title','') or 'New'}", expanded=(i==0)):
            c1, c2 = st.columns(2)
            with c1:
                exp_data[i]["title"]     = label_row("Job Title",        f"ex_t_{i}",  value=exp.get("title",""),    placeholder="e.g. AI & ML Trainee")
                exp_data[i]["company"]   = label_row("Company",          f"ex_c_{i}",  value=exp.get("company",""),  placeholder="e.g. INFOSTATS Pvt Ltd, Bangalore")
            with c2:
                exp_data[i]["duration"]  = label_row("Duration",         f"ex_d_{i}",  value=exp.get("duration",""), placeholder="e.g. March 2026 - Present")
                exp_data[i]["cert_link"] = label_row("Certificate Link", f"ex_cl_{i}", value=exp.get("cert_link",""),placeholder="https://certificate.com")

            st.markdown("**📝 Description Bullets**")
            bullets = exp.get("bullets", [""])
            for j, b in enumerate(bullets):
                bc1, bc2 = st.columns([6, 0.4])
                with bc1:
                    bullets[j] = st.text_input(f"Point {j+1}", value=b,
                        key=f"ex_b_{i}_{j}", placeholder="Describe your responsibilities...")
                with bc2:
                    st.write(""); st.write("")
                    if st.button("🗑️", key=f"ex_bd_{i}_{j}") and len(bullets) > 1:
                        bullets.pop(j); st.rerun()
            if st.button("➕ Add Bullet", key=f"ex_ba_{i}"):
                bullets.append(""); st.rerun()
            exp_data[i]["bullets"] = bullets

            if st.button(f"🗑️ Remove Experience {i+1}", key=f"ex_del_{i}") and len(exp_data) > 1:
                exp_data.pop(i); st.rerun()
    if st.button("➕ Add Another Experience"):
        exp_data.append({"title":"","company":"","duration":"","cert_link":"","bullets":[""]}); st.rerun()
    st.divider()

    st.markdown("### 🎓 Education")
    edu_data = st.session_state.education
    EDU_LABELS = ["SSC (10th)","Intermediate / PUC","Degree / B.Tech"]
    for i, edu in enumerate(edu_data):
        lbl = EDU_LABELS[i] if i < len(EDU_LABELS) else f"Education {i+1}"
        with st.expander(f"{lbl}: {edu.get('institution','') or 'Add Details'}", expanded=(i==0)):
            c1, c2 = st.columns(2)
            with c1:
                edu_data[i]["degree"]      = label_row("Qualification", f"ed_dg_{i}", value=edu.get("degree",""),      placeholder="e.g. B.Tech CSE")
                edu_data[i]["institution"] = label_row("Institution",   f"ed_in_{i}", value=edu.get("institution",""), placeholder="e.g. RGUKT - RK Valley")
            with c2:
                edu_data[i]["score"]       = label_row("Score / CGPA",  f"ed_sc_{i}", value=edu.get("score",""),       placeholder="e.g. CGPA: 9.0")
                edu_data[i]["year"]        = label_row("Year",           f"ed_yr_{i}", value=edu.get("year",""),        placeholder="e.g. 2021-2025")
            edu_data[i]["proof_link"]      = label_row("Proof Link",     f"ed_pl_{i}", value=edu.get("proof_link",""), placeholder="https://certificate.com")
            if st.button("🗑️ Remove", key=f"ed_del_{i}") and len(edu_data) > 1:
                edu_data.pop(i); st.rerun()
    if st.button("➕ Add Education"):
        edu_data.append({"degree":"","institution":"","score":"","year":"","proof_link":""}); st.rerun()
    st.divider()

    st.markdown("### 🏆 Certifications")
    cert_data = st.session_state.certifications
    for i, cert in enumerate(cert_data):
        c1, c2, c3 = st.columns([3, 3, 0.4])
        with c1:
            cert_data[i]["name"] = st.text_input("Certificate Name", value=cert.get("name",""),
                key=f"ce_n_{i}", placeholder="e.g. Python to GenAI - Udemy")
        with c2:
            cert_data[i]["link"] = st.text_input("Certificate URL", value=cert.get("link",""),
                key=f"ce_l_{i}", placeholder="https://certificate.com")
        with c3:
            st.write(""); st.write("")
            if st.button("🗑️", key=f"ce_del_{i}") and len(cert_data) > 1:
                cert_data.pop(i); st.rerun()
    if st.button("➕ Add Certificate"):
        cert_data.append({"name":"","link":""}); st.rerun()
    st.divider()

    st.markdown("### 🏅 Achievements")
    ach_data = st.session_state.achievements
    ach_data = [{"text": a, "link":""} if isinstance(a, str) else a for a in ach_data]
    st.session_state.achievements = ach_data
    for i, ach in enumerate(ach_data):
        c1, c2, c3 = st.columns([3, 3, 0.4])
        with c1:
            ach_data[i]["text"] = st.text_input(f"Achievement {i+1}", value=ach.get("text",""),
                key=f"ach_t_{i}", placeholder="e.g. Dr. APJ Kalam Vidya Puraskar 2019")
        with c2:
            ach_data[i]["link"] = st.text_input("Proof Link", value=ach.get("link",""),
                key=f"ach_l_{i}", placeholder="https://certificate.com")
        with c3:
            st.write(""); st.write("")
            if st.button("🗑️", key=f"ach_del_{i}") and len(ach_data) > 1:
                ach_data.pop(i); st.rerun()
    if st.button("➕ Add Achievement"):
        ach_data.append({"text":"","link":""}); st.rerun()
    st.divider()

    st.markdown("### 📜 Declaration")
    decl_text = label_row("Declaration", "w_decl_text", wtype="textarea", height=70,
        value=st.session_state.declaration)
    _, dc1, dc2 = st.columns([2, 1, 1])
    with dc1:
        decl_name  = label_row("Name",  "w_decl_name",  value=st.session_state.decl_name)
    with dc2:
        decl_place = label_row("Place", "w_decl_place", value=st.session_state.decl_place)
    st.divider()

    if st.button("🚀 Generate My Resume", use_container_width=True, type="primary"):
        st.session_state.personal       = {"name":name,"phone":phone,"email":email,
                                            "location":location,"linkedin":linkedin,"github":github}
        st.session_state.summary        = summary
        st.session_state.skills         = skills_data
        st.session_state.projects       = projects_data
        st.session_state.experience     = exp_data
        st.session_state.education      = edu_data
        st.session_state.certifications = cert_data
        st.session_state.achievements   = ach_data
        st.session_state.declaration    = decl_text
        st.session_state.decl_name      = decl_name
        st.session_state.decl_place     = decl_place
        st.session_state.chat_history   = []
        st.session_state.step           = "generating"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: GENERATING
# ══════════════════════════════════════════════════════════════════════════════
def page_generating():
    st.title("📄 AI Resume Builder")
    with st.spinner("🤖 AI is enhancing your summary..."):
        ai_enhance_summary()
    with st.spinner("📄 Building PDF..."):
        st.session_state.pdf_bytes = build_pdf(st.session_state.template)
    st.session_state.step = "preview"
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
def page_preview():
    t = TEMPLATES[st.session_state.template]
    st.title(f"📄 Resume Preview - {t['emoji']} {t['name']}")

    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.session_state.personal.get("name","Resume").replace(" ","_")
        st.download_button("📥 Download PDF", data=st.session_state.pdf_bytes,
            file_name=f"{name}_Resume.pdf", mime="application/pdf", use_container_width=True)
    with c2:
        if st.button("✏️ Edit Details", use_container_width=True):
            st.session_state.step = "form"; st.rerun()
    with c3:
        if st.button("🔄 Start Over", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            init_state(); st.rerun()

    st.divider()

    left, right = st.columns([1, 1.6])

    with left:
        st.subheader("🤖 AI Resume Assistant")
        st.caption("Ask AI to change anything - summary, skills, projects, experience, etc.")
        st.caption("**Examples:**")
        st.markdown("""
- *"Make the summary shorter and more focused on healthcare AI"*
- *"Add Docker and Kubernetes to Cloud/DevOps skills"*
- *"Add a bullet point to project 1 about deployment on Azure"*
- *"Change my phone number to +91 9999999999"*
- *"Add a new certification: AWS Cloud Practitioner"*
- *"Make all project bullets more professional and ATS-friendly"*
""")
        st.divider()

        chat = st.session_state.chat_history
        for msg in chat:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")
        st.divider()

        user_input = st.text_area("Type your change request:", height=100,
            placeholder="e.g. Add Kubernetes to Cloud/DevOps skills...",
            key="mod_input")

        if st.button("Apply Change & Update Preview", use_container_width=True, type="primary"):
            if user_input.strip():
                with st.spinner("🤖 AI is applying your changes..."):
                    try:
                        ai_apply_modification(user_input.strip())
                        st.session_state.pdf_bytes = build_pdf(st.session_state.template)
                        st.session_state.chat_history.append({"role":"user",    "content": user_input.strip()})
                        st.session_state.chat_history.append({"role":"assistant","content": "Done! Changes applied and PDF updated."})
                        st.rerun()
                    except json.JSONDecodeError:
                        st.error("AI returned invalid format. Try rephrasing your request.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please type what you want to change.")

        if chat and st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []; st.rerun()

    with right:
        st.subheader("📄 Live Preview")
        st.caption("Updates every time you apply a change.")
        show_pdf_preview(st.session_state.pdf_bytes)

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
step = st.session_state.step
if   step == "template":   page_template()
elif step == "form":       page_form()
elif step == "generating": page_generating()
elif step == "preview":    page_preview()