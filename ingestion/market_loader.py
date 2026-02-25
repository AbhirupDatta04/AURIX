""" 🧠 Market Loader Design
This module must:
Accept ticker symbol
Insert into tickers table if not exists
Fetch historical price data
Insert into market_prices
Avoid duplicate inserts
Be reusable """

import yfinance as yf
import sqlite3
from datetime import datetime


DB_PATH = "aurix.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def upsert_ticker(ticker_symbol, company_name=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO tickers (ticker, company_name)
        VALUES (?, ?)
        """,
        (ticker_symbol.upper(), company_name),
    )

    conn.commit()
    conn.close()


def get_ticker_id(ticker_symbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tickers WHERE ticker = ?",
        (ticker_symbol.upper(),),
    )

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def load_market_data(ticker_symbol, period="5y"):
    ticker_symbol = ticker_symbol.upper()

    print(f"Fetching market data for {ticker_symbol}...")

    stock = yf.Ticker(ticker_symbol)
    df = stock.history(period=period)

    if df.empty:
        print("No data found.")
        return

    upsert_ticker(ticker_symbol, stock.info.get("longName"))
    ticker_id = get_ticker_id(ticker_symbol)

    conn = get_connection()
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT OR IGNORE INTO market_prices
            (ticker_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticker_id,
                index.strftime("%Y-%m-%d"),
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"],
            ),
        )

    conn.commit()
    conn.close()

    print(f"Market data loaded for {ticker_symbol}.")