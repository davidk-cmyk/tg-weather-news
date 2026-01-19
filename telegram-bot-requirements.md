# Telegram Weather & News Bot - Requirements

## Project Overview
A simple Telegram bot that delivers daily weather updates for Lisbon and top news headlines from Meduza in Russian.

## Functional Requirements

### 1. Automated Daily Updates
- **Schedule**: Send updates once per day at 8:00 AM UK timezone
- **Content**: Weather forecast + Meduza news headlines
- **Delivery**: Direct message to the user's Telegram account

### 2. Weather Information
- **Location**: Lisbon, Portugal
- **Data Points**:
  - Feels-like temperature
  - High temperature for the day
  - Low temperature for the day
  - Precipitation chance (%)
  - Weather condition (sunny/rainy/cloudy/etc.)
- **API**: Use free, open API with simple setup (e.g., OpenWeatherMap, WeatherAPI, or similar)

### 3. Meduza News Headlines
- **Language**: Russian
- **Quantity**: Top 10 most recent articles
- **Format**: Headline + clickable link to article
- **Source**: Meduza news feed/API

### 4. Manual Testing Commands
- **Command**: `/test`, `/today`, or `/update` (choose one)
- **Behavior**: Immediately sends the same content that would be sent during the scheduled 8 AM update
- **Purpose**: Testing and verification

### 5. Bot Commands
- `/start` - Initialize bot and welcome message
- `/test` or `/today` - Manually trigger today's update
- `/help` - Show available commands

## Technical Requirements

### Technology Stack
- **Language**: Python 3.x
- **Bot Framework**: python-telegram-bot library
- **Weather API**: Free tier API (OpenWeatherMap or WeatherAPI.com)
- **News Source**: Meduza RSS feed or API
- **Scheduler**: APScheduler or similar for daily scheduled tasks

### Hosting
- **Platform**: Railway
- **Requirements**:
  - Must support scheduled tasks (always-on)
  - Environment variables for API keys and bot token
  - Python runtime support

### Configuration
Environment variables needed:
- `TELEGRAM_BOT_TOKEN` - Bot token from BotFather
- `TELEGRAM_CHAT_ID` - Your personal chat ID
- `WEATHER_API_KEY` - API key for weather service
- `TIMEZONE` - UK timezone (Europe/London)
- `DAILY_UPDATE_TIME` - 08:00

## API Requirements

### Weather API
- Free tier availability
- No credit card required for signup
- Simple REST API
- Supports:
  - Current weather conditions
  - Daily forecast (high/low)
  - Feels-like temperature
  - Precipitation probability

### Meduza News
- Access to Russian-language articles
- RSS feed or public API
- Returns at minimum:
  - Article headline
  - Article URL
  - Publication timestamp (for sorting by recency)

## Message Format

### Daily Update Message Structure
```
🌤 Weather in Lisbon (DD/MM/YYYY)

Feels like: XX°C
High: XX°C | Low: XX°C
Precipitation: XX%
Conditions: [Sunny/Rainy/Cloudy/etc.]

📰 Meduza - Top 10 Headlines

1. [Headline text](article_url)
2. [Headline text](article_url)
...
10. [Headline text](article_url)
```

## Non-Functional Requirements

### Reliability
- Bot should handle API failures gracefully
- Log errors for debugging
- Retry logic for failed API calls

### Error Handling
- If weather API fails: Send notification with error message
- If Meduza feed fails: Send notification with error message
- If partial data available: Send what's available with note about missing data

### Monitoring
- Basic logging to console/file
- Track successful/failed scheduled updates
- Log API response times

## Deliverables

1. **Source Code**
   - Python bot application
   - requirements.txt with dependencies
   - README.md with setup instructions

2. **Configuration Files**
   - .env.example with required environment variables
   - Railway deployment configuration (if needed)

3. **Documentation**
   - Setup guide for Railway deployment
   - Instructions for obtaining API keys
   - Instructions for getting Telegram bot token and chat ID

## Development Approach
- Working prototype priority
- Simple, maintainable code
- Minimal dependencies
- Easy to deploy and configure

## Out of Scope (for initial version)
- Multiple users support
- Location customization
- Update frequency changes
- Web dashboard
- Database storage
- Advanced analytics

## Success Criteria
- Bot successfully sends scheduled update at 8 AM UK time daily
- Weather data displays correctly for Lisbon
- Top 10 Meduza headlines in Russian with working links
- Manual test command works on-demand
- Deployed and running on Railway
- All features functional in production environment
