import yfinance as yf
import requests
import os

# ===== ENV =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== CONFIG =====
us_stocks = ["AAPL", "NVDA", "GOOGL"]
tw_stocks = ["2330.TW", "7822.TW"]

indices = {
    "NASDAQ": "^IXIC",
    "Dow": "^DJI",
    "TWII": "^TWII"
}

# ===== FX =====
fx_pairs = {
    "USD/TWD": "USDTWD=X",
    "TWD/JPY": "TWDJPY=X",
    "TWD/CNY": "TWDCNY=X"
}

# ===== HELPERS =====
def price_fmt(symbol, price):
    if symbol.endswith(".TW") or symbol == "^TWII":
        return f"NT${price:.2f}"
    return f"${price:.2f}"

def yahoo(symbol):
    return f"https://finance.yahoo.com/quote/{symbol}/"

def md_link(name, symbol):
    return f"[{name}]({yahoo(symbol)})"

def fetch(symbol):
    t = yf.Ticker(symbol)
    d = t.history(period="2d")

    if len(d) < 2:
        raise Exception(f"Not enough data for {symbol}")

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
lines.append("🇺🇸 *US STOCKS*")

for s in us_stocks:
    try:
        price, pct = fetch(s)
        all_changes.append(pct)

        lines.append(
            f"{md_link(s, s)}  "
            f"`{price_fmt(s, price):>10}`  "
            f"`{pct:+.2f}%`  "
            f"{sentiment(pct)}"
        )

    except Exception as e:
        lines.append(f"{s} error: {e}")

# ===== TAIWAN STOCKS =====
lines.append("\n🇹🇼 *TAIWAN STOCKS*")

for s in tw_stocks:
    try:
        price, pct = fetch(s)
        all_changes.append(pct)

        lines.append(
            f"{md_link(s, s)}  "
            f"`{price_fmt(s, price):>10}`  "
            f"`{pct:+.2f}%`  "
            f"{sentiment(pct)}"
        )

    except Exception as e:
        lines.append(f"{s} error: {e}")

# ===== INDICES =====
lines.append("\n🌍 *INDICES*")

for name, symbol in indices.items():
    try:
        price, pct = fetch(symbol)
        all_changes.append(pct)

        lines.append(
            f"{md_link(name, symbol)}  "
            f"`{price_fmt(symbol, price):>10}`  "
            f"`{pct:+.2f}%`  "
            f"{sentiment(pct)}"
        )

    except Exception as e:
        lines.append(f"{name} error: {e}")

# ===== FX =====
lines.append("\n💱 *FX (TWD BASE)*")

for name, symbol in fx_pairs.items():
    try:
        price, pct = fetch(symbol)
        all_changes.append(pct)

        lines.append(
            f"{md_link(name, symbol)}  "
            f"`{price:.4f}`  "
            f"`{pct:+.2f}%`"
        )

    except Exception as e:
        lines.append(f"{name} error: {e}")

# ===== AI SUMMARY =====
avg = sum(all_changes) / len(all_changes)

if avg > 1:
    mood = "🟢 Strong bullish market"
elif avg > 0:
    mood = "🟡 Mild bullish bias"
elif avg > -1:
    mood = "⚪ Sideways market"
else:
    mood = "🔴 Risk-off environment"

text = (
    f"🧠 *AI SUMMARY*: {mood}\n\n"
    + "\n".join(lines)
)

# ===== SEND TO TELEGRAM =====
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
)
