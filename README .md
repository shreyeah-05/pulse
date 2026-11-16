# Pulse

A small Python bot that emails you a **daily digest** with the current weather and a random fact. It runs on a schedule using **GitHub Actions**, so there is no server to keep running.

## What it does

Every day at **8:00 AM IST** (02:30 UTC), the workflow:

1. Fetches the current weather for **Thiruvananthapuram** from the [OpenWeatherMap](https://openweathermap.org/api) API (temperature in °C and a short description).
2. Fetches the fact of the day from the [Useless Facts](https://uselessfacts.jsph.pl/) API.
3. Builds a plain-text summary and saves it as `daily_summary.txt`.
4. Emails the summary through Gmail (SMTP over SSL).
5. Uploads `daily_summary.txt` as a workflow artifact, so you can also read it from the Actions run.

Example email:

```
--- PULSE DAILY DIGEST ---

Weather: 29.4°C, Scattered clouds

Daily Fact: <the fact of the day>
```

If the weather or fact request fails, the digest shows a short fallback message instead of crashing.

## Project structure

```
pulse/
├── bot.py                      # Fetches data, builds the summary, sends the email
├── requirements.txt            # Python dependencies (requests)
└── .github/workflows/daily.yml # Daily schedule and manual trigger
```

## Setup

### 1. Get the credentials

- **Weather API key:** create a free account at OpenWeatherMap and copy your API key. New keys can take a little while to activate.
- **Gmail App Password:** turn on 2-Step Verification for the sending Gmail account, then create an App Password in your Google account settings. Use this instead of your normal password.

### 2. Add GitHub secrets

In your repo, go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret | Value |
|---|---|
| `WEATHER_API_KEY` | Your OpenWeatherMap API key |
| `EMAIL_SENDER` | Gmail address the digest is sent from |
| `EMAIL_PASSWORD` | The Gmail App Password |
| `EMAIL_RECEIVER` | Address that receives the digest (can be the same as the sender) |

### 3. Run it

- It runs automatically every day on the schedule.
- To test straight away, open the **Actions** tab, choose **Pulse - Daily Summary Bot**, and click **Run workflow**.

## Run locally

```bash
pip install -r requirements.txt

export WEATHER_API_KEY="your_key"
export EMAIL_SENDER="you@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export EMAIL_RECEIVER="you@gmail.com"

python bot.py
```

On Windows PowerShell, use `$env:WEATHER_API_KEY="your_key"` instead of `export`.

## Customising

- **City:** change `Thiruvananthapuram` in the weather URL in `bot.py`.
- **Send time:** edit the `cron` line in `.github/workflows/daily.yml`. GitHub uses UTC, so IST is UTC+5:30. Scheduled runs can start a few minutes late.
- **More content:** add a function in `bot.py` (news headlines, a quote, a to-do reminder) and include its result in `build_summary()`.

## Notes

- Never commit API keys or passwords. Keep them in GitHub secrets.
- GitHub may pause scheduled workflows in repositories with no activity for 60 days. If the emails stop, re-enable the workflow from the Actions tab.
- Free-tier APIs have rate limits, which are far above one request a day.
