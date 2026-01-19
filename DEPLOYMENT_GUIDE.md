# Deployment Guide: From Code to Live Telegram Bot

This guide takes you from having the code in your repository to a fully functional Telegram bot running in production.

**Estimated time:** 15-20 minutes

---

## Table of Contents

1. [Create Your Telegram Bot](#step-1-create-your-telegram-bot)
2. [Get Your Telegram Chat ID](#step-2-get-your-telegram-chat-id)
3. [Get OpenWeatherMap API Key](#step-3-get-openweathermap-api-key)
4. [Push Code to GitHub](#step-4-push-code-to-github)
5. [Deploy to Railway](#step-5-deploy-to-railway)
6. [Test Your Bot](#step-6-test-your-bot)
7. [Troubleshooting](#troubleshooting)

---

## Step 1: Create Your Telegram Bot

You'll create a bot using Telegram's official [@BotFather](https://t.me/BotFather).

### 1.1 Open BotFather

1. Open Telegram (mobile app or desktop)
2. Search for `@BotFather` in the search bar
3. Verify it has a **blue checkmark** (official account)
4. Click **Start** to begin

### 1.2 Create a New Bot

1. Send the command:
   ```
   /newbot
   ```

2. BotFather will ask: **"How are we going to call it?"**
   - Enter a display name (e.g., `Weather News Bot`)
   - This is what users see as the bot's name

3. BotFather will ask: **"Choose a username for your bot"**
   - Enter a unique username ending in `bot` (e.g., `my_weather_news_bot`)
   - Username must be unique across all of Telegram
   - Can contain letters, numbers, and underscores

4. **Save your bot token!**
   - BotFather will respond with something like:
     ```
     Done! Congratulations on your new bot. You will find it at t.me/my_weather_news_bot.

     Use this token to access the HTTP API:
     1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
     ```
   - **Copy and save this token securely** - you'll need it later
   - Never share this token publicly or commit it to Git

### 1.3 Configure Bot Commands (Optional but Recommended)

1. In BotFather, send:
   ```
   /mybots
   ```

2. Select your bot from the list

3. Click **Edit Bot** → **Edit Commands**

4. Send this message to set up command hints:
   ```
   start - Initialize bot and show welcome
   test - Get today's weather and news update
   today - Same as test
   help - Show available commands
   ```

5. Users will now see these commands when typing `/` in your bot

---

## Step 2: Get Your Telegram Chat ID

The bot needs your Chat ID to send you scheduled messages.

### Option A: Use the Bot Itself (After Deployment)

1. After deploying, send `/start` to your bot
2. The bot will display your Chat ID

### Option B: Use @userinfobot (Recommended - Do This Now)

1. Open Telegram and search for `@userinfobot`
2. Click **Start**
3. The bot will immediately reply with your user info:
   ```
   Id: 123456789
   First: YourName
   Lang: en
   ```
4. **Save the `Id` number** - this is your Chat ID

### Option C: Use @RawDataBot

1. Search for `@RawDataBot` on Telegram
2. Send any message
3. Look for `"id":` in the response - that's your Chat ID

---

## Step 3: Get OpenWeatherMap API Key

### 3.1 Create Account

1. Go to [OpenWeatherMap](https://openweathermap.org/)
2. Click **Sign In** → **Create an Account**
3. Fill in:
   - Username
   - Email
   - Password
4. Agree to terms and click **Create Account**
5. Verify your email (check spam folder if needed)

### 3.2 Get Your API Key

1. Log in to [OpenWeatherMap](https://home.openweathermap.org/)
2. Go to **API Keys** tab (or visit https://home.openweathermap.org/api_keys)
3. You'll see a default API key already generated
4. **Copy this API key** and save it

### 3.3 Important Notes

- New API keys take **up to 2 hours** to activate
- Free tier includes **1,000 calls/day** - more than enough for this bot
- No credit card required for the free tier

---

## Step 4: Push Code to GitHub

If your code isn't already on GitHub:

### 4.1 Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click **+** → **New repository**
3. Name it (e.g., `tg-weather-news`)
4. Keep it **Public** or **Private** (Railway works with both)
5. **Don't** initialize with README (you already have files)
6. Click **Create repository**

### 4.2 Push Your Code

In your terminal, navigate to your project folder and run:

```bash
cd /path/to/tg-weather-news

# Initialize git if not already done
git init

# Add all files (except sensitive ones)
git add .

# Create initial commit
git commit -m "Initial commit: Telegram Weather & News Bot"

# Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USERNAME/tg-weather-news.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4.3 Verify Upload

1. Refresh your GitHub repository page
2. Confirm these files are present:
   - `main.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `README.md`
   - `.env.example`

---

## Step 5: Deploy to Railway

Railway is a cloud platform that makes deployment simple.

### 5.1 Create Railway Account

1. Go to [Railway](https://railway.app/)
2. Click **Login** → **Login with GitHub**
3. Authorize Railway to access your GitHub

### 5.2 Create New Project

1. Click **New Project** (or **+ New** button)
2. Select **Deploy from GitHub repo**
3. Find and select your `tg-weather-news` repository
   - If you don't see it, click **Configure GitHub App** to grant access
4. Railway will automatically detect it's a Python project

### 5.3 Add Environment Variables

**This is the most important step!**

1. Click on your deployed service (the purple box)
2. Go to **Variables** tab
3. Click **+ New Variable** and add each of these:

| Variable Name | Value |
|--------------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather (e.g., `1234567890:ABCdef...`) |
| `TELEGRAM_CHAT_ID` | Your Chat ID from Step 2 (e.g., `123456789`) |
| `WEATHER_API_KEY` | Your OpenWeatherMap API key |
| `TIMEZONE` | `Europe/London` |
| `DAILY_UPDATE_TIME` | `08:00` |

4. After adding all variables, Railway will automatically redeploy

### 5.4 Verify Deployment

1. Go to **Deployments** tab
2. Wait for the deployment to show **Success** (green checkmark)
3. Click on the deployment to see logs
4. Look for:
   ```
   Starting Telegram Weather & News Bot
   Scheduled daily update at 08:00 Europe/London
   Bot is running...
   ```

### 5.5 Keep Bot Running 24/7

Railway's free tier has usage limits. For production:

1. Go to **Settings** → **Subscription**
2. Consider upgrading to **Hobby** plan ($5/month) for:
   - No sleep after inactivity
   - More execution hours
   - Better reliability

Alternatively, free tier works but may sleep after periods of inactivity.

---

## Step 6: Test Your Bot

### 6.1 Test Commands

1. Open Telegram
2. Search for your bot by its username (e.g., `@my_weather_news_bot`)
3. Click **Start**
4. You should see:
   ```
   👋 Welcome to the Weather & News Bot!

   I'll send you daily updates at 8:00 AM (UK time) with:
   • Weather forecast for Lisbon
   • Top 10 news headlines from Meduza (in Russian)

   Commands:
   /test - Get today's update now
   /help - Show this help message

   Your chat ID: 123456789
   ```

### 6.2 Test Daily Update

1. Send `/test` to the bot
2. You should receive:
   ```
   📤 Fetching today's update...

   ☀️ Weather in Lisbon (19/01/2026)

   Feels like: 15°C
   High: 18°C | Low: 12°C
   Precipitation: 10%
   Conditions: Clear

   📰 Meduza - Top 10 Headlines

   1. [Headline in Russian](https://meduza.io/...)
   2. ...
   ```

### 6.3 Verify Scheduled Updates

- Wait until 8:00 AM UK time
- Or temporarily change `DAILY_UPDATE_TIME` in Railway to a time 2-3 minutes from now
- Check Railway logs to confirm the scheduled job runs

---

## Troubleshooting

### Bot doesn't respond

1. Check Railway deployment status (should be green)
2. Check Railway logs for errors
3. Verify `TELEGRAM_BOT_TOKEN` is correct (no extra spaces)
4. Make sure you started a chat with the bot first

### Weather data shows "temporarily unavailable"

1. OpenWeatherMap API keys take up to 2 hours to activate
2. Verify `WEATHER_API_KEY` is correct
3. Check Railway logs for specific error messages

### News data shows "temporarily unavailable"

1. Check if Meduza.io is accessible from your region
2. Check Railway logs for RSS fetch errors

### Scheduled updates not working

1. Verify `TELEGRAM_CHAT_ID` is set correctly
2. Check the timezone is `Europe/London`
3. Look at Railway logs at 8:00 AM UK time for job execution

### Railway deployment fails

1. Check that `requirements.txt` exists and is valid
2. Ensure `Procfile` contains: `worker: python main.py`
3. Check build logs for specific errors

### "No module named X" error

1. Ensure all dependencies are in `requirements.txt`
2. Try redeploying by clicking **Redeploy** in Railway

---

## Quick Reference: Your Credentials

Keep this filled out (store securely, not in Git):

```
TELEGRAM_BOT_TOKEN=________________
TELEGRAM_CHAT_ID=________________
WEATHER_API_KEY=________________
```

---

## Next Steps (Optional Enhancements)

Once your bot is running:

1. **Custom commands** - Add more commands via BotFather
2. **Profile picture** - Set a bot avatar via BotFather (`/mybots` → Edit Bot → Edit Botpic)
3. **Description** - Add bot description (`/mybots` → Edit Bot → Edit Description)
4. **Multiple users** - Modify code to support multiple chat IDs
5. **Custom location** - Add commands to change the weather location

---

## Resources

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots/tutorial)
- [Railway Documentation](https://docs.railway.app/)
- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [python-telegram-bot Library](https://python-telegram-bot.readthedocs.io/)

---

**Congratulations!** Your Weather & News Bot is now live on Telegram! 🎉
