import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_future_prediction():
    conn = sqlite3.connect("burnoutguard.db")
    df = pd.read_sql_query(
        "SELECT date, score FROM checkins ORDER BY date", conn
    )
    conn.close()

    if len(df) < 3:
        return None, None, None

    # Convert dates and create weekly index
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = range(len(df))

    # Fit a simple linear trend
    x = df['week'].values
    y = df['score'].values
    slope = np.polyfit(x, y, 1)[0]
    last_score = y[-1]

    # Project 3 weeks forward
    future_scores = []
    for i in range(1, 4):
        projected = last_score + (slope * i)
        projected = max(5, min(25, projected))
        future_scores.append(round(projected, 1))

    # Predict risk for week 3
    week3_score = future_scores[2]
    if week3_score <= 10:
        future_risk = "Low Risk"
        trend_message = "Your burnout trend is improving. Keep it up! 🟢"
    elif week3_score <= 16:
        future_risk = "Moderate Risk"
        trend_message = "Your burnout is staying moderate. Watch your stress levels. 🟡"
    else:
        future_risk = "High Risk"
        trend_message = "⚠️ Warning: Based on your trend, you may reach critical burnout in 3 weeks. Please take action now."

    return future_scores, future_risk, trend_message
