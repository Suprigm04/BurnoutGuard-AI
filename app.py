import streamlit as st
import sqlite3
import os
import pandas as pd
import plotly.graph_objects as go
from predict_future import get_future_prediction
from datetime import date
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ── Database setup ───────────────────────────────────────────


def init_db():
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER, q5 INTEGER,
            score INTEGER,
            risk_level TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_checkin(q1, q2, q3, q4, q5, score, risk_level):
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO checkins (date, q1, q2, q3, q4, q5, score, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (str(date.today()), q1, q2, q3, q4, q5, score, risk_level))
    conn.commit()
    conn.close()


def predict_risk(q1, q2, q3, q4, q5, score):
    import pickle
    with open("burnout_model.pkl", "rb") as f:
        model = pickle.load(f)
    prediction = model.predict([[q1, q2, q3, q4, q5, score]])
    return prediction[0]

# ── AI Companion ─────────────────────────────────────────────


def get_ai_response(user_message, score, risk_level):
    crisis_words = ["suicide", "kill myself",
                    "end my life", "self harm", "hurt myself"]
    if any(word in user_message.lower() for word in crisis_words):
        return "🆘 I'm concerned about what you shared. Please reach out for help immediately:\n\n**988 Suicide & Crisis Lifeline — call or text 988**\n\nYou are not alone."

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"""You are a compassionate mental health companion for healthcare workers.
            The user just completed a burnout check-in and scored {score}/25 — {risk_level}.
            Respond with empathy, warmth and understanding. Keep responses short (2-3 sentences).
            Never give medical advice. If they seem in crisis, gently suggest professional help."""},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content


# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="BurnoutGuard AI",
    page_icon="🛡️",
    layout="centered"
)

# ── Styling ──────────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp {
        background: #f8f9fa;
    }
    h1 {
        color: #e74c3c !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
    }
    h2, h3 {
        color: #2c3e50 !important;
    }
    .stButton > button {
        background: #e74c3c;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background: #c0392b;
    }
    .stSlider > div > div {
        background: #fadbd8 !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #2c3e50 !important;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="
        background: white;
        padding: 10px 20px;
        border-bottom: 2px solid #e74c3c;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    ">
        <div style="font-size: 20px; font-weight: 900; color: #e74c3c;">
            🛡️ BurnoutGuard AI
        </div>
        <div style="display: flex; gap: 20px;">
            <a href="/" target="_self" style="
                text-decoration: none;
                color: #e74c3c;
                font-weight: 600;
                font-size: 14px;
            ">🏠 Home</a>
            <a href="/Manager_Dashboard" target="_self" style="
                text-decoration: none;
                color: #2c3e50;
                font-weight: 600;
                font-size: 14px;
            ">📊 Manager Dashboard</a>
        </div>
    </div>
""", unsafe_allow_html=True)


# ── App ──────────────────────────────────────────────────────
init_db()

st.title("🛡️ BurnoutGuard AI")
st.subheader("Weekly Check-in")
st.write("This takes 2 minutes. Your responses are private.")
st.caption("Rate each statement: 1 = Never  |  2 = Rarely  |  3 = Sometimes  |  4 = Often  |  5 = Always")

st.divider()

q1 = st.slider("I feel emotionally drained from my work.", 1, 5, 3)
q2 = st.slider("I feel used up at the end of the workday.", 1, 5, 3)
q3 = st.slider(
    "I feel tired when I get up and have to face another day at work.", 1, 5, 3)
q4 = st.slider("Working with people all day is a strain for me.", 1, 5, 3)
q5 = st.slider("I feel burned out from my work.", 1, 5, 3)

st.divider()

if st.button("Submit Check-in"):
    score = q1 + q2 + q3 + q4 + q5

    if score <= 10:
        risk_level = "Low Risk"
        message = "You're doing well. Keep checking in weekly."
        emoji = "🟢"
    elif score <= 16:
        risk_level = "Moderate Risk"
        message = "Some signs of stress. Be kind to yourself this week."
        emoji = "🟡"
    else:
        risk_level = "High Risk"
        message = "You're showing signs of burnout. Consider talking to someone you trust."
        emoji = "🔴"

    ml_prediction = predict_risk(q1, q2, q3, q4, q5, score)
    save_checkin(q1, q2, q3, q4, q5, score, risk_level)
    st.session_state["score"] = score
    st.session_state["risk_level"] = risk_level
    st.session_state["show_companion"] = True

    st.success(
        f"Check-in saved! Your score: {score}/25 — {emoji} {risk_level}")
    st.info(message)
    st.info(f"🤖 ML Model Prediction: **{ml_prediction}**")

# ── Trend Chart ──────────────────────────────────────────────
st.divider()
st.subheader("📈 Your Burnout Trend")

conn = sqlite3.connect("burnoutguard.db")
df = pd.read_sql_query(
    "SELECT date, score, risk_level FROM checkins ORDER BY date", conn)
conn.close()

if len(df) > 0:
    fig = go.Figure()
    fig.add_hrect(y0=0, y1=10, fillcolor="green", opacity=0.1, line_width=0,
                  annotation_text="🟢 Low Risk", annotation_position="left")
    fig.add_hrect(y0=10, y1=16, fillcolor="orange", opacity=0.1, line_width=0,
                  annotation_text="🟡 Moderate Risk", annotation_position="left")
    fig.add_hrect(y0=16, y1=25, fillcolor="red", opacity=0.1, line_width=0,
                  annotation_text="🔴 High Risk", annotation_position="left")
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["score"],
        mode="lines+markers",
        line=dict(color="#e74c3c", width=3),
        marker=dict(size=8),
        name="Burnout Score"
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 25], title="Burnout Score"),
        xaxis=dict(title="Week"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)
# ── Forward prediction ───────────────────────────────────────
future_scores, future_risk, trend_message = get_future_prediction()

if future_scores:
    st.divider()
    st.subheader("🔮 Your Burnout Forecast")
    st.write("Based on your trend, here's where you're heading:")

    col1, col2, col3 = st.columns(3)
    col1.metric("Week 1 Forecast", f"{future_scores[0]}/25")
    col2.metric("Week 2 Forecast", f"{future_scores[1]}/25")
    col3.metric("Week 3 Forecast", f"{future_scores[2]}/25")

    if future_risk == "High Risk":
        st.error(f"🔴 {trend_message}")
    elif future_risk == "Moderate Risk":
        st.warning(f"🟡 {trend_message}")
    else:
        st.success(f"🟢 {trend_message}")
else:
    st.info("Submit a few check-ins to see your trend.")

# ── AI Companion ─────────────────────────────────────────────
if True:
    st.divider()
    st.subheader("💬 Talk to Your AI Companion")
    st.write("How are you feeling? You can share anything here.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type here...")
    if user_input:
        st.session_state["messages"].append(
            {"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        response = get_ai_response(
            user_input, st.session_state["score"], st.session_state["risk_level"])
        st.session_state["messages"].append(
            {"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
