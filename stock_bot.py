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

# ===== DATA =====
us_stocks = ["AAPL", "NVDA", "TSLA"]
tw_stocks = ["2330.TW", "2454.TW"]

indices = {
    "NASDAQ": "^IXIC",
    "Dow": "^DJI",
    "TWII": "^TWII"
}

# ===== HELPERS =====

def price_fmt(symbol, price):
    return f"NT${price:.2f}" if symbol.endswith(".TW") else f"${price:.2f}"

def link(symbol, text):
    return f"[{text}](https://finance.yahoo.com/quote/{symbol}/)"

def fetch(symbol):
    t = yf.Ticker(symbol)
    d = t.history(period="2d")
    latest = d["Close"].iloc[-1]
    prev = d["Close"].iloc[-2]
    pct = ((latest - prev) / prev) * 100
    return latest, pct

# ===== AI SENTIMENT ENGINE (v2) =====

all_changes = []

def add_row(symbol):
    price, pct = fetch(symbol)
    all_changes.append(pct)

    return f"{link(symbol, symbol):<10} {price_fmt(symbol, price):>10} {pct:+.2f}%"

# ===== BUILD MESSAGE =====

msg = []

# --- AI SUMMARY ---
avg = sum(all_changes) / len(all_changes) if all_changes else 0

if avg > 1:
    mood = "🟢 Strong bullish momentum"
elif avg > 0:
    mood = "🟡 Mild positive bias"
elif avg > -1:
    mood = "⚪ Sideways market"
else:
    mood = "🔴 Risk-off / bearish pressure"

msg.append(f"📊 *MARKET DASHBOARD*\n")
msg.append(f"🧠 AI: {mood}\n")

# --- US STOCKS ---
msg.append("🇺🇸 US STOCKS")
for s in us_stocks:
    msg.append(add_row(s))

msg.append("\n🇹🇼 TAIWAN STOCKS")
for s in tw_stocks:
    msg.append(add_row(s))

msg.append("\n🌍 INDICES")
for name, symbol in indices.items():
    msg.append(add_row(symbol))

text = "\n".join(msg)

# ===== SEND =====
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": text,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
})
