# 📊 Telegram Stock Bot

<img width="367" height="509" alt="telegram-stock-bot-demo" src="https://github.com/user-attachments/assets/b35d276e-e8a1-4a7d-be25-ffcc6ae56e31" />

A Telegram bot that sends automated daily market dashboards featuring stock prices, market indices, and foreign exchange rates. Powered by Yahoo Finance and GitHub Actions for scheduled execution.

## Features

✨ **Real-time Market Data**
- 🇺🇸 US stocks (AAPL, NVDA, GOOGL)
- 🇹🇼 Taiwan stocks (2330.TW, 7822.TW)
- 🌍 Market indices (NASDAQ, Dow Jones, Taiwan Weighted Index)
- 💱 Foreign exchange rates (USD/TWD, TWD/JPY, TWD/CNY)

📈 **Smart Analysis**
- Calculates daily percentage changes
- Sentiment indicators (🔥 very strong, 🟢 bullish, ⚪ neutral, 🔴 weak, 💀 strong down)
- AI summary with overall market mood

🤖 **Automated Delivery**
- Runs on GitHub Actions (no server needed)
- Scheduled for 2 times daily during market hours
- Mon–Fri at 09:15 AM and 1:15 PM (Taiwan time)
- Manual trigger available via workflow dispatch

## Setup

### 1. Prerequisites
- GitHub account (for Actions)
- Telegram account
- Telegram bot (create via [@BotFather](https://t.me/botfather))

### 2. Get Your Telegram Credentials

**Create a Bot:**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token**

**Get Your Chat ID:**
1. Message your bot any text
2. Visit: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
3. Replace `<BOT_TOKEN>` with your token
4. Copy your **Chat ID** from the response

### 3. Add Secrets to GitHub

1. Go to your repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Add two new secrets:
   - `BOT_TOKEN`: Your Telegram bot token
   - `CHAT_ID`: Your Telegram chat ID

### 4. Install & Run Locally (Optional)

```bash
# Clone the repository
git clone https://github.com/dennys/telegram-stock-bot.git
cd telegram-stock-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export BOT_TOKEN="your_bot_token"
export CHAT_ID="your_chat_id"

# Run the bot
python stock_bot.py
