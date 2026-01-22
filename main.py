#!/usr/bin/env python3
"""
Telegram Weather & News Bot
Sends daily weather updates for Lisbon and top 10 Meduza news headlines in Russian.
"""

import logging
import os
from datetime import datetime, time
from zoneinfo import ZoneInfo

import feedparser
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TIMEZONE = os.getenv("TIMEZONE", "Europe/London")
DAILY_UPDATE_TIME = os.getenv("DAILY_UPDATE_TIME", "08:00")

# Constants
LISBON_LAT = 38.7223
LISBON_LON = -9.1393
MEDUZA_RSS_URL = "https://meduza.io/rss/all"
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHERMAP_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Weather condition translations
WEATHER_CONDITIONS = {
    "clear sky": "Clear",
    "few clouds": "Partly Cloudy",
    "scattered clouds": "Cloudy",
    "broken clouds": "Cloudy",
    "overcast clouds": "Overcast",
    "shower rain": "Showers",
    "rain": "Rainy",
    "light rain": "Light Rain",
    "moderate rain": "Rain",
    "heavy intensity rain": "Heavy Rain",
    "thunderstorm": "Thunderstorm",
    "snow": "Snow",
    "mist": "Misty",
    "fog": "Foggy",
    "haze": "Hazy",
}


def get_weather_emoji(condition: str) -> str:
    """Get emoji for weather condition."""
    condition_lower = condition.lower()
    if "clear" in condition_lower or "sunny" in condition_lower:
        return "☀️"
    elif "cloud" in condition_lower or "overcast" in condition_lower:
        return "☁️"
    elif "rain" in condition_lower or "shower" in condition_lower:
        return "🌧️"
    elif "thunder" in condition_lower:
        return "⛈️"
    elif "snow" in condition_lower:
        return "❄️"
    elif "mist" in condition_lower or "fog" in condition_lower or "haze" in condition_lower:
        return "🌫️"
    else:
        return "🌤️"


def fetch_weather() -> dict | None:
    """Fetch weather data from OpenWeatherMap API."""
    try:
        # Get current weather
        current_params = {
            "lat": LISBON_LAT,
            "lon": LISBON_LON,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        current_response = requests.get(OPENWEATHERMAP_URL, params=current_params, timeout=10)
        current_response.raise_for_status()
        current_data = current_response.json()

        # Get forecast for high/low and precipitation
        forecast_params = {
            "lat": LISBON_LAT,
            "lon": LISBON_LON,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "cnt": 8  # Get 24 hours of forecast (3-hour intervals)
        }
        forecast_response = requests.get(OPENWEATHERMAP_FORECAST_URL, params=forecast_params, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Calculate high/low from forecast
        temps = [item["main"]["temp"] for item in forecast_data["list"]]
        high_temp = max(temps)
        low_temp = min(temps)

        # Get precipitation probability (max from forecast)
        precip_probs = []
        for item in forecast_data["list"]:
            if "pop" in item:
                precip_probs.append(item["pop"] * 100)
        precip_chance = max(precip_probs) if precip_probs else 0

        # Get weather condition
        condition = current_data["weather"][0]["description"]
        condition_display = WEATHER_CONDITIONS.get(condition, condition.title())

        return {
            "feels_like": round(current_data["main"]["feels_like"]),
            "high": round(high_temp),
            "low": round(low_temp),
            "precipitation": round(precip_chance),
            "condition": condition_display,
            "emoji": get_weather_emoji(condition)
        }

    except requests.RequestException as e:
        logger.error(f"Weather API error: {e}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Weather data parsing error: {e}")
        return None


def fetch_meduza_news() -> list[dict] | None:
    """Fetch top 10 news headlines from Meduza RSS feed."""
    try:
        # Use requests to fetch RSS content for better reliability
        response = requests.get(MEDUZA_RSS_URL, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.text)

        if feed.bozo and not feed.entries:
            logger.error(f"RSS feed error: {feed.bozo_exception}")
            return None

        headlines = []
        for entry in feed.entries[:10]:
            headlines.append({
                "title": entry.title,
                "link": entry.link
            })

        return headlines

    except requests.RequestException as e:
        logger.error(f"Meduza RSS request error: {e}")
        return None
    except Exception as e:
        logger.error(f"Meduza RSS parsing error: {e}")
        return None


def format_daily_message() -> str:
    """Format the daily update message."""
    tz = ZoneInfo(TIMEZONE)
    today = datetime.now(tz).strftime("%d/%m/%Y")

    message_parts = []

    # Weather section
    weather = fetch_weather()
    if weather:
        weather_section = (
            f"{weather['emoji']} Weather in Lisbon ({today})\n\n"
            f"Feels like: {weather['feels_like']}°C\n"
            f"High: {weather['high']}°C | Low: {weather['low']}°C\n"
            f"Precipitation: {weather['precipitation']}%\n"
            f"Conditions: {weather['condition']}"
        )
    else:
        weather_section = (
            f"🌤️ Weather in Lisbon ({today})\n\n"
            "⚠️ Weather data temporarily unavailable"
        )
    message_parts.append(weather_section)

    # News section
    headlines = fetch_meduza_news()
    if headlines:
        news_lines = ["📰 Meduza - Top 10 Headlines\n"]
        for i, headline in enumerate(headlines, 1):
            news_lines.append(f"{i}. [{headline['title']}]({headline['link']})")
        news_section = "\n".join(news_lines)
    else:
        news_section = "📰 Meduza - Top 10 Headlines\n\n⚠️ News data temporarily unavailable"
    message_parts.append(news_section)

    return "\n\n".join(message_parts)


async def send_daily_update(context: ContextTypes.DEFAULT_TYPE = None, chat_id: str = None) -> None:
    """Send the daily update message."""
    target_chat_id = chat_id or TELEGRAM_CHAT_ID

    if not target_chat_id:
        logger.error("No chat ID available for sending update")
        return

    message = format_daily_message()

    try:
        if context and hasattr(context, 'bot'):
            await context.bot.send_message(
                chat_id=target_chat_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        else:
            # This shouldn't happen in normal operation
            logger.error("No bot context available")
        logger.info(f"Daily update sent to {target_chat_id}")
    except Exception as e:
        logger.error(f"Failed to send daily update: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    welcome_message = (
        "👋 Welcome to the Weather & News Bot!\n\n"
        "I'll send you daily updates at 8:00 AM (UK time) with:\n"
        "• Weather forecast for Lisbon\n"
        "• Top 10 news headlines from Meduza (in Russian)\n\n"
        "Commands:\n"
        "/test - Get today's update now\n"
        "/minutely_on - Enable test mode (updates every minute)\n"
        "/minutely_off - Disable test mode\n"
        "/help - Show all commands\n\n"
        f"Your chat ID: `{update.effective_chat.id}`"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")
    logger.info(f"Start command received from chat {update.effective_chat.id}")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /test command - send immediate update."""
    await update.message.reply_text("📤 Fetching today's update...")

    message = format_daily_message()
    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info(f"Test command executed for chat {update.effective_chat.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_message = (
        "📖 Available Commands:\n\n"
        "/start - Initialize bot and show welcome message\n"
        "/test - Manually trigger today's update\n"
        "/today - Same as /test\n"
        "/minutely_on - Enable test mode (updates every minute)\n"
        "/minutely_off - Disable test mode\n"
        "/help - Show this help message\n\n"
        "📅 Automatic updates are sent daily at 8:00 AM UK time."
    )
    await update.message.reply_text(help_message)


async def scheduled_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job to run at scheduled time."""
    logger.info("Running scheduled daily update")
    if TELEGRAM_CHAT_ID:
        message = format_daily_message()
        try:
            await context.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.info(f"Daily update sent to {TELEGRAM_CHAT_ID}")
        except Exception as e:
            logger.error(f"Failed to send scheduled update: {e}")


async def minutely_on_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /minutely_on command - enable minutely updates for testing."""
    chat_id = update.effective_chat.id

    # Only allow the configured chat ID to use this
    if TELEGRAM_CHAT_ID and str(chat_id) != str(TELEGRAM_CHAT_ID):
        await update.message.reply_text("⛔ Unauthorized. This command is only available to the bot owner.")
        return

    # Check if minutely job already exists
    current_jobs = context.job_queue.get_jobs_by_name("minutely_update")
    if current_jobs:
        await update.message.reply_text("⚠️ Test mode is already enabled. Use /minutely_off to disable.")
        return

    # Add minutely job
    context.job_queue.run_repeating(
        scheduled_job,
        interval=60,  # 60 seconds
        first=5,      # Start after 5 seconds
        name="minutely_update",
        chat_id=chat_id
    )

    await update.message.reply_text(
        "✅ Test mode enabled!\n\n"
        "📨 You will now receive updates every minute.\n"
        "⏱️ First update in 5 seconds.\n\n"
        "Use /minutely_off to disable."
    )
    logger.info(f"Minutely test mode enabled for chat {chat_id}")


async def minutely_off_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /minutely_off command - disable minutely updates."""
    chat_id = update.effective_chat.id

    # Only allow the configured chat ID to use this
    if TELEGRAM_CHAT_ID and str(chat_id) != str(TELEGRAM_CHAT_ID):
        await update.message.reply_text("⛔ Unauthorized. This command is only available to the bot owner.")
        return

    # Remove all minutely jobs
    current_jobs = context.job_queue.get_jobs_by_name("minutely_update")
    if not current_jobs:
        await update.message.reply_text("⚠️ Test mode is not active.")
        return

    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text(
        "✅ Test mode disabled!\n\n"
        "📅 Automatic updates will resume at the scheduled time (8:00 AM UK time)."
    )
    logger.info(f"Minutely test mode disabled for chat {chat_id}")


def main() -> None:
    """Main function to run the bot."""
    # Validate configuration
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

    if not WEATHER_API_KEY:
        logger.error("WEATHER_API_KEY not set")
        raise ValueError("WEATHER_API_KEY environment variable is required")

    logger.info("Starting Telegram Weather & News Bot")

    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(CommandHandler("today", test_command))
    application.add_handler(CommandHandler("minutely_on", minutely_on_command))
    application.add_handler(CommandHandler("minutely_off", minutely_off_command))
    application.add_handler(CommandHandler("help", help_command))

    # Setup scheduler for daily updates using python-telegram-bot's job queue
    if TELEGRAM_CHAT_ID:
        tz = ZoneInfo(TIMEZONE)
        hour, minute = map(int, DAILY_UPDATE_TIME.split(":"))
        target_time = time(hour=hour, minute=minute, tzinfo=tz)

        application.job_queue.run_daily(
            scheduled_job,
            time=target_time,
            name="daily_update"
        )
        logger.info(f"Scheduled daily update at {DAILY_UPDATE_TIME} {TIMEZONE}")
    else:
        logger.warning("TELEGRAM_CHAT_ID not set - scheduled updates disabled")

    # Run the bot
    logger.info("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
