import streamlit as st
import json, requests, random

# ── 1. CONFIGURATION ──
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

# ── 2. GLOBAL CSS (FLAT UI, ZERO INDENTATION TO PREVENT CODE BOXES) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
html, body, .stApp { background: #0F0C29 !important; font-family: 'Plus Jakarta Sans', sans-serif; }
.rp-container { background: rgba(20, 20, 35, 0.5); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 1.5rem; margin-bottom: 1.5rem; }
.rp-head { font-size: 1.2rem; font-weight: 800; color: #ffffff; margin-bottom: 1.2rem; }
.rp-row { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.rp-name { font-size: 1rem; font-weight: 700; color: #ffffff; }
.rp-mode { font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-top: 4px; }
.rp-score { font-size: 1.2rem; font-weight: 800; color: #4ade80; text-align: right; }
.rp-time { font-size: 0.75rem; color: rgba(255,255,255,0.4); text-align: right; margin-top: 4px; }
.stTextArea textarea { background-color: #17153B !important; color: #ffffff !important; border-radius: 16px !important; border: 1px solid #302B63 !important; }
.imp-card { background: #1A1A2E; border-left: 4px solid #4ade80; padding: 1rem; margin-bottom: 1rem; border-radius: 8px; color: white; }
.sec-lbl { font-size: 1.2rem; font-weight: 800; color: white; margin-top: 2rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── 3. AI EVALUATION LOGIC (STRICTLY NEUTRAL, NO ENCOURAGEMENT) ──
def evaluate(question, answer):
    sys_p = ("You are a strict, objective, and neutral technical interviewer. Evaluate the candidate's answer for technical accuracy and relevance. "
             "DO NOT use any encouraging words, greetings, or conversational fillers. Provide direct, factual feedback only. "
             "Return ONLY valid JSON:\n"
             '{"score":<1.0-10.0>,"verdict":"<Direct factual verdict without encouragement>","improvement":"<Direct, neutral technical correction if needed>","strengths":["<s1>","<s2>"]}')
    
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": sys_p}, 
                  {"role": "user", "content": f"Q: {question}\nA: {answer}"}]})
        return json.loads(r.json()["choices"][0]["message"]["content"].replace("```json", "").replace("```", ""))
    except Exception:
        return {"score": 0.0, "verdict": "Error analyzing response.", "improvement": "System error. Please skip or retry.", "strengths": []}

# ── 4. QUESTIONS DATABASE (50 PER DOMAIN) ──
ALL_QUESTIONS = {
    "Software Engineering": ["Tell me about yourself.", "Explain OOP.", "What is REST?", "SQL vs NoSQL?", "Git basics?", "Recursion?", "Time complexity?", "HTTP vs HTTPS?", "Linked lists?", "MVC pattern?", "Binary search?", "Abstract vs Interface?", "Debugging?", "CI/CD?", "Frontend vs Backend?", "Hardest project?", "Clean code?", "Deadlocks?", "Polymorphism?", "Async programming?", "DB indexing?", "Docker?", "Machine Learning?", "Design patterns?", "Unit testing?", "Cloud computing?", "Stay updated?", "Algorithms?", "Compiled vs Interpreted?", "Memory management?", "Microservices?", "Foreign keys?", "GET vs POST?", "Responsive design?", "Big O?", "Framework vs Library?", "Agile?", "Exception handling?", "Copying objects?", "Virtual machines?", "Load balancers?", "Encapsulation?", "IPv4 vs IPv6?", "Callback functions?", "CRUD operations?", "Career goals?", "Dependency injection?", "TDD?", "System design?", "Refactoring?"],
    "Human Resources": ["Tell me about yourself.", "Handling conflict?", "Recruitment approach?", "Labor laws?", "Performance management?", "Generalist vs Specialist?", "Job analysis?", "Retention strategies?", "Unfair treatment?", "EVP?", "Training effectiveness?", "Onboarding?", "Confidentiality?", "Coaching vs Mentoring?", "Diversity & Inclusion?", "HR metrics?", "Underperformance?", "Competency frameworks?", "Company culture?", "Employee handbooks?", "Exit interviews?", "Succession planning?", "Harassment policy?", "HR in restructuring?", "Compensation design?", "Talent management?", "Leaves of absence?", "360-degree feedback?", "Prioritizing tasks?", "Job specs?", "Unbiased hiring?", "Employer branding?", "Policy violations?", "Engagement surveys?", "High-potential talent?", "HRIS experience?", "Payroll issues?", "Wellness programs?", "Salary negotiations?", "KPIs?", "Attendance issues?", "Recognition programs?", "Legal compliance?", "PIPs?", "Cultural differences?", "Turnover types?", "Manager relations?", "HR audits?", "Terminations?", "Future of HR?"],
    "Marketing": ["Tell me about yourself.", "Successful campaign?", "Measuring ROI?", "Target audience research?", "Creative vs Data?", "B2B vs B2C?", "SEO basics?", "Content strategy?", "Marketing funnel?", "Social analytics?", "Email marketing?", "Product launches?", "Buyer personas?", "Organic vs Paid?", "Competitor analysis?", "A/B testing?", "Brand positioning?", "CLV calculations?", "Influencer marketing?", "Value propositions?", "Reach vs Engagement?", "Budget management?", "CRO?", "Ad copywriting?", "Content vs Advertising?", "Building email lists?", "Affiliate marketing?", "Google Analytics?", "USP definition?", "Rebranding?", "CAC explained?", "Content calendars?", "Brand awareness?", "Storytelling?", "Programmatic ads?", "PR crisis?", "Go-to-market strategy?", "Market segmentation?", "Consumer psychology?", "Brand sentiment?", "Native advertising?", "Local marketing?", "Customer journeys?", "Data personalization?", "Strategy vs Plan?", "Viral marketing?", "Retargeting?", "Marketing trends?", "Omnichannel marketing?", "Marketing future?"]
}

# ── 5. STATE MANAGEMENT ──
if 'screen' not in st.session_state:
    st.session_state.update(screen="home", field=None, current_q=0, history=[], scores=[], answers=[], tips=[], strengths=[], q_cache={})

# ── 6. MAIN APP LOGIC ──
if st.session_state.screen == "home":
    # HTML must be flush-left to prevent white code boxes
    st.markdown("""
<div class="rp-head" style="text-align:center;">AI Interview Master</div>
""", unsafe_allow_html=True)
    
    st.markdown("""
<div class="rp-container">
  <div class="rp-head">Recent Practice</div>
  <div class="rp-row"><div><div class="rp-name">Software Engineering</div><div class="rp-mode">Strict Mode</div></div><div><div class="rp-score">9.0</div><div class="rp-time">2 days ago</div></div></div>
  <div class="rp-row"><div><div class="rp-name">HR Interview</div><div class="rp-mode">Neutral Mode</div></div><div><div class="rp-score">8.5</div><div class="rp-time">4 days ago</div></div></div>
  <div class="rp-row"><div><div class="rp-name">Marketing</div><div class="rp-mode">Neutral Mode</div></div><div><div class="rp-score">7.8</div><div class="rp-time">1 week ago</div></div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### Start New Interview")
    domain = st.selectbox("Select Domain", list(ALL_QUESTIONS.keys()))
    if st.button("Start Mock Interview"):
        st.session_state.field = domain
        st.session_state.history = random.sample(ALL_QUESTIONS[domain], 5) # Select 5 questions from the 50
        st.session_state.current_q = 0
        st.session_state.scores = []
        st.session_state.answers = []
        st.session_state.tips = []
        st.session_state.strengths = []
        st.session_state.q_cache = {i: q for i, q in enumerate(st.session_state.history)}
        st.session_state.screen = "interview"
        st.rerun()

elif st.session_state.screen == "interview":
    idx = st.session_state.current_q
    if idx < len(st.session_state.history):
        q = st.session_state.history[idx]
        st.markdown(f"<div class='sec-lbl'>Question {idx+1} of {len(st.session_state.history)}</div>", unsafe_allow_html=True)
        st.write(f"**{q}**")
        
        ans = st.text_area("Your Answer:", key=f"ans_{idx}", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer"):
                if ans.strip():
                    with st.spinner("Analyzing response..."):
                        res = evaluate(q, ans)
                        st.session_state.scores.append(res.get("score", 0))
                        st.session_state.answers.append(ans)
                        st.session_state.tips.append(res.get("improvement", ""))
                        st.session_state.strengths.append(res.get("strengths", []))
                        st.session_state.current_q += 1
                        st.rerun()
                else:
                    st.warning("Please provide an answer before submitting.")
        with col2:
            if st.button("Skip Question"):
                st.session_state.scores.append(0)
                st.session_state.answers.append("Skipped")
                st.session_state.tips.append("Question skipped.")
                st.session_state.strengths.append([])
                st.session_state.current_q += 1
                st.rerun()
    else:
        st.session_state.screen = "results"
        st.rerun()

elif st.session_state.screen == "results":
    st.markdown("<div class='sec-lbl'>Interview Complete</div>", unsafe_allow_html=True)
    avg_score = sum(st.session_state.scores) / len(st.session_state.scores) if st.session_state.scores else 0
    
    st.markdown(f"""
<div class="rp-container" style="text-align:center;">
  <div class="rp-head">Final Score</div>
  <div class="rp-score" style="font-size: 2rem;">{avg_score:.1f} / 10</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='sec-lbl'>Question Breakdown</div>", unsafe_allow_html=True)
    
    for i in range(len(st.session_state.scores)):
        s = st.session_state.scores[i]
        q = st.session_state.q_cache.get(i, f"Question {i+1}")
        tip = st.session_state.tips[i]
        lbl = f"{s}/10" if s > 0 else "Skipped"
        
        with st.expander(f"Q{i+1}: {q[:45]}… — {lbl}"):
            st.markdown(f"""
<div style="color:white; font-size: 0.95rem; margin-bottom: 15px;">
  <b>Your Answer:</b><br>{st.session_state.answers[i]}
</div>
""", unsafe_allow_html=True)
            
            if tip and "Skipped" not in tip:
                st.markdown(f"""
<div class="imp-card" style="margin-bottom:0;">
  <div>
    <div style="font-weight:bold; margin-bottom:5px;">Direct Feedback</div>
    <div>{tip}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    if st.button("Return Home"):
        st.session_state.screen = "home"
        st.rerun()