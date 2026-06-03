# 🛡️ BurnoutGuard AI
### Early-Warning System for Healthcare Worker Burnout

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange)
![AI](https://img.shields.io/badge/AI-Llama%203.3-green)

🌐 **Live Demo:** https://burnoutguard-ai-ibk7.onrender.com
---

## 🚨 The Problem

54% of nurses experience burnout. Healthcare worker burnout costs the US **$9 billion annually** in turnover. Enterprise tools exist but are sold to hospitals — individual workers have nothing accessible to them.

**BurnoutGuard AI fills that gap.**

---

## 🧠 What It Does

- 📋 **Weekly check-in** — 5 questions based on the Maslach Burnout Inventory (MBI)
- 📊 **Burnout score + trend chart** — tracks risk over time with colour-coded zones
- 🤖 **ML risk prediction** — logistic regression model predicts risk level in real time
- 🔮 **3-week forecast** — predicts where your burnout is heading before it hits
- 💬 **AI companion** — empathetic chat powered by Llama 3.3, with crisis safety guardrails
- 📈 **Manager dashboard** — anonymized team-level risk heatmap, no individual surveillance

---

## 🔬 Why It's Different

Most burnout tools ask "how do you feel today?" BurnoutGuard asks "where are you heading?"

The forward-looking prediction uses your personal longitudinal data — no knowledge cutoff, no generic advice. The longer you use it, the smarter it gets about you specifically.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| ML Model | scikit-learn (Logistic Regression) |
| AI Companion | Llama 3.3 via Groq API |
| Forecasting | NumPy linear trend projection |

---

## 🚀 Run Locally

git clone https://github.com/Suprigm04/BurnoutGuard-AI.git
cd BurnoutGuard-AI
pip install -r requirements.txt

Create a .env file:
GROQ_API_KEY=GROQ_API_KEY=your-groq-api-key-here

Run the app:
streamlit run app.py

---

## ⚠️ Disclaimer

This is a personal project built to explore AI in healthcare. It is not a medical device and does not constitute clinical advice. Real deployment would require clinical validation, ethics approval, and HIPAA compliance.

---

## 👩‍💻 Built By

**Supriya GM** — CS Masters student with an Information Science background, passionate about building AI tools that solve real healthcare problems.

[LinkedIn](https://www.linkedin.com/in/supriyagangadharamalebennur) | [GitHub](https://github.com/Suprigm04)