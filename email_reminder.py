import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def get_all_users():
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users


def get_last_checkin(username):
    conn = sqlite3.connect("burnoutguard.db")
    c = conn.cursor()
    c.execute("""
        SELECT date, score, risk_level 
        FROM checkins 
        WHERE username = ? 
        ORDER BY date DESC LIMIT 1
    """, (username,))
    result = c.fetchone()
    conn.close()
    return result


def send_reminder_email(to_email, username, last_score=None, risk_level=None):
    sender_email = "your-gmail@gmail.com"
    sender_password = "your-app-password"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "⏰ Time for your weekly BurnoutGuard check-in"
    msg["From"] = sender_email
    msg["To"] = to_email

    if last_score:
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #e74c3c;">🛡️ BurnoutGuard AI</h2>
            <p>Hi {username},</p>
            <p>Time for your weekly burnout check-in. It only takes 2 minutes.</p>
            <p>Your last score was <strong>{last_score}/25</strong> — <strong>{risk_level}</strong></p>
            <p>Tracking weekly helps catch burnout before it hits.</p>
            <a href="http://localhost:8501" style="
                background: #e74c3c;
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
            ">Take My Check-in →</a>
            <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
                BurnoutGuard AI — Not a medical tool. If you're in crisis call 988.
            </p>
        </body>
        </html>
        """
    else:
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #e74c3c;">🛡️ BurnoutGuard AI</h2>
            <p>Hi {username},</p>
            <p>Time for your weekly burnout check-in. It only takes 2 minutes.</p>
            <a href="http://localhost:8501" style="
                background: #e74c3c;
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
            ">Take My Check-in →</a>
            <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
                BurnoutGuard AI — Not a medical tool. If you're in crisis call 988.
            </p>
        </body>
        </html>
        """

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
