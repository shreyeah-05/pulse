import requests
from datetime import date

def get_weather(city = "Thiruvananthapuram"):
    """fetches today's weather as a one-line text summary"""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url,timeout = 10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"

def get_quote():
    """fetch a random motivational quote from ZenQuotes"""
    url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(url,timeout = 10)
        response.raise_for_status()
        data = response.json()
        quote = data(0)["q"]
    except Exception as e:
        return f"Weather unavailable ({e})"
    
def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime("%A, %d %B %Y")
    weather = get_weather()
    quote = get_quote()

    summary = f"""=====================================
PULSE - Daily Summary
{today}
=====================================

WEATHER
{weather}

TODAY'S QUOTE
{quote}

====================================="""

    return summary

def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()
    print(summary)  # shows in the Actions log

    # Save to a file (uploaded as a downloadable artifact)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)



print("Pulse can run successfully")

if __name__ == "__main__":
    run()