import os
import smtplib
from email.mime.text import MIMEText
import requests

def get_weather():
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        return "Weather Data: Error (Missing API Key)"
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Thiruvananthapuram&appid={api_key}&units=metric"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"Weather: {temp}°C, {desc.capitalize()}"
    except Exception:
        return "Weather Data: Temporarily unavailable"

def get_daily_fact():
    try:
        url = "https://uselessfacts.jsph.pl/api/v2/facts/today"
        response = requests.get(url).json()
        return f"Daily Fact: {response['text']}"
    except Exception:
        return "Daily Fact: Could not fetch today's fact"

def send_email(summary_text):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")  # Gmail App Password
    receiver = os.environ.get("EMAIL_RECEIVER")

    msg = MIMEText(summary_text)
    msg["Subject"] = "Pulse - Daily Summary"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    print("Email sent.")

def build_summary():
    weather_data = get_weather()
    fact_data = get_daily_fact()
    
    summary = f"--- PULSE DAILY DIGEST ---\n\n{weather_data}\n\n{fact_data}\n"
    
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
        
    send_email(summary)

if __name__ == "__main__":
    build_summary()