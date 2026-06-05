import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go


# ── Password Protection ──────────────────────────────────────
if "manager_auth" not in st.session_state:
    st.session_state["manager_auth"] = False

if not st.session_state["manager_auth"]:
    st.title("📊 Manager Dashboard")
    st.write("This area is restricted to managers only.")
    password = st.text_input("Enter manager password", type="password")
    if st.button("Access Dashboard"):
        if password == "manager123":
            st.session_state["manager_auth"] = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

st.set_page_config(
    page_title="BurnoutGuard — Manager View",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Manager Dashboard")
st.write("Team-level burnout overview. Individual identities are never shown.")

st.divider()

conn = sqlite3.connect("burnoutguard.db")
df = pd.read_sql_query(
    "SELECT date, score, risk_level FROM checkins ORDER BY date", conn)
conn.close()

if len(df) == 0:
    st.info("No check-in data yet.")
else:
    # ── Summary metrics ──
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Check-ins", len(df))
    col2.metric("Average Score", f"{df['score'].mean():.1f}/25")
    col3.metric("High Risk Check-ins",
                len(df[df['risk_level'] == 'High Risk']))

    st.divider()

    # ── Risk breakdown ──
    st.subheader("🧩 Team Risk Breakdown")
    risk_counts = df['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['Risk Level', 'Count']

    colors = {
        'Low Risk': '#2ecc71',
        'Moderate Risk': '#f39c12',
        'High Risk': '#e74c3c'
    }

    fig_pie = go.Figure(data=[go.Pie(
        labels=risk_counts['Risk Level'],
        values=risk_counts['Count'],
        marker=dict(colors=[colors.get(r, '#95a5a6')
                    for r in risk_counts['Risk Level']]),
        hole=0.4
    )])
    fig_pie.update_layout(paper_bgcolor="white")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # ── Trend over time ──
    st.subheader("📈 Team Burnout Trend Over Time")
    fig = go.Figure()
    fig.add_hrect(y0=0, y1=10, fillcolor="green", opacity=0.1,
                  line_width=0, annotation_text="🟢 Low", annotation_position="left")
    fig.add_hrect(y0=10, y1=16, fillcolor="orange", opacity=0.1, line_width=0,
                  annotation_text="🟡 Moderate", annotation_position="left")
    fig.add_hrect(y0=16, y1=25, fillcolor="red", opacity=0.1, line_width=0,
                  annotation_text="🔴 High", annotation_position="left")
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["score"],
        mode="lines+markers",
        line=dict(color="#e74c3c", width=3),
        marker=dict(size=8),
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 25], title="Burnout Score"),
        xaxis=dict(title="Date"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Alert ──
    high_risk_count = len(df[df['risk_level'] == 'High Risk'])
    total = len(df)
    if high_risk_count / total > 0.5:
        st.error(
            f"⚠️ Alert: More than 50% of check-ins are High Risk. Consider team-level support.")
    elif high_risk_count / total > 0.3:
        st.warning(
            f"⚠️ Warning: {high_risk_count} out of {total} check-ins are High Risk.")
    else:
        st.success("✅ Team burnout levels are within acceptable range.")
