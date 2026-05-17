import yfinance as yf
import requests
import os
from datetime import datetime
import pytz

# ===== ENV =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== CONFIG =====
stocks = [
    "AAPL",
    "NVDA",
    "TSLA",
    "2330.TW",
    "7822.TW"
]

# ===== TIME CHECK (Taiwan Mon-Fri ONLY) =====
tw = pytz.timezone("Asia/Taipei")
now = datetime.now(tw)

# weekday(): Mon=0 ... Sun=6
if now.weekday() > 4:
    print("Weekend - skip execution")
    exit()

# ===== FORMAT PRICE =====
def format_price(symbol, price):
    if symbol.endswith(".TW"):
        return f"NT${price:.2f}"
    return f"${price:.2f}"

# ===== FETCH DATA =====
messages = []

for symbol in stocks:
    stock = yf.Ticker(symbol)
    data = stock.history(period="2d")

    latest = data["Close"].iloc[-1]
    previous = data["Close"].iloc[-2]

    pct = ((latest - previous) / previous) * 100

    messages.append(
        f"{symbol}: {format_price(symbol, latest)} ({pct:+.2f}%)"
    )

text = "\n".join(messages)

# ===== SEND TO TELEGRAM =====
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": text
})
