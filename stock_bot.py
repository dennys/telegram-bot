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

if now.weekday() > 8:  # FIXED: Sat/Sun skip
    exit()

# ===== CONFIG =====
us_stocks = ["AAPL", "NVDA", "GOOGL"]
tw_stocks = ["2330.TW", "7822.TW"]

indices = {
    "NASDAQ": "^IXIC",
    "Dow": "^DJI",
    "TWII": "^TWII"
}

# ===== FX (NEW) =====
fx_pairs = {
    "TWD/USD": "TWDUSD=X",
    "TWD/CNY": "TWDCNY=X",
    "TWD/JPY": "TWDJPY=X"
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

# ===== BUILD MESSAGE =====
lines = []
all_changes = []

lines.append("📊 *MARKET DASHBOARD*\n")

# ===== US STOCKS =====
lines.append("🇺🇸 US STOCKS")

for s in us_stocks:
    price, pct = fetch(s)
    all_changes.append(pct)

    lines.append(
        f"{s}  {price_fmt(s, price):>10}  {pct:+.2f}%  ({sentiment(pct)})"
    )

# ===== TAIWAN STOCKS =====
lines.append("\n🇹🇼 TAIWAN STOCKS")

for s in tw_stocks:
    price, pct = fetch(s)
    all_changes.append(pct)

    lines.append(
        f"{s}  {price_fmt(s, price):>10}  {pct:+.2f}%  ({sentiment(pct)})"
    )

# ===== INDICES =====
lines.append("\n🌍 INDICES")

for name, symbol in indices.items():
    price, pct = fetch(symbol)
    all_changes.append(pct)

    lines.append(
        f"{name}  {price_fmt(symbol, price):>10}  {pct:+.2f}%  ({sentiment(pct)})"
    )

# ===== FX (NEW SECTION) =====
lines.append("\n💱 FX (TWD BASE)")

for name, symbol in fx_pairs.items():
    price, pct = fetch(symbol)
    all_changes.append(pct)

    lines.append(
        f"{name}  {price:.4f}  {pct:+.2f}%"
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

# ===== SEND (NO INLINE KEYBOARD) =====
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": text,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
})
