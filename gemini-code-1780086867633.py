import streamlit as st
import json, re, requests, random

st.set_page_config(
    page_title="AI Interview Master",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = ""

# ── 1. PREMIUM STYLING ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243E 100%); min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1rem 3rem; max-width: 480px; margin: auto; }

.stButton > button {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  border-radius: 16px !important;
  transition: all 0.2s ease !important;
  height: auto !important;
  padding: 1.2rem 1rem !important;
  width: 100% !important;
}
.stButton > button p { font-size: 1.05rem !important; margin: 0 !important; }
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
  border: 2px solid rgba(102,126,234,0.6) !important;
  box-shadow: 0 8px 32px rgba(102,126,234,0.4) !important;
  font-weight: 700 !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 40px rgba(102,126,234,0.6) !important;
}
.stButton > button[kind="secondary"] {
  background: rgba(0, 0, 0, 0.2) !important;
  color: rgba(255,255,255,0.9) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  backdrop-filter: blur(10px) !important;
  font-weight: 500 !important;
}
.stButton > button[kind="secondary"]:hover {
  background: rgba(255,255,255,0.1) !important;
  border-color: rgba(102,126,234,0.5) !important;
  color: white !important;
}

/* ── FIXED TEXT AREA CSS TO PREVENT WHITE BOX ERROR ── */
.stTextArea textarea, .stTextArea div[data-baseweb="textarea"], .stTextArea div[data-baseweb="base-input"] {
    background-color: rgba(0, 0, 0, 0.3) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border-radius: 16px !important;
}
.stTextArea div[data-baseweb="textarea"] {
    border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
    padding: 2px !important;
}
.stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.4) !important;
    -webkit-text-fill-color: rgba(255,255,255,0.4) !important;
}
.stTextArea div[data-baseweb="base-input"]:focus-within {
    border-color: rgba(102,126,234,0.9) !important;
    box-shadow: 0 0 0 2px rgba(102,126,234,0.3) !important;
    background-color: rgba(0, 0, 0, 0.5) !important;
}

div[data-testid="stExpander"] {
    background: rgba(0, 0, 0, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 16px !important;
    margin-bottom: 1rem !important;
}
div[data-testid="stExpander"] summary { background: rgba(255, 255, 255, 0.05) !important; border-radius: 16px !important; }
div[data-testid="stExpander"] summary p { color: #ffffff !important; font-weight: 600 !important; }
div[data-testid="stExpander"] div[role="region"] { color: rgba(255,255,255,0.85) !important; padding: 1rem !important; }

.rp-head { font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 1rem; letter-spacing: 0.02em; }
.rp-row { display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
.rp-row:last-child { border-bottom: none; padding-bottom: 0; }
.rp-name { font-size: 0.95rem; font-weight: 700; color: #ffffff; }
.rp-mode { font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 3px; }
.rp-score { font-size: 1.1rem; font-weight: 800; color: #4ade80; text-align: right; }
.rp-time { font-size: 0.75rem; color: rgba(255,255,255,0.4); text-align: right; margin-top: 2px; }

.gcard { background: rgba(0,0,0,0.15); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.12); border-radius: 24px; padding: 1.3rem 1.4rem; margin-bottom: 1rem; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(102,126,234,0.2); border: 1px solid rgba(102,126,234,0.4); color: #a5b4fc; font-size: 0.78rem; font-weight: 600; padding: 5px 14px; border-radius: 20px; margin-bottom: 1rem; letter-spacing: 0.05em; text-transform: uppercase; }
.hero-title { font-size: 2.1rem; font-weight: 800; color: white; line-height: 1.2; margin-bottom: 0.4rem; letter-spacing: -0.02em; }
.hero-title span { background: linear-gradient(135deg,#a5b4fc,#f9a8d4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-sub { font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 1.5rem; }
.score-hero { display: flex; align-items: center; justify-content: space-between; }
.score-big { font-size: 3rem; font-weight: 800; color: white; }
.score-pct { font-size: 1rem; color: rgba(255,255,255,0.5); }
.score-badge-icon { width: 56px; height: 56px; border-radius: 18px; background: linear-gradient(135deg,#667eea,#764ba2); display: flex; align-items: center; justify-content: center; font-size: 1.6rem; box-shadow: 0 8px 24px rgba(102,126,234,0.5); }
.pb-bg { background: rgba(255,255,255,0.1); border-radius: 8px; height: 6px; margin-top: 12px; }
.pb-fill { background: linear-gradient(90deg,#667eea,#a5b4fc); border-radius: 8px; height: 6px; transition: width 0.8s ease; }
.trend { font-size: 0.78rem; font-weight: 600; color: #4ade80; }

/* Flexbox Stats Container to fix mobile alignment */
.stats-container { display: flex; gap: 10px; justify-content: space-between; margin-bottom: 1rem; }
.stat-box { flex: 1; background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 1rem 0.5rem; text-align: center; }
.stat-num { font-size: 1.8rem; font-weight: 800; color: white; }
.stat-lbl { font-size: 0.75rem; color: rgba(255,255,255,0.45); margin-top: 2px; }

.sec-lbl { font-size: 0.75rem; font-weight: 700; color: rgba(255,255,255,0.45); letter-spacing: 0.1em; text-transform: uppercase; margin: 1.2rem 0 0.7rem; }
.int-hdr { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.2rem; }
.int-field { font-size: 1.3rem; font-weight: 800; color: white; }
.int-mode { font-size: 0.8rem; color: rgba(255,255,255,0.45); margin-top: 3px; }
.q-pill { background: rgba(102,126,234,0.2); border: 1px solid rgba(102,126,234,0.4); color: #a5b4fc; font-size: 0.85rem; font-weight: 700; padding: 8px 16px; border-radius: 20px; white-space: nowrap; }
.mic-wrap { display: flex; flex-direction: column; align-items: center; margin: 1.2rem 0 1rem; }
.mic-outer { width: 110px; height: 110px; border-radius: 50%; background: rgba(102,126,234,0.1); border: 2px solid rgba(102,126,234,0.2); display: flex; align-items: center; justify-content: center; }
.mic-inner { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 8px 32px rgba(102,126,234,0.6); }
.mic-lbl { font-size: 0.82rem; color: rgba(255,255,255,0.4); margin-top: 10px; }
.q-card { background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.12); border-radius: 20px; padding: 1.2rem 1.3rem; margin-bottom: 1rem; }
.q-lbl { font-size: 0.72rem; font-weight: 600; color: #a5b4fc; margin-bottom: 6px; letter-spacing: 0.08em; text-transform: uppercase; }
.q-text { font-size: 1rem; font-weight: 600; color: white; line-height: 1.6; }
.prog-bar-bg { background: rgba(255,255,255,0.1); border-radius: 6px; height: 5px; margin-bottom: 1.2rem; }
.prog-bar-fill { background: linear-gradient(90deg, #667eea, #a5b4fc); border-radius: 6px; height: 5px; transition: width 0.5s ease; }
.fb-q-lbl { font-size: 0.75rem; color: rgba(255,255,255,0.4); margin-bottom: 8px; }
.score-card { background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.12); border-radius: 22px; padding: 1.3rem; margin-bottom: 1rem; }
.sc-top { display: flex; justify-content: space-between; align-items: flex-start; }
.sc-label { font-size: 0.75rem; color: rgba(255,255,255,0.45); margin-bottom: 4px; }
.sc-num { font-size: 3rem; font-weight: 800; display: inline; }
.sc-den { font-size: 1.1rem; color: rgba(255,255,255,0.4); }
.sc-icon { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
.s-green { color: #4ade80; } .c-green { background: linear-gradient(135deg,#4ade80,#22c55e); }
.s-orange { color: #fb923c; } .c-orange { background: linear-gradient(135deg,#fb923c,#f59e0b); }
.s-red { color: #f87171; } .c-red { background: linear-gradient(135deg,#f87171,#ef4444); }
.sc-bar-bg { background: rgba(255,255,255,0.1); border-radius: 6px; height: 6px; margin: 12px 0 8px; }
.sc-verdict { font-size: 0.88rem; font-weight: 600; }
.imp-card { background: rgba(251,146,60,0.08); border: 1px solid rgba(251,146,60,0.2); border-radius: 18px; padding: 1rem 1.1rem; margin-bottom: 0.85rem; display: flex; gap: 12px; align-items: flex-start; }
.imp-ico { background: rgba(251,146,60,0.15); border-radius: 10px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.imp-ttl { font-size: 0.9rem; font-weight: 700; color: #fb923c; margin-bottom: 4px; }
.imp-txt { font-size: 0.82rem; color: rgba(255,255,255,0.85); line-height: 1.55; }
.dw-card { background: rgba(74,222,128,0.07); border: 1px solid rgba(74,222,128,0.2); border-radius: 18px; padding: 1rem 1.1rem; margin-bottom: 0.85rem; }
.dw-ttl { font-size: 0.9rem; font-weight: 700; color: #4ade80; margin-bottom: 8px; }
.dw-item { font-size: 0.82rem; color: rgba(255,255,255,0.85); margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
.res-hero { text-align: center; padding: 1rem 0 0.5rem; }
.res-trophy { font-size: 3rem; margin-bottom: 0.5rem; }
.res-title { font-size: 1.7rem; font-weight: 800; color: white; }
.res-sub { font-size: 0.85rem; color: rgba(255,255,255,0.4); margin-top: 4px; }
.overall-card { background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)); border: 1px solid rgba(102,126,234,0.3); border-radius: 24px; padding: 1.5rem; text-align: center; margin: 1rem 0; }
.ov-num { font-size: 4rem; font-weight: 800; color: white; line-height: 1; }
.ov-den { font-size: 1.5rem; color: rgba(255,255,255,0.4); }
.ov-verdict { font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# ── 2. API & LOGIC ──
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_ai(messages, max_tokens=280):
    r = requests.post(GROQ_URL,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": max_tokens, "temperature": 0.7},
        timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def score_cls(s):
    if s >= 8:  return "s-green",  "c-green",  "#4ade80"
    if s >= 5:  return "s-orange", "c-orange", "#fb923c"
    return "s-red", "c-red", "#f87171"

def evaluate(question, answer):
    mode  = st.session_state.mode
    field = st.session_state.field
    sys_p = (f"You evaluate a {field} interview answer. Style: {mode}. "
             "Return ONLY valid JSON, no markdown:\n"
             '{"score":<1.0-10.0>,"verdict":"<3-5 words>",'
             '"improvement":"<1-2 sentence tip>","strengths":["<s1>","<s2>"]}')
    raw = call_ai([{"role": "system", "content": sys_p},
                   {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"}], 220)
    
    triple_backtick = "```"
    raw = raw.replace(f"{triple_backtick}json", "").replace(triple_backtick, "").strip()
    return json.loads(raw)

# ── 3. QUESTIONS DATABASE (50 per domain) ──
ALL_QUESTIONS = {
    "Software Engineering": [
        "Tell me about yourself and why you chose Software Engineering.",
        "Explain the difference between OOP and functional programming with an example.",
        "What is the difference between a stack and a queue? Give real-world examples.",
        "Explain what REST API is and how it works.",
        "What is the difference between SQL and NoSQL databases?",
        "What is version control and why is Git important?",
        "Explain the concept of recursion with a simple example.",
        "What is time complexity and why does it matter?",
        "What is the difference between HTTP and HTTPS?",
        "Explain what a linked list is and when you would use it.",
        "What is object-oriented programming? Explain its four main principles.",
        "What is the difference between a process and a thread?",
        "What is an API and how have you used one in your projects?",
        "Explain the MVC design pattern.",
        "What is a binary search tree and how does it work?",
        "What is the difference between abstract classes and interfaces?",
        "Explain what debugging is and describe your debugging process.",
        "What is continuous integration and continuous deployment (CI/CD)?",
        "What is the difference between frontend and backend development?",
        "Describe the most challenging technical project you have built.",
        "How do you make sure your code is clean and easy for teammates to understand?",
        "What is a deadlock in operating systems and how do you prevent it?",
        "Explain what polymorphism is with a real example.",
        "What is the difference between synchronous and asynchronous programming?",
        "What is an index in a database and why is it used?",
        "What is Docker and why is it useful?",
        "Explain the concept of machine learning in simple terms.",
        "What is a design pattern? Name three common ones.",
        "What is the difference between unit testing and integration testing?",
        "What is cloud computing and name three cloud service providers.",
        "How do you stay updated with new technologies in software engineering?",
        "Explain what an algorithm is and give an example.",
        "What is the difference between a compiled and interpreted language?",
        "What is memory management and what is garbage collection?",
        "Explain what microservices architecture is.",
        "What is a foreign key in a relational database?",
        "What is the difference between GET and POST HTTP methods?",
        "What is responsive design in web development?",
        "Explain what Big O notation means.",
        "What is a framework and how is it different from a library?",
        "What is agile methodology and how does it work?",
        "Explain what an exception is and how you handle it in code.",
        "What is the difference between deep copy and shallow copy?",
        "What is a virtual machine?",
        "What is the purpose of a load balancer?",
        "What is encapsulation and why is it important?",
        "What is the difference between IPv4 and IPv6?",
        "Explain what a callback function is.",
        "What is CRUD and give an example of each operation.",
        "Where do you see yourself in three years as a software engineer?",
    ],
    "Human Resources": [
        "Tell me about yourself and your passion for Human Resources.",
        "How would you handle a conflict between two employees affecting team performance?",
        "Walk me through your approach to recruiting and selecting the best candidates.",
        "How do you stay updated with labour laws and compliance requirements?",
        "How do you approach employee performance management and career development?",
        "What is the difference between HR generalist and HR specialist roles?",
        "How do you conduct a job analysis?",
        "What strategies do you use to improve employee retention?",
        "How do you handle a situation where a manager is treating employees unfairly?",
        "What is an employee value proposition and why is it important?",
        "How do you measure the effectiveness of a training program?",
        "What is onboarding and how do you design an effective onboarding program?",
        "How do you handle confidential employee information?",
        "What is the difference between coaching and mentoring?",
        "How do you approach diversity and inclusion in the workplace?",
        "What metrics do you use to measure HR success?",
        "How do you handle an employee who is consistently underperforming?",
        "What is a competency framework and how is it used?",
        "How do you build a positive company culture?",
        "What is the purpose of an employee handbook?",
        "How do you conduct an exit interview and use that data?",
        "What is succession planning and why is it important?",
        "How do you handle a harassment complaint in the workplace?",
        "What is the role of HR during organizational change or restructuring?",
        "How do you design a compensation and benefits package?",
        "What is talent management and how does it differ from recruitment?",
        "How do you handle an employee requesting a leave of absence?",
        "What is a 360-degree feedback process?",
        "How do you prioritize tasks when you have multiple HR issues at once?",
        "What is the difference between a job description and a job specification?",
        "How do you ensure fair and unbiased hiring practices?",
        "What is employer branding and how does HR contribute to it?",
        "How do you handle a situation where an employee refuses to follow company policy?",
        "What is the importance of employee engagement surveys?",
        "How do you identify high-potential employees?",
        "What is HRIS and how have you used HR technology?",
        "How do you handle payroll discrepancies?",
        "What is the role of HR in employee wellness programs?",
        "How do you approach salary negotiations with candidates?",
        "What is a KPI and give examples of HR KPIs?",
        "How do you handle an employee who frequently calls in sick?",
        "What is the importance of employee recognition programs?",
        "How do you ensure legal compliance in hiring practices?",
        "What is a performance improvement plan (PIP)?",
        "How do you handle cultural differences in a diverse workplace?",
        "What is the difference between voluntary and involuntary turnover?",
        "How do you build relationships with department managers?",
        "What is an HR audit and how do you conduct one?",
        "How do you handle terminating an employee?",
        "Where do you see HR evolving in the next five years?",
    ],
    "Marketing": [
        "Tell me about yourself and what excites you about a marketing career.",
        "Describe a successful marketing campaign you planned or contributed to.",
        "How do you measure the ROI of a digital marketing campaign?",
        "How do you research and understand your target audience?",
        "How do you balance creative thinking with data-driven decision making?",
        "What is the difference between B2B and B2C marketing?",
        "What is SEO and how do you optimize content for search engines?",
        "How do you create a content marketing strategy?",
        "What is the marketing funnel and explain each stage?",
        "How do you use social media analytics to improve performance?",
        "What is email marketing and what makes an effective email campaign?",
        "How do you handle a product launch from planning to execution?",
        "What is a buyer persona and how do you create one?",
        "What is the difference between organic and paid marketing?",
        "How do you approach competitor analysis?",
        "What is A/B testing and how do you use it in marketing?",
        "What is brand positioning and how do you define it?",
        "How do you calculate customer lifetime value (CLV)?",
        "What is influencer marketing and when is it effective?",
        "How do you create a compelling value proposition?",
        "What is the difference between reach, impressions, and engagement?",
        "How do you manage a marketing budget across multiple channels?",
        "What is conversion rate optimization (CRO)?",
        "How do you write effective ad copy?",
        "What is content marketing and how does it differ from advertising?",
        "How do you build and grow an email subscriber list?",
        "What is affiliate marketing and how does it work?",
        "How do you use Google Analytics to track campaign performance?",
        "What is a unique selling proposition (USP)?",
        "How do you approach rebranding a company or product?",
        "What is customer acquisition cost (CAC) and why does it matter?",
        "How do you create a social media content calendar?",
        "What is the difference between brand awareness and brand loyalty?",
        "How do you use storytelling in marketing?",
        "What is programmatic advertising?",
        "How do you handle negative reviews or a PR crisis?",
        "What is a go-to-market strategy?",
        "How do you segment a market effectively?",
        "What is the role of psychology in consumer behavior?",
        "How do you measure brand sentiment?",
        "What is native advertising and how does it differ from display ads?",
        "How do you approach local marketing for a small business?",
        "What is customer journey mapping?",
        "How do you use data to personalize marketing messages?",
        "What is the difference between a marketing strategy and a marketing plan?",
        "How do you create a viral marketing campaign?",
        "What is retargeting and how does it work?",
        "How do you stay updated with digital marketing trends?",
        "What is omnichannel marketing?",
        "Where do you see marketing evolving in the next five years?",
    ]
}

RECENT = [
    {"name": "Software Engineering", "mode": "Strict Mode",   "score": "9.0", "time": "2 days ago"},
    {"name": "HR Interview",         "mode": "Friendly Mode", "score": "8.5", "time": "4 days ago"},
    {"name": "Marketing",            "mode": "Friendly Mode", "score": "7.8", "time": "1 week ago"},
]

TOTAL = 5  # Number of questions per active session (pulled randomly from the 50 above)

def init():
    defaults = dict(
        screen="home", field=None, mode="Friendly", current_q=0,
        history=[], scores=[], tips=[], strengths=[], answers=[],
        fb_ready=False, q_cache={}
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

def get_questions(field):
    # This ensures a random selection of 5 questions from the 50-question pool every time
    qs = ALL_QUESTIONS.get(field, [])
    return random.sample(qs, min(TOTAL, len(qs)))

def get_followup(q_num):
    mode  = st.session_state.mode
    field = st.session_state.field
    tone  = "warm and encouraging" if mode == "Friendly" else "strict and direct"
    sys_p = (f"You are a {tone} interviewer for a {field} role. "
             f"This is question {q_num} of {TOTAL}. "
             "Based on the conversation, ask ONE smart interview question. "
             "Return ONLY the question. No numbering, no preamble.")
    msgs = ([{"role": "system", "content": sys_p}]
            + st.session_state.history
            + [{"role": "user", "content": f"Ask question {q_num} now."}])
    return call_ai(msgs, 120)

# ════════════════════════════════════════════════════════════════
#  SCREEN: HOME
# ════════════════════════════════════════════════════════════════
if st.session_state.screen == "home":

    st.markdown("""
    <div class="hero-badge">🎙 AI-Powered • 24/7 Available</div>
    <div class="hero-title">Master Your<br><span>Interview Skills</span></div>
    <div class="hero-sub">Practice with AI, get instant feedback, land your dream job.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gcard">
      <div class="score-hero">
        <div>
          <div style="font-size:.75rem;color:rgba(255,255,255,.45);margin-bottom:4px">CAREER READINESS</div>
          <div><span class="score-big">81</span><span class="score-pct">%</span></div>
        </div>
        <div class="score-badge-icon">🏅</div>
      </div>
      <div class="pb-bg"><div class="pb-fill" style="width:81%"></div></div>
      <div style="display:flex;justify-content:space-between;margin-top:8px">
        <span style="font-size:.72rem;color:rgba(255,255,255,.35)">Beginner</span>
        <span class="trend">↗ +12% this week</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Replaced Streamlit columns with custom flexbox for perfect alignment across devices
    st.markdown("""
    <div class="stats-container">
      <div class="stat-box">
        <div class="stat-num">24</div>
        <div class="stat-lbl">Total Sessions</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">8.2</div>
        <div class="stat-lbl">Avg Score /10</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    rows = "".join([
        f"""
        <div class="rp-row">
          <div><div class="rp-name">{p["name"]}</div><div class="rp-mode">{p["mode"]}</div></div>
          <div><div class="rp-score">{p["score"]}</div><div class="rp-time">{p["time"]}</div></div>
        </div>
        """
        for p in RECENT
    ])
    st.markdown(f"""
    <div class="gcard">
      <div class="rp-head">Recent Practice</div>
      {rows}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Mock Interview  →", use_container_width=True, type="primary"):
        st.session_state.screen = "setup"
        st.rerun()

# ════════════════════════════════════════════════════════════════
#  SCREEN: SETUP
# ════════════════════════════════════════════════════════════════
elif st.session_state.screen == "setup":

    st.markdown("""
    <div style="font-size:1.6rem;font-weight:800;color:white;margin-bottom:.3rem">Setup Interview</div>
    <div style="font-size:.85rem;color:rgba(255,255,255,.45);margin-bottom:.5rem">Choose your domain and interviewer style</div>
    <div class="sec-lbl">Select Domain</div>
    """, unsafe_allow_html=True)

    domains = [
        ("Software Engineering", "Technical & coding interviews", "💻"),
        ("Human Resources", "Behavioral & HR interviews", "👤"),
        ("Marketing", "Strategy & creative interviews", "🎯"),
    ]

    for name, sub, icon in domains:
        is_selected = (st.session_state.field == name)
        btn_type = "primary" if is_selected else "secondary"
        if st.button(f"{icon}   **{name}** — {sub}", key=f"d_{name}", type=btn_type, use_container_width=True):
            st.session_state.field = name
            st.rerun()

    st.markdown('<div class="sec-lbl">Interviewer Style</div>', unsafe_allow_html=True)

    cf, cs = st.columns(2)
    with cf:
        is_friendly = (st.session_state.mode == "Friendly")
        if st.button("🙂   **Friendly**", key="bf", type="primary" if is_friendly else "secondary", use_container_width=True):
            st.session_state.mode = "Friendly"
            st.rerun()
    with cs:
        is_strict = (st.session_state.mode == "Strict")
        if st.button("🎯   **Strict**", key="bs", type="primary" if is_strict else "secondary", use_container_width=True):
            st.session_state.mode = "Strict"
            st.rerun()

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)
    
    go = bool(st.session_state.field)
    if st.button("Continue to Interview  →", use_container_width=True, type="primary", disabled=not go):
        questions = get_questions(st.session_state.field)
        st.session_state.update(
            screen="interview", current_q=0, history=[],
            scores=[], tips=[], strengths=[], answers=[],
            fb_ready=False, q_cache={i: q for i, q in enumerate(questions)}
        )
        st.rerun()
    if not go:
        st.markdown('<div style="text-align:center;font-size:.8rem;color:rgba(255,255,255,.35);margin-top:.5rem">Please select a domain to continue</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  SCREEN: INTERVIEW
# ════════════════════════════════════════════════════════════════
elif st.session_state.screen == "interview":

    qi    = st.session_state.current_q
    field = st.session_state.field
    mode  = st.session_state.mode
    pct   = int(qi / TOTAL * 100)
    emoji = "🙂" if mode == "Friendly" else "🎯"

    st.markdown(f"""
    <div class="prog-bar-bg">
      <div class="prog-bar-fill" style="width:{pct}%"></div>
    </div>
    <div class="int-hdr">
      <div>
        <div class="int-field">{field}</div>
        <div class="int-mode">{emoji} {mode} Mode</div>
      </div>
      <div class="q-pill">Q {qi+1} / {TOTAL}</div>
    </div>
    <div class="mic-wrap">
      <div class="mic-outer"><div class="mic-inner">🎙️</div></div>
      <div class="mic-lbl">AI is listening...</div>
    </div>
    """, unsafe_allow_html=True)

    if qi not in st.session_state.q_cache:
        with st.spinner("Preparing question..."):
            try:
                q = get_followup(qi + 1)
                st.session_state.q_cache[qi] = q
            except Exception as e:
                st.error(f"Could not load question: {e}")
                st.stop()

    question = st.session_state.q_cache[qi]

    st.markdown(f"""
    <div class="q-card">
      <div class="q-lbl">Question {qi+1}</div>
      <div class="q-text">{question}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.fb_ready:
        ans = st.text_area("ans", placeholder="Type your answer here...",
                           height=120, label_visibility="collapsed", key=f"a{qi}")

        cs2, ck = st.columns([3, 1])
        with cs2:
            if st.button("Submit Answer", use_container_width=True, type="primary", disabled=not ans.strip()):
                with st.spinner("Evaluating..."):
                    try:
                        res = evaluate(question, ans.strip())
                        sc  = float(res.get("score", 5))
                        st.session_state.scores.append(sc)
                        st.session_state.tips.append(res.get("improvement", ""))
                        st.session_state.strengths.append(res.get("strengths", ["Clear response", "Good effort"]))
                        st.session_state.answers.append(ans.strip())
                        st.session_state[f"vd{qi}"] = res.get("verdict", "Good Effort!")
                        st.session_state.history += [
                            {"role": "assistant", "content": question},
                            {"role": "user",      "content": ans.strip()}
                        ]
                        st.session_state.fb_ready = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Evaluation error: {e}")
        with ck:
            if st.button("Skip", use_container_width=True):
                st.session_state.scores.append(0)
                st.session_state.tips.append("Skipped.")
                st.session_state.strengths.append([])
                st.session_state.answers.append("[Skipped]")
                st.session_state.history += [
                    {"role": "assistant", "content": question},
                    {"role": "user",      "content": "I want to skip this."}
                ]
                st.session_state.fb_ready  = False
                st.session_state.current_q += 1
                if st.session_state.current_q >= TOTAL:
                    st.session_state.screen = "results"
                st.rerun()

    else:
        sc   = st.session_state.scores[qi]
        tip  = st.session_state.tips[qi]
        strs = st.session_state.strengths[qi]
        verd = st.session_state.get(f"vd{qi}", "Good Effort!")
        nc, cc, vc = score_cls(sc)
        pct2 = int(sc / 10 * 100)

        st.markdown(f'<div class="fb-q-lbl">Question {qi+1} of {TOTAL} — Feedback</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="score-card">
          <div class="sc-top">
            <div>
              <div class="sc-label">YOUR SCORE</div>
              <span class="sc-num {nc}">{sc}</span><span class="sc-den">/10</span>
            </div>
            <div class="sc-icon {cc}">↗</div>
          </div>
          <div class="sc-bar-bg">
            <div style="background:{vc};border-radius:6px;height:6px;width:{pct2}%"></div>
          </div>
          <div class="sc-verdict" style="color:{vc}">✓ {verd}</div>
        </div>
        """, unsafe_allow_html=True)

        if tip:
            st.markdown(f"""
            <div class="imp-card">
              <div class="imp-ico">⚡</div>
              <div>
                <div class="imp-ttl">Key Improvement</div>
                <div class="imp-txt">{tip}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        if strs:
            items = "".join([f'<div class="dw-item">✅ {s}</div>' for s in strs])
            st.markdown(f"""
            <div class="dw-card">
              <div class="dw-ttl">What You Did Well</div>
              {items}
            </div>
            """, unsafe_allow_html=True)

        is_last = qi >= TOTAL - 1
        lbl = "View Results  🏆" if is_last else "Next Question  →"
        if st.button(lbl, use_container_width=True, type="primary"):
            st.session_state.fb_ready  = False
            st.session_state.current_q += 1
            if st.session_state.current_q >= TOTAL:
                st.session_state.screen = "results"
            st.rerun()

        if st.button("Exit Interview", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()

# ════════════════════════════════════════════════════════════════
#  SCREEN: RESULTS
# ════════════════════════════════════════════════════════════════
elif st.session_state.screen == "results":

    valid = [s for s in st.session_state.scores if s > 0]
    avg   = round(sum(valid) / len(valid), 1) if valid else 0.0
    best  = max(valid) if valid else 0

    if avg >= 8:   verd = "Excellent Performance! 🌟"
    elif avg >= 6: verd = "Good Effort — Keep Polishing! 👍"
    elif avg >= 4: verd = "Good Start — Practice More! 📈"
    else:          verd = "Keep Practicing — You'll Improve! 💪"

    nc, cc, vc = score_cls(avg)
    pct = int(avg / 10 * 100)

    st.markdown(f"""
    <div class="res-hero">
      <div class="res-trophy">🏆</div>
      <div class="res-title">Session Complete!</div>
      <div class="res-sub">{st.session_state.field} · {st.session_state.mode} Mode</div>
    </div>
    <div class="overall-card">
      <div style="font-size:.75rem;color:rgba(255,255,255,.45);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px">Overall Score</div>
      <span class="ov-num">{avg}</span><span class="ov-den">/10</span>
      <div style="background:rgba(255,255,255,.1);border-radius:6px;height:6px;margin:14px auto;max-width:180px">
        <div style="background:{vc};border-radius:6px;height:6px;width:{pct}%"></div>
      </div>
      <div class="ov-verdict">{verd}</div>
    </div>
    """, unsafe_allow_html=True)

    # Replaced Streamlit columns with custom flexbox for perfect alignment across devices
    st.markdown(f"""
    <div class="stats-container">
      <div class="stat-box">
        <div class="stat-num">{len(valid)}</div>
        <div class="stat-lbl">Answered</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{avg}</div>
        <div class="stat-lbl">Average</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{best}</div>
        <div class="stat-lbl">Best</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:.75rem;font-weight:700;color:rgba(255,255,255,.4);letter-spacing:.1em;text-transform:uppercase;margin:1.2rem 0 .7rem">
      Question Breakdown
    </div>
    """, unsafe_allow_html=True)

    for i in range(len(st.session_state.scores)):
        s   = st.session_state.scores[i]
        q   = st.session_state.q_cache.get(i, f"Question {i+1}")
        tip = st.session_state.tips[i]
        lbl = f"{s}/10" if s > 0 else "Skipped"
        
        with st.expander(f"Q{i+1}: {q[:50]}… — {lbl}"):
            st.write(f"**Your Answer:**\n {st.session_state.answers[i]}")
            if tip and "Skipped" not in tip:
                st.markdown(f"""
                <div class="imp-card">
                  <div class="imp-ico">💡</div>
                  <div>
                    <div class="imp-ttl">Tip</div>
                    <div class="imp-txt">{tip}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    
    if st.button("🔄  Practice Again", use_container_width=True, type="primary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init()
        st.session_state.screen = "setup"
        st.rerun()