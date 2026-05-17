import yfinance as yf
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

stocks = [
    "AAPL",
    "NVDA",
    "TSLA",
    "2330.TW",
    "7822.TW"
]

messages = []

for symbol in stocks:
    stock = yf.Ticker(symbol)
    data = stock.history(period="2d")

    latest = data["Close"].iloc[-1]
    previous = data["Close"].iloc[-2]

    pct = ((latest - previous) / previous) * 100

    messages.append(
        f"{symbol}: ${latest:.2f} ({pct:+.2f}%)"
    )

text = "\n".join(messages)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": text
})