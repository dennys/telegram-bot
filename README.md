# 📊 Telegram Stock Bot

<img width="367" height="509" alt="telegram-stock-bot-demo" src="https://github.com/user-attachments/assets/b35d276e-e8a1-4a7d-be25-ffcc6ae56e31" />

A Telegram bot that sends automated daily market dashboards featuring stock prices, market indices, and foreign exchange rates. Powered by Yahoo Finance and GitHub Actions for scheduled execution.

## 🤖 AI-Assisted Generation

This project has been **100% generated with AI assistance**. The entire codebase, including the Python implementation, workflow configurations, and documentation, was created using artificial intelligence.

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

### 3. Configure GitHub Actions Variables

1. Go to your repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Add two new **repository variables** (not secrets):
   - `BOT_TOKEN`: Your Telegram bot token
   - `CHAT_ID`: Your Telegram chat ID

**Why Variables Instead of Secrets?**
- Variables are used for non-sensitive configuration values that may need to be referenced or modified frequently
- Both are encrypted and require repository access to view

### 4. Customize Stocks & Forex Rates

To modify which stocks and forex pairs the bot tracks, edit the GitHub Actions workflow file:

1. Open `.github/workflows/stock_bot.yml` (or your workflow file)
2. Locate the variable definitions or the Python script configuration
3. Update the stock symbols and forex pairs as needed:
   - **US Stocks**: Modify the stock ticker list (e.g., AAPL, NVDA, GOOGL)
   - **Taiwan Stocks**: Update Taiwan stock codes (e.g., 2330.TW, 7822.TW)
   - **Market Indices**: Add or remove indices (NASDAQ, ^DJI, ^TWII)
   - **Forex Pairs**: Change currency pairs (USD/TWD, TWD/JPY, TWD/CNY)
4. Commit and push your changes
5. The bot will use the updated configuration on the next scheduled run

### 5. Adjust Execution Schedule

To change when the bot runs:

1. Open `.github/workflows/stock_bot.yml`
2. Find the `schedule` section in the workflow
3. Update the cron expressions:
   - Current: `'15 1 * * 1-5'` (09:15 AM Taiwan time) and `'15 13 * * 1-5'` (1:15 PM Taiwan time)
   - Cron format: `minute hour day month day-of-week`
   - **Example**: Change to `'0 8 * * 1-5'` for 8:00 AM
   - Note: Times are in UTC; convert to your timezone accordingly
4. Commit and push; GitHub will apply the new schedule

### 6. Install & Run Locally (Optional)

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
```

---

Made with ❤️ using GitHub Actions and Telegram API
