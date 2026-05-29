import streamlit as st
import json, requests, random

# ── CONFIGURATION ──
st.set_page_config(page_title="AI Interview Master", page_icon="🎙️", layout="centered", initial_sidebar_state="collapsed")

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = ""

# ── GLOBAL CSS (FLAT UI, NO CODE BOXES) ──
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
</style>
""", unsafe_allow_html=True)

# ── AI LOGIC (STRICTLY NEUTRAL) ──
def call_ai(messages, max_tokens=280):
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": max_tokens, "temperature": 0.5})
    return r.json()["choices"][0]["message"]["content"].strip()

def evaluate(question, answer):
    # REMOVED ALL ENCOURAGING LANGUAGE / STRICTLY NEUTRAL
    sys_p = ("You are a professional, neutral interviewer. Evaluate the candidate's answer for technical accuracy and relevance. "
             "Return ONLY valid JSON. No conversational fillers, no encouragement, no cheerleading:\n"
             '{"score":<1.0-10.0>,"verdict":"<Factual verdict>",'
             '"improvement":"<Provide a direct, neutral technical correction if needed.>",'
             '"strengths":["<s1>","<s2>"]}')
    raw = call_ai([{"role": "system", "content": sys_p},
                   {"role": "user", "content": f"Q: {question}\nA: {answer}"}])
    return json.loads(raw.replace("```json", "").replace("```", ""))

# ── INITIALIZE STATE ──
if 'screen' not in st.session_state:
    st.session_state.update(screen="home", history=[], current_q=0, field=None, scores=[], answers=[], tips=[], strengths=[])

# ── MAIN INTERFACE ──
if st.session_state.screen == "home":
    st.markdown('<div class="rp-head" style="text-align:center;">AI Interview Master</div>', unsafe_allow_html=True)
    
    # RECENT PRACTICE (FLAT HTML)
    st.markdown("""
    <div class="rp-container">
      <div class="rp-head">Recent Practice</div>
      <div class="rp-row">
        <div><div class="rp-name">Software Engineering</div><div class="rp-mode">Strict Mode</div></div>
        <div><div class="rp-score">9.0</div><div class="rp-time">2 days ago</div></div>
      </div>
      <div class="rp-row">
        <div><div class="rp-name">HR Interview</div><div class="rp-mode">Neutral Mode</div></div>
        <div><div class="rp-score">8.5</div><div class="rp-time">4 days ago</div></div>
      </div>
      <div class="rp-row">
        <div><div class="rp-name">Marketing</div><div class="rp-mode">Neutral Mode</div></div>
        <div><div class="rp-score">7.8</div><div class="rp-time">1 week ago</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Mock Interview"):
        st.session_state.screen = "interview"
        st.rerun()

elif st.session_state.screen == "interview":
    st.markdown("### Interview Session")
    # INTERVIEW LOOP LOGIC
    # Ensure all feedback uses: st.markdown(f"...", unsafe_allow_html=True)
    if st.button("Back Home"):
        st.session_state.screen = "home"
        st.rerun()
