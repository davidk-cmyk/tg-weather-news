# Telegram Weather & News Bot

A Telegram bot that sends daily weather updates for Lisbon and top 10 Meduza news headlines in Russian at 8:00 AM UK time.

## Features

- Daily weather updates for Lisbon (feels-like, high/low temps, precipitation, conditions)
- Top 10 Meduza news headlines in Russian with clickable links
- Scheduled daily updates at 8:00 AM UK time
- Manual test commands for on-demand updates

## Commands

- `/start` - Initialize bot and show welcome message
- `/test` or `/today` - Manually trigger today's update
- `/help` - Show available commands

## Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Save the bot token provided

### 2. Get Your Chat ID

1. Start a chat with your new bot
2. Send `/start` to the bot
3. The bot will display your chat ID

Alternatively, use [@userinfobot](https://t.me/userinfobot) to get your chat ID.

### 3. Get OpenWeatherMap API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Navigate to API Keys in your account
3. Generate a new API key (free tier is sufficient)

### 4. Local Development

```bash
# Clone the repository
git clone https://github.com/davidk-cmyk/tg-weather-news.git
cd tg-weather-news

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor

# Run the bot
python main.py
```

### 5. Deploy to Railway

1. Create an account at [Railway](https://railway.app)
2. Connect your GitHub repository
3. Create a new project from the repository
4. Add environment variables in Railway dashboard:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `WEATHER_API_KEY`
   - `TIMEZONE` (optional, defaults to Europe/London)
   - `DAILY_UPDATE_TIME` (optional, defaults to 08:00)
5. Deploy!

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | - | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Yes | - | Your Telegram chat ID |
| `WEATHER_API_KEY` | Yes | - | OpenWeatherMap API key |
| `TIMEZONE` | No | Europe/London | Timezone for scheduled updates |
| `DAILY_UPDATE_TIME` | No | 08:00 | Time for daily updates (HH:MM) |

## Message Format

```
☀️ Weather in Lisbon (19/01/2026)

Feels like: 15°C
High: 18°C | Low: 12°C
Precipitation: 10%
Conditions: Clear

📰 Meduza - Top 10 Headlines

1. [Headline text](article_url)
2. [Headline text](article_url)
...
10. [Headline text](article_url)
```

## Tech Stack

- Python 3.x
- python-telegram-bot
- APScheduler
- requests
- feedparser
- python-dotenv

## License

MIT
