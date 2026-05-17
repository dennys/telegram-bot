import yfinance as yf
import requests
import os
from datetime import datetime
import pytz

# ===== ENV =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== TIME FILTER (Mon-Fri Taiwan) =====
tw = pytz.timezone("Asia/Taipei")
now = datetime.now(tw)

if now.weekday() > 4:
    print("Weekend skip")
    exit()

# ===== CONFIG =====
us_stocks = ["AAPL", "NVDA", "GOOGL"]
tw_stocks = ["2330.TW", "7822.TW"]

indices = {
    "NASDAQ": "^IXIC",
    "Dow": "^DJI",
    "TWII": "^TWII"
}

# ===== HELPERS =====
def yahoo(symbol):
    return f"https://finance.yahoo.com/quote/{symbol}/"

def fetch(symbol):
    t = yf.Ticker(symbol)
    d = t.history(period="2d")

    latest = d["Close"].iloc[-1]
    prev = d["Close"].iloc[-2]

    pct = ((latest - prev) / prev) * 100
    return latest, pct

def sentiment(pct):
    if pct > 2:
        return "🔥 very strong"
    elif pct > 0.5:
        return "🟢 bullish"
    elif pct > -0.5:
        return "⚪ neutral"
    elif pct > -2:
        return "🔴 weak"
    else:
        return "💀 strong down"

def format_price(symbol, price):
    if symbol.endswith(".TW") or symbol == "^TWII":
        return f"NT${price:.2f}"
    return f"${price:.2f}"

# ===== BUILD SENTIMENT =====
changes = []

def collect(symbol):
    price, pct = fetch(symbol)
    changes.append(pct)
    return pct

# ===== PRE-CALC MARKET =====
for s in us_stocks + tw_stocks:
    collect(s)

for _, s in indices.items():
    collect(s)

avg = sum(changes) / len(changes)

if avg > 1:
    mood = "🟢 Strong bullish market"
elif avg > 0:
    mood = "🟡 Mild bullish bias"
elif avg > -1:
    mood = "⚪ Sideways market"
else:
    mood = "🔴 Risk-off environment"

# ===== CLEAN UI TEXT (NO TABLES) =====
text = f"""🧠 AI MARKET SUMMARY
{mood}

📊 Watchlist updated (use buttons below)
"""

# ===== INLINE BUTTONS =====
keyboard = {
    "inline_keyboard": [
        [
            {"text": "📈 AAPL", "url": yahoo("AAPL")},
            {"text": "📈 NVDA", "url": yahoo("NVDA")},
            {"text": "📈 GOOGL", "url": yahoo("GOOGL")}
        ],
        [
            {"text": "📈 2330", "url": yahoo("2330.TW")},
            {"text": "📈 7822", "url": yahoo("7822.TW")}
        ],
        [
            {"text": "📊 NASDAQ", "url": yahoo("^IXIC")},
            {"text": "📊 TWII", "url": yahoo("^TWII")},
            {"text": "📊 Dow", "url": yahoo("^DJI")}
        ]
    ]
}

# ===== SEND =====
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": text,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True,
    "reply_markup": keyboard
})
