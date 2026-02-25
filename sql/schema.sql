CREATE TABLE IF NOT EXISTS tickers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE,
    company_name TEXT,
    sector TEXT,
    industry TEXT
);

CREATE TABLE IF NOT EXISTS market_prices (
    ticker_id INTEGER,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    PRIMARY KEY (ticker_id, date)
);

CREATE TABLE IF NOT EXISTS fundamentals (
    ticker_id INTEGER,
    date TEXT,
    revenue REAL,
    net_income REAL,
    total_debt REAL,
    operating_margin REAL,
    free_cash_flow REAL,
    PRIMARY KEY (ticker_id, date)
);

CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker_id INTEGER,
    date TEXT,
    headline TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS computed_signals (
    ticker_id INTEGER,
    date TEXT,
    volatility_30d REAL,
    momentum_30d REAL,
    revenue_growth REAL,
    debt_ratio REAL,
    regime_label TEXT,
    health_score REAL,
    PRIMARY KEY (ticker_id, date)
);