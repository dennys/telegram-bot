import yfinance as yf
import requests
import os
from datetime import datetime
import pytz

# ===== ENV =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== TIME FILTER (Mon-Fri TW) =====
tw = pytz.timezone("Asia/Taipei")
now = datetime.now(tw)

if now.weekday() > ９:
    exit()

# ===== CONFIG =====
us_stocks = ["AAPL", "NVDA", "GOOGL"]   # TSLA -> GOOGL
tw_stocks = ["2330.TW", "7822.TW"]      # 2454.TW -> 7822.TW

indices = {
    "NASDAQ": "^IXIC",
    "Dow": "^DJI",
    "TWII": "^TWII"
}

# ===== HELPERS =====
def price_fmt(symbol, price):
    return f"NT${price:.2f}" if symbol.endswith(".TW") or symbol == "^TWII" else f"${price:.2f}"

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

# ===== BUTTON BUILDER =====
def buttons(symbol):
    return [
        [
            {"text": "📈 Chart", "url": yahoo(symbol)},
            {"text": "📰 News", "url": f"https://finance.yahoo.com/quote/{symbol}/news"},
            {"text": "⚠ Alert", "callback_data": f"alert:{symbol}"}
        ]
    ]

# ===== BUILD MESSAGE =====
lines = []
all_changes = []

lines.append("📊 *MARKET DASHBOARD*\n")

# ===== US =====
lines.append("🇺🇸 US STOCKS")

for s in us_stocks:
    price, pct = fetch(s)
    all_changes.append(pct)

    lines.append(
        f"[{s}]({yahoo(s)})  {price_fmt(s, price):>10}  {pct:+.2f}%  ({sentiment(pct)})"
    )

# ===== TW =====
lines.append("\n🇹🇼 TAIWAN STOCKS")

for s in tw_stocks:
    price, pct = fetch(s)
    all_changes.append(pct)

    lines.append(
        f"[{s}]({yahoo(s)})  {price_fmt(s, price):>10}  {pct:+.2f}%  ({sentiment(pct)})"
    )

# ===== INDICES =====
lines.append("\n🌍 INDICES")

for name, symbol in indices.items():
    price, pct = fetch(symbol)
    all_changes.append(pct)

    lines.append(
        f"[{name}]({yahoo(symbol)})  {price_fmt(symbol, price):>10}  {pct:+.2f}%  ({sentiment(pct)})"
    )

# ===== AI MARKET SENTIMENT =====
avg = sum(all_changes) / len(all_changes)

if avg > 1:
    mood = "🟢 Strong bullish market"
elif avg > 0:
    mood = "🟡 Mild bullish bias"
elif avg > -1:
    mood = "⚪ Sideways market"
else:
    mood = "🔴 Risk-off environment"

text = f"🧠 AI SUMMARY: {mood}\n\n" + "\n".join(lines)

# ===== INLINE BUTTONS (group level) =====
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
            {"text": "📊 TWII", "url": yahoo("^TWII")}
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
