import streamlit as st
import json, re, requests

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Interview Master",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
#  API KEY — loaded from Streamlit secrets, never asked from user
# ═══════════════════════════════════════════════════════════════
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = ""

# ═══════════════════════════════════════════════════════════════
#  CSS — matches Figma design exactly
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:#EEF1F8;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.4rem 1.1rem 3rem;max-width:460px;margin:auto;}
.stButton>button{font-family:'Inter',sans-serif;font-weight:600;border-radius:14px;padding:0.75rem 1rem;transition:all .15s;}
.stButton>button[kind="primary"]{background:#2B4EFF;color:white;border:none;border-radius:16px;font-size:1rem;padding:.85rem;}
.stButton>button[kind="primary"]:hover{background:#1a3de0;}
.stButton>button[kind="secondary"]{background:white;color:#374151;border:1.5px solid #E5E7EB;}
.stTextArea textarea{border-radius:16px;border:1.5px solid #E5E7EB;font-family:'Inter',sans-serif;font-size:.95rem;background:white;color:#111827;padding:.9rem 1rem;}
.stTextArea textarea:focus{border-color:#2B4EFF;}
.card{background:#fff;border-radius:20px;padding:1.15rem 1.3rem;margin-bottom:.9rem;box-shadow:0 2px 12px rgba(0,0,0,.06);}
.page-title{font-size:2rem;font-weight:800;color:#2B4EFF;margin-bottom:.1rem;}
.page-sub{font-size:.95rem;color:#6B7280;margin-bottom:1.3rem;}
.cr-label{font-size:.8rem;color:#9CA3AF;}
.cr-num{font-size:2.1rem;font-weight:800;color:#2B4EFF;}
.pb-bg{background:#E5E7EB;border-radius:8px;height:8px;margin-top:10px;}
.pb-fill{background:#2B4EFF;border-radius:8px;height:8px;}
.stat-label{font-size:.8rem;color:#9CA3AF;margin-bottom:3px;}
.stat-val{font-size:1.65rem;font-weight:700;color:#111827;}
.rp-head{font-size:1rem;font-weight:700;color:#111827;margin-bottom:.7rem;}
.rp-row{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #F3F4F6;}
.rp-name{font-size:.9rem;font-weight:600;color:#111827;}
.rp-mode,.rp-time{font-size:.75rem;color:#9CA3AF;}
.rp-score{font-size:.95rem;font-weight:700;color:#22C55E;}
.sec-label{font-size:1rem;font-weight:700;color:#111827;margin:1rem 0 .55rem;}
.domain-card{background:white;border-radius:16px;padding:.95rem 1.1rem;margin-bottom:.65rem;display:flex;align-items:center;gap:.9rem;border:2px solid transparent;box-shadow:0 1px 6px rgba(0,0,0,.05);}
.domain-card.sel{border-color:#2B4EFF;}
.d-icon{width:50px;height:50px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;}
.d-name{font-size:.97rem;font-weight:700;color:#111827;}
.d-sub{font-size:.78rem;color:#9CA3AF;}
.style-card{border-radius:16px;padding:.95rem;text-align:center;border:2px solid transparent;box-shadow:0 1px 6px rgba(0,0,0,.05);}
.style-card.friendly{background:#F0FDF4;border-color:#BBF7D0;}
.style-card.strict{background:#fff;border-color:#E5E7EB;}
.style-card.sel-f{border-color:#22C55E!important;}
.style-card.sel-s{border-color:#374151!important;}
.s-icon{font-size:1.9rem;margin-bottom:5px;}
.s-label{font-size:.88rem;font-weight:600;color:#374151;}
.int-hdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.1rem;}
.int-field{font-size:1.25rem;font-weight:700;color:#111827;}
.int-mode{font-size:.8rem;color:#9CA3AF;margin-top:2px;}
.q-badge{background:white;border-radius:50%;width:50px;height:50px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.92rem;color:#111827;box-shadow:0 2px 8px rgba(0,0,0,.1);flex-shrink:0;}
.mic-wrap{display:flex;flex-direction:column;align-items:center;margin:1.1rem 0;}
.mic-circle{width:96px;height:96px;border-radius:50%;background:#3D4F6E;display:flex;align-items:center;justify-content:center;font-size:2.4rem;box-shadow:0 0 0 14px rgba(61,79,110,.1),0 0 0 28px rgba(61,79,110,.05);}
.mic-lbl{font-size:.83rem;color:#9CA3AF;margin-top:10px;}
.q-lbl{font-size:.76rem;color:#9CA3AF;margin-bottom:5px;}
.q-text{font-size:.97rem;font-weight:600;color:#111827;line-height:1.55;}
.fb-qlabel{font-size:.76rem;color:#9CA3AF;margin-bottom:6px;}
.score-num{font-size:2.9rem;font-weight:800;display:inline;}
.score-den{font-size:1.2rem;font-weight:400;color:#9CA3AF;}
.s-orange{color:#F59E0B;}.s-green{color:#22C55E;}.s-red{color:#EF4444;}
.s-circle{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:700;color:white;float:right;margin-top:-6px;}
.c-orange{background:#F59E0B;}.c-green{background:#22C55E;}.c-red{background:#EF4444;}
.verdict{font-size:.88rem;font-weight:600;margin-top:5px;}
.imp-card{background:white;border-radius:16px;padding:1rem 1.1rem;margin-bottom:.85rem;display:flex;gap:11px;align-items:flex-start;box-shadow:0 1px 6px rgba(0,0,0,.05);}
.imp-ico{background:#F3F4F6;border-radius:10px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:.95rem;flex-shrink:0;}
.imp-ttl{font-size:.92rem;font-weight:700;color:#111827;margin-bottom:3px;}
.imp-txt{font-size:.83rem;color:#6B7280;line-height:1.55;}
.dw-card{background:#F0FDF4;border-radius:16px;padding:1rem 1.1rem;margin-bottom:.85rem;border:1px solid #BBF7D0;}
.dw-ttl{font-size:.92rem;font-weight:700;color:#15803D;margin-bottom:7px;}
.dw-item{font-size:.83rem;color:#166534;margin-bottom:3px;}
.res-title{font-size:1.65rem;font-weight:800;color:#111827;text-align:center;margin-bottom:.2rem;}
.res-sub{font-size:.88rem;color:#9CA3AF;text-align:center;margin-bottom:1.1rem;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  GROQ API CALL
# ═══════════════════════════════════════════════════════════════
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_ai(messages, max_tokens=280):
    r = requests.post(GROQ_URL,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}",
                 "Content-Type": "application/json"},
        json={"model": "llama-3.1-8b-instant", "messages": messages,
              "max_tokens": max_tokens, "temperature": 0.7},
        timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

# ═══════════════════════════════════════════════════════════════
#  QUESTION BANKS
# ═══════════════════════════════════════════════════════════════
QUESTIONS = {
    "Software Engineering": [
        "Tell me about yourself and why you chose Software Engineering.",
        "Explain the difference between OOP and functional programming with an example.",
        "Describe the most challenging technical project you have built.",
        "How do you make sure your code is clean and easy for teammates to understand?",
        "Where do you see yourself in three years as a software engineer?"
    ],
    "Human Resources": [
        "Tell me about yourself and your passion for Human Resources.",
        "How would you handle a conflict between two employees affecting team performance?",
        "Walk me through your approach to recruiting and selecting the best candidates.",
        "How do you stay updated with labour laws and compliance requirements?",
        "How do you approach employee performance management and career development?"
    ],
    "Marketing": [
        "Tell me about yourself and what excites you about a marketing career.",
        "Describe a successful marketing campaign you planned or contributed to.",
        "How do you measure the ROI of a digital marketing campaign?",
        "How do you research and understand your target audience?",
        "How do you balance creative thinking with data-driven decision making?"
    ]
}

RECENT = [
    {"name": "Software Engineering", "mode": "Strict Mode",   "score": "9.0", "time": "2 days ago"},
    {"name": "HR Interview",         "mode": "Friendly Mode", "score": "8.5", "time": "4 days ago"},
    {"name": "Marketing",            "mode": "Friendly Mode", "score": "7.8", "time": "1 week ago"},
]

TOTAL = 5

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════
#  AI FUNCTIONS
# ═══════════════════════════════════════════════════════════════
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


def evaluate(question, answer):
    mode  = st.session_state.mode
    field = st.session_state.field
    sys_p = (f"You evaluate a {field} interview answer. Style: {mode}. "
             "Return ONLY valid JSON, no markdown:\n"
             '{"score":<1.0-10.0>,"verdict":"<3-5 words>",'
             '"improvement":"<1-2 sentence tip>","strengths":["<s1>","<s2>"]}')
    raw = call_ai([{"role": "system", "content": sys_p},
                   {"role": "user",
                    "content": f"Question: {question}\nAnswer: {answer}"}], 220)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def score_cls(s):
    if s >= 8:
        return "s-green",  "c-green",  "#22C55E"
    if s >= 5:
        return "s-orange", "c-orange", "#F59E0B"
    return "s-red", "c-red", "#EF4444"

# ═══════════════════════════════════════════════════════════════
#  SCREEN: HOME
# ═══════════════════════════════════════════════════════════════
if st.session_state.screen == "home":

    st.markdown('<div class="page-title">AI Interview Master</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your 24/7 Virtual Career Mentor</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <div class="cr-label">Career Readiness Score</div>
          <div class="cr-num">81%</div>
        </div>
        <div style="background:#2B4EFF;border-radius:14px;width:50px;height:50px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.4rem">🏅</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px">
        <div class="pb-bg" style="flex:1">
          <div class="pb-fill" style="width:81%"></div>
        </div>
        <span style="color:#22C55E;font-weight:600;font-size:.83rem">↗ +12%</span>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div class="card"><div class="stat-label">Interviews</div>'
            '<div class="stat-val">24</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            '<div class="card"><div class="stat-label">Avg Score</div>'
            '<div class="stat-val">8.2/10</div></div>', unsafe_allow_html=True)

    rows = "".join([
        f'<div class="rp-row">'
        f'<div><div class="rp-name">{p["name"]}</div>'
        f'<div class="rp-mode">{p["mode"]}</div></div>'
        f'<div><div class="rp-score">{p["score"]}</div>'
        f'<div class="rp-time">{p["time"]}</div></div></div>'
        for p in RECENT
    ])
    st.markdown(
        f'<div class="card"><div class="rp-head">Recent Practice</div>{rows}</div>',
        unsafe_allow_html=True)

    if st.button("▶  Start Mock Interview", use_container_width=True, type="primary"):
        st.session_state.screen = "setup"
        st.rerun()

# ═══════════════════════════════════════════════════════════════
#  SCREEN: SETUP
# ═══════════════════════════════════════════════════════════════
elif st.session_state.screen == "setup":

    st.markdown(
        '<div class="page-title" style="font-size:1.7rem">Setup Your Interview</div>',
        unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Choose your domain and interviewer style</div>',
        unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Select Domain</div>', unsafe_allow_html=True)

    domains = [
        ("Software Engineering", "Technical & coding interviews",  "💻", "#2B4EFF", "#EEF1FF"),
        ("Human Resources",      "Behavioral & HR interviews",     "👤", "#7C3AED", "#F3EEFF"),
        ("Marketing",            "Strategy & creative interviews", "🎯", "#EC4899", "#FFF0F7"),
    ]

    for name, sub, icon, ic, bg in domains:
        sel   = st.session_state.field == name
        radio = "🔵" if sel else ""
        st.markdown(
            f'<div class="domain-card {"sel" if sel else ""}">'
            f'<div class="d-icon" style="background:{bg};color:{ic}">{icon}</div>'
            f'<div style="flex:1">'
            f'<div class="d-name">{name}</div>'
            f'<div class="d-sub">{sub}</div></div>'
            f'<div>{radio}</div></div>', unsafe_allow_html=True)
        if st.button(f"Select {name}", key=f"d_{name}", use_container_width=True):
            st.session_state.field = name
            st.rerun()

    st.markdown('<div class="sec-label">Choose Interviewer Style</div>',
                unsafe_allow_html=True)

    cf, cs = st.columns(2)
    with cf:
        sf = st.session_state.mode == "Friendly"
        st.markdown(
            f'<div class="style-card friendly {"sel-f" if sf else ""}">'
            '<div class="s-icon">🙂</div>'
            '<div class="s-label">Friendly</div></div>', unsafe_allow_html=True)
        if st.button("Friendly", use_container_width=True, key="bf"):
            st.session_state.mode = "Friendly"
            st.rerun()
    with cs:
        ss = st.session_state.mode == "Strict"
        st.markdown(
            f'<div class="style-card strict {"sel-s" if ss else ""}">'
            '<div class="s-icon">🛡️</div>'
            '<div class="s-label">Strict</div></div>', unsafe_allow_html=True)
        if st.button("Strict", use_container_width=True, key="bs"):
            st.session_state.mode = "Strict"
            st.rerun()

    st.markdown("<div style='margin-top:.8rem'></div>", unsafe_allow_html=True)
    go = bool(st.session_state.field)
    if st.button("Continue to Interview  →", use_container_width=True,
                 type="primary", disabled=not go):
        st.session_state.update(
            screen="interview", current_q=0, history=[],
            scores=[], tips=[], strengths=[], answers=[],
            fb_ready=False, q_cache={}
        )
        st.rerun()
    if not go:
        st.caption("Please select a domain first.")

# ═══════════════════════════════════════════════════════════════
#  SCREEN: INTERVIEW
# ═══════════════════════════════════════════════════════════════
elif st.session_state.screen == "interview":

    qi    = st.session_state.current_q
    field = st.session_state.field
    mode  = st.session_state.mode
    icon  = "🙂" if mode == "Friendly" else "🛡️"

    st.markdown(
        f'<div class="int-hdr">'
        f'<div><div class="int-field">{field}</div>'
        f'<div class="int-mode">{icon} {mode} Mode</div></div>'
        f'<div class="q-badge">{qi + 1}/5</div></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="mic-wrap">'
        '<div class="mic-circle">🎙️</div>'
        '<div class="mic-lbl">AI is listening...</div></div>',
        unsafe_allow_html=True)

    if qi not in st.session_state.q_cache:
        with st.spinner("Preparing question..."):
            try:
                q = QUESTIONS[field][qi] if qi == 0 else get_followup(qi + 1)
                st.session_state.q_cache[qi] = q
            except Exception as e:
                st.error(f"Could not load question: {e}")
                st.stop()

    question = st.session_state.q_cache[qi]

    st.markdown(
        f'<div class="card">'
        f'<div class="q-lbl">Question {qi + 1}</div>'
        f'<div class="q-text">{question}</div></div>', unsafe_allow_html=True)

    if not st.session_state.fb_ready:
        ans = st.text_area(
            "ans", placeholder="Type your answer here or speak...",
            height=125, label_visibility="collapsed", key=f"a{qi}")

        cs2, ck = st.columns([3, 1])
        with cs2:
            if st.button("Submit Answer", use_container_width=True,
                         type="primary", disabled=not ans.strip()):
                with st.spinner("Evaluating your answer..."):
                    try:
                        res  = evaluate(question, ans.strip())
                        sc   = float(res.get("score", 5))
                        st.session_state.scores.append(sc)
                        st.session_state.tips.append(res.get("improvement", ""))
                        st.session_state.strengths.append(
                            res.get("strengths", ["Clear response", "Good effort"]))
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
                    {"role": "user",      "content": "I want to skip this question."}
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
        pct = int(sc / 10 * 100)

        st.markdown(f'<div class="fb-qlabel">Question {qi+1} of 5</div>',
                    unsafe_allow_html=True)

        st.markdown(
            f'<div class="card">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
            f'<div><div style="font-size:.8rem;color:#9CA3AF">Your Score</div>'
            f'<span class="score-num {nc}">{sc}</span>'
            f'<span class="score-den">/10</span></div>'
            f'<div class="s-circle {cc}">↗</div></div>'
            f'<div style="background:#E5E7EB;border-radius:8px;height:8px;margin:10px 0">'
            f'<div style="background:{vc};border-radius:8px;height:8px;width:{pct}%">'
            f'</div></div>'
            f'<div class="verdict" style="color:{vc}">✓ {verd}</div></div>',
            unsafe_allow_html=True)

        if tip:
            st.markdown(
                f'<div class="imp-card">'
                f'<div class="imp-ico">⚡</div>'
                f'<div><div class="imp-ttl">Key Improvement</div>'
                f'<div class="imp-txt">{tip}</div></div></div>',
                unsafe_allow_html=True)

        if strs:
            items = "".join([f'<div class="dw-item">✓ {s}</div>' for s in strs])
            st.markdown(
                f'<div class="dw-card">'
                f'<div class="dw-ttl">What You Did Well</div>{items}</div>',
                unsafe_allow_html=True)

        is_last = qi >= TOTAL - 1
        lbl = "View Results" if is_last else "Next Question  →"
        if st.button(lbl, use_container_width=True, type="primary"):
            st.session_state.fb_ready  = False
            st.session_state.current_q += 1
            if st.session_state.current_q >= TOTAL:
                st.session_state.screen = "results"
            st.rerun()

        if st.button("Exit Interview", use_container_width=True):
            st.session_state.screen = "home"
            st.rerun()

# ═══════════════════════════════════════════════════════════════
#  SCREEN: RESULTS
# ═══════════════════════════════════════════════════════════════
elif st.session_state.screen == "results":

    valid = [s for s in st.session_state.scores if s > 0]
    avg   = round(sum(valid) / len(valid), 1) if valid else 0.0
    best  = max(valid) if valid else 0

    if avg >= 8:
        verd = "Excellent Performance! 🌟"
    elif avg >= 6:
        verd = "Good Effort — Keep Polishing! 👍"
    elif avg >= 4:
        verd = "Good Start — Practice More! 📈"
    else:
        verd = "Keep Practicing — You'll Improve! 💪"

    nc, cc, vc = score_cls(avg)
    pct = int(avg / 10 * 100)

    st.markdown('<div class="res-title">Session Complete! 🏆</div>',
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="res-sub">{st.session_state.field} · '
        f'{st.session_state.mode} Mode · {TOTAL} Questions</div>',
        unsafe_allow_html=True)

    st.markdown(
        f'<div class="card" style="text-align:center;padding:1.4rem">'
        f'<div style="font-size:.82rem;color:#9CA3AF">Overall Score</div>'
        f'<span class="score-num {nc}">{avg}</span>'
        f'<span class="score-den">/10</span>'
        f'<div style="background:#E5E7EB;border-radius:8px;height:8px;'
        f'margin:12px auto;max-width:200px">'
        f'<div style="background:{vc};border-radius:8px;height:8px;width:{pct}%">'
        f'</div></div>'
        f'<div style="font-size:.9rem;color:#6B7280;margin-top:6px">{verd}</div></div>',
        unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, lbl, val in [
        (c1, "Answered", len(valid)),
        (c2, "Avg Score", avg),
        (c3, "Best Score", best)
    ]:
        with col:
            st.markdown(
                f'<div class="card" style="text-align:center;padding:.9rem">'
                f'<div class="stat-label">{lbl}</div>'
                f'<div class="stat-val" style="font-size:1.3rem">{val}</div></div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Question Breakdown</div>',
                unsafe_allow_html=True)

    for i in range(len(st.session_state.scores)):
        s   = st.session_state.scores[i]
        q   = st.session_state.q_cache.get(i, f"Question {i+1}")
        tip = st.session_state.tips[i]
        lbl = f"{s}/10" if s > 0 else "Skipped"
        with st.expander(f"Q{i+1}: {q[:55]}… — {lbl}"):
            st.write(f"**Your answer:** {st.session_state.answers[i]}")
            if tip and "Skipped" not in tip:
                st.markdown(
                    f'<div class="dw-card" style="background:#FFFBEB;'
                    f'border-color:#FDE68A">'
                    f'<div style="color:#92400E;font-size:.83rem">💡 {tip}</div>'
                    f'</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:.8rem'></div>", unsafe_allow_html=True)
    if st.button("🔄  Practice Again", use_container_width=True, type="primary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init()
        st.session_state.screen = "setup"
        st.rerun()
