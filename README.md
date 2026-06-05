```markdown

\# 📊 Financial Data Pipeline — NASDAQ Historical Stock Data



\[!\[Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat\&logo=python\&logoColor=white)](https://www.python.org/)

\[!\[Yahoo Finance](https://img.shields.io/badge/Data%20Source-Yahoo%20Finance-6001D2?style=flat\&logo=yahoo\&logoColor=white)](https://finance.yahoo.com/)

\[!\[License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

\[!\[Google Colab](https://img.shields.io/badge/Google%20Colab-Ready-F9AB00?style=flat\&logo=googlecolab\&logoColor=white)](https://colab.research.google.com/)



A comprehensive Python pipeline for downloading, processing and analyzing historical stock market data from NASDAQ-listed companies. Extracts OHLCV prices, dividend history, market capitalization, and computes \*\*55+ technical indicators\*\* organized in a structured directory hierarchy.



\---



\## 📋 Table of Contents



\- \[Project Structure](#-project-structure)

\- \[Key Features](#-key-features)

\- \[Quick Start](#-quick-start)

\- \[Data Dictionary](#-data-dictionary)

&#x20; - \[Stock Prices](#stock-prices)

&#x20; - \[Dividends \& Corporate Actions](#dividends--corporate-actions)

&#x20; - \[Market Capitalization](#market-capitalization)

&#x20; - \[Technical Indicators](#technical-indicators)

\- \[Usage Examples](#-usage-examples)

\- \[Technical Indicators Reference](#-technical-indicators-reference)

\- \[Limitations](#-limitations)

\- \[License](#-license)



\---



\## 📁 Project Structure



```

financial-data-pipeline/

│

├── data/

│   └── nasdaq-listed-symbols.csv        # NASDAQ ticker symbols

│

├── scripts/

│   ├── download\_cotacoes.py             # OHLCV price downloader

│   ├── download\_indicadores.py          # Technical indicators calculator

│   └── pipeline\_completo.py             # Unified extraction pipeline

│

├── historicos/

│   ├── cotacoes/                        # Daily OHLCV prices

│   │   └── {TICKER}.csv

│   ├── dividendos/                      # Dividend history \& metrics

│   │   └── {TICKER}.csv

│   ├── valor\_mercado/                   # Historical market cap

│   │   └── {TICKER}.csv

│   └── indicadores/

│       ├── rsi/                         # Relative Strength Index

│       ├── macd/                        # MACD

│       ├── bollinger/                   # Bollinger Bands

│       ├── fibonacci/                   # Fibonacci Retracement

│       ├── medias\_moveis/               # Moving Averages

│       ├── volatilidade/                # Volatility \& Returns

│       └── tendencia/                   # Trends \& Signals

│

├── resumo\_dividendos.csv                # Consolidated dividend summary

├── resumo\_valor\_mercado.csv             # Consolidated market cap

└── symbols\_valid.csv                    # Successfully processed tickers

```



\---



\## 🚀 Key Features



\### 📈 Historical Stock Prices

\- \*\*Full OHLCV\*\*: Open, High, Low, Close, Adjusted Close, Volume

\- \*\*Configurable Range\*\*: Default from 2016-01-01 to present

\- \*\*Scalable\*\*: Supports 5,000+ NASDAQ symbols

\- \*\*Precision\*\*: Prices rounded to 2 decimal places, Volume as integer



\### 💰 Dividends \& Corporate Actions

\- Complete dividend payment history (ex-dividend dates and amounts)

\- \*\*Dividend Yield\*\*, \*\*Dividend Rate\*\*, \*\*Payout Ratio\*\*

\- Trailing 12-month total dividends and payment count

\- Upcoming ex-dividend date

\- Stock split history with adjustment ratios



\### 🏢 Market Capitalization

\- \*\*Daily Market Cap\*\* = Closing Price × Shares Outstanding

\- Automatic adjustment for historical stock splits

\- Dollar-denominated trading volume

\- Market cap in billions for readability

\- Daily percentage change



\### 📊 Technical Indicators (55+ metrics)



| Category | Indicators | Key Signals |

|----------|-----------|-------------|

| \*\*Moving Averages\*\* | MA-7, MA-14, MA-30, MA-50, MA-200 | Golden Cross / Death Cross |

| \*\*RSI\*\* | RSI-7, RSI-14 | Overbought (>70) / Oversold (<30) |

| \*\*MACD\*\* | MACD Line, Signal Line, Histogram | Bullish / Bearish Crossovers |

| \*\*Bollinger Bands\*\* | Upper, Middle, Lower, Bandwidth | Price at Upper/Lower Band |

| \*\*Fibonacci\*\* | 9 Retracement Levels (0% to 161.8%) | Support/Resistance Zones, Confluence |

| \*\*Volatility\*\* | Daily Returns, 20-Day Volatility, Range, Gap | Volume Ratio, Gap Analysis |

| \*\*Trend\*\* | 7-Day \& 50-Day Direction, Trend Strength | Consecutive Bullish Candles |



\---



\## 🔧 Quick Start



\### Prerequisites



```bash

pip install yfinance pandas numpy

```



\### Installation



```bash

git clone https://github.com/your-username/financial-data-pipeline.git

cd financial-data-pipeline

```



\### Basic Usage



```python

\# Run the complete pipeline

python scripts/pipeline\_completo.py



\# Or run individual components

python scripts/download\_cotacoes.py      # Prices only

python scripts/download\_indicadores.py   # Indicators only

```



\### Configuration



Edit the following parameters in any script:



```python

offset = 0              # Starting index in symbol list

limit = 100             # Number of symbols to process

start\_date = '2016-01-01'  # Historical start date

```



\---



\## 📊 Data Dictionary



\### Stock Prices

\*\*Location:\*\* `historicos/cotacoes/{TICKER}.csv`



| # | Field | Type | Example | Description |

|---|-------|------|---------|-------------|

| 1 | `Date` | `date` | 2024-01-15 | Trading day (YYYY-MM-DD) |

| 2 | `Open` | `decimal(2)` | 185.50 | Opening price |

| 3 | `High` | `decimal(2)` | 188.75 | Highest price of the day |

| 4 | `Low` | `decimal(2)` | 184.20 | Lowest price of the day |

| 5 | `Close` | `decimal(2)` | 187.30 | Closing price |

| 6 | `Adj Close` | `decimal(2)` | 187.30 | Adjusted close (splits \& dividends) |

| 7 | `Volume` | `integer` | 52,456,700 | Shares traded |



> \*\*Note:\*\* Use `Adj Close` for accurate return calculations as it accounts for corporate actions.



\### Dividends \& Corporate Actions

\*\*Location:\*\* `historicos/dividendos/{TICKER}.csv`



| # | Field | Type | Example | Description |

|---|-------|------|---------|-------------|

| 1 | `Date` | `date` | 2024-03-15 | Event date |

| 2 | `Dividends` | `decimal(4)` | 0.2500 | Dividend per share |

| 3 | `Stock\_Splits` | `decimal(4)` | 2.0000 | Split ratio (2.0 = 2:1 split) |

| 4 | `Dividend\_Yield` | `decimal(2)` | 2.50 | Annual dividend yield (%) |

| 5 | `Dividend\_Rate` | `decimal(2)` | 1.00 | Estimated annual dividend per share ($) |

| 6 | `Payout\_Ratio` | `decimal(2)` | 35.00 | Earnings paid as dividends (%) |

| 7 | `Dividend\_1Y\_Total` | `decimal(4)` | 1.0000 | Total dividends (trailing 12 months) |

| 8 | `Dividend\_1Y\_Count` | `integer` | 4 | Number of payments (12 months) |

| 9 | `Last\_Dividend` | `decimal(4)` | 0.2500 | Most recent dividend amount |

| 10 | `Ex\_Dividend\_Date` | `date` | 2024-06-15 | Next ex-dividend date |



\### Market Capitalization

\*\*Location:\*\* `historicos/valor\_mercado/{TICKER}.csv`



| # | Field | Type | Example | Description |

|---|-------|------|---------|-------------|

| 1 | `Date` | `date` | 2024-01-15 | Trading day |

| 2 | `Close` | `decimal(2)` | 187.30 | Closing price |

| 3 | `Shares\_Outstanding` | `integer` | 15,500,000,000 | Total shares outstanding |

| 4 | `Market\_Cap` | `decimal(2)` | 2,903,150,000,000 | Market capitalization ($) |

| 5 | `Market\_Cap\_B` | `decimal(2)` | 2903.15 | Market cap in billions ($B) |

| 6 | `Market\_Cap\_Change\_Pct` | `decimal(2)` | 1.25 | Daily change (%) |

| 7 | `Volume\_Dollar` | `decimal(2)` | 9,825,345,100 | Dollar volume traded ($) |



\### Technical Indicators



\#### RSI — Relative Strength Index

\*\*Location:\*\* `historicos/indicadores/rsi/{TICKER}.csv`



| # | Field | Type | Range/Values | Description |

|---|-------|------|--------------|-------------|

| 1 | `Date` | `date` | YYYY-MM-DD | Trading day |

| 2 | `RSI\_7` | `decimal(2)` | 0–100 | 7-period RSI (faster signal) |

| 3 | `RSI\_14` | `decimal(2)` | 0–100 | 14-period RSI (standard) |

| 4 | `RSI\_Sinal` | `text` | Sobrecomprado / Neutro / Sobrevendido | >70 = Overbought, <30 = Oversold |



\#### MACD — Moving Average Convergence Divergence

\*\*Location:\*\* `historicos/indicadores/macd/{TICKER}.csv`



| # | Field | Type | Description |

|---|-------|------|-------------|

| 1 | `Date` | `date` | Trading day |

| 2 | `MACD\_Line` | `decimal(2)` | MACD line (EMA-12 − EMA-26) |

| 3 | `MACD\_Signal` | `decimal(2)` | Signal line (EMA-9 of MACD) |

| 4 | `MACD\_Histogram` | `decimal(2)` | Histogram (MACD − Signal) |

| 5 | `MACD\_Sinal` | `text` | Compra (Bullish) / Neutro / Venda (Bearish) |



\#### Bollinger Bands

\*\*Location:\*\* `historicos/indicadores/bollinger/{TICKER}.csv`



| # | Field | Type | Description |

|---|-------|------|-------------|

| 1 | `Date` | `date` | Trading day |

| 2 | `BB\_Upper` | `decimal(2)` | Upper band (+2 standard deviations) |

| 3 | `BB\_Middle` | `decimal(2)` | 20-day Simple Moving Average |

| 4 | `BB\_Lower` | `decimal(2)` | Lower band (−2 standard deviations) |

| 5 | `BB\_Width` | `decimal(2)` | Band width (%) — low = squeeze, high = expansion |

| 6 | `BB\_Position` | `decimal(2)` | 0 = at Lower, 1 = at Upper |

| 7 | `BB\_Sinal` | `text` | Sobrecomprado / Neutro / Sobrevendido |



\#### Fibonacci Retracement

\*\*Location:\*\* `historicos/indicadores/fibonacci/{TICKER}.csv`



| # | Field | Type | Level | Description |

|---|-------|------|-------|-------------|

| 1 | `Date` | `date` | — | Trading day |

| 2 | `Fib\_0` | `decimal(2)` | 0% | Support (swing low) |

| 3 | `Fib\_236` | `decimal(2)` | 23.6% | Shallow retracement |

| 4 | `Fib\_382` | `decimal(2)` | 38.2% | Moderate support/resistance |

| 5 | `Fib\_50` | `decimal(2)` | 50% | Equilibrium point |

| 6 | `Fib\_618` | `decimal(2)` | 61.8% | \*\*Golden Ratio\*\* — Key level |

| 7 | `Fib\_786` | `decimal(2)` | 78.6% | Deep retracement |

| 8 | `Fib\_1` | `decimal(2)` | 100% | Resistance (swing high) |

| 9 | `Fib\_1\_272` | `decimal(2)` | 127.2% | Extension projection |

| 10 | `Fib\_1\_618` | `decimal(2)` | 161.8% | \*\*Golden Ratio\*\* extension |

| 11 | `Fib\_Position` | `decimal(2)` | 0–2 | Relative position in the range |

| 12 | `Fib\_Level\_Current` | `text` | — | Current Fibonacci level |

| 13 | `Fib\_Distance\_Next` | `decimal(2)` | — | Distance to next level |

| 14 | `Fib\_Zone` | `text` | — | Support / Resistance / Consolidation / Breakout |

| 15 | `Fib\_Buy\_Signal` | `integer` | 0/1 | Price touched support (38.2% or 61.8%) |

| 16 | `Fib\_Sell\_Signal` | `integer` | 0/1 | Price touched resistance (78.6% or 100%) |



\#### Moving Averages

\*\*Location:\*\* `historicos/indicadores/medias\_moveis/{TICKER}.csv`



| # | Field | Type | Period | Description |

|---|-------|------|--------|-------------|

| 1 | `Date` | `date` | — | Trading day |

| 2 | `MA\_7` | `decimal(2)` | 7 days | Very short-term trend |

| 3 | `MA\_14` | `decimal(2)` | 14 days | Short-term trend |

| 4 | `MA\_30` | `decimal(2)` | 30 days | Monthly support/resistance |

| 5 | `MA\_50` | `decimal(2)` | 50 days | Medium-term trend |

| 6 | `MA\_200` | `decimal(2)` | 200 days | Long-term trend |

| 7 | `Sinal\_MA\_7\_14` | `integer` | — | 1 = Bullish crossover, −1 = Bearish |

| 8 | `Sinal\_MA\_50\_200` | `integer` | — | 1 = Golden Cross, −1 = Death Cross |



\#### Volatility \& Returns

\*\*Location:\*\* `historicos/indicadores/volatilidade/{TICKER}.csv`



| # | Field | Type | Description |

|---|-------|------|-------------|

| 1 | `Date` | `date` | Trading day |

| 2 | `Returns` | `decimal(4)` | Daily return (%) |

| 3 | `Returns\_Log` | `decimal(4)` | Logarithmic return |

| 4 | `Volatilidade\_20` | `decimal(2)` | Annualized 20-day volatility (%) |

| 5 | `Range\_Diario` | `decimal(2)` | Daily range (High − Low) |

| 6 | `Range\_Percentual` | `decimal(2)` | Daily range (%) |

| 7 | `Gap` | `decimal(2)` | Opening gap ($) |

| 8 | `Gap\_Percentual` | `decimal(2)` | Opening gap (%) |

| 9 | `Volume\_Medio\_20` | `integer` | 20-day average volume |

| 10 | `Volume\_Ratio` | `decimal(2)` | Volume / Average (>1.5 = abnormal) |



\#### Trends \& Signals

\*\*Location:\*\* `historicos/indicadores/tendencia/{TICKER}.csv`



| # | Field | Type | Description |

|---|-------|------|-------------|

| 1 | `Date` | `date` | Trading day |

| 2 | `Tendencia\_7d` | `text` | Short-term direction (Alta/Baixa) |

| 3 | `Tendencia\_50d` | `text` | Medium-term direction (Alta/Baixa) |

| 4 | `Forca\_Tendencia` | `decimal(2)` | 5-day MA-50 slope (%) |

| 5 | `Forca\_Movimento` | `decimal(2)` | 1 = Closed at high, −1 = Closed at low |

| 6 | `Velas\_Alta\_Consecutivas` | `integer` | Consecutive bullish candles |



\---



\## 💻 Usage Examples



\### Detecting Multiple Buy Signals



```python

import pandas as pd



ticker = 'AAPL'



\# Load indicators

rsi = pd.read\_csv(f'historicos/indicadores/rsi/{ticker}.csv')

macd = pd.read\_csv(f'historicos/indicadores/macd/{ticker}.csv')

fib = pd.read\_csv(f'historicos/indicadores/fibonacci/{ticker}.csv')



\# Check alignment of buy signals

buy\_signals\_aligned = (

&#x20;   (rsi\['RSI\_Sinal'].iloc\[-1] == 'Sobrevendido') \&

&#x20;   (macd\['MACD\_Sinal'].iloc\[-1] == 'Compra') \&

&#x20;   (fib\['Fib\_Buy\_Signal'].iloc\[-1] == 1)

)



if buy\_signals\_aligned:

&#x20;   print(f"✅ {ticker}: Multiple BUY signals aligned!")

else:

&#x20;   print(f"⏳ {ticker}: Waiting for signal alignment")

```



\### Screening for Recent Golden Cross



```python

import os

import pandas as pd



golden\_cross\_stocks = \[]



for file in os.listdir('historicos/indicadores/medias\_moveis/'):

&#x20;   df = pd.read\_csv(f'historicos/indicadores/medias\_moveis/{file}')

&#x20;   

&#x20;   # Detect Golden Cross: MA-50 crossed above MA-200 today

&#x20;   if len(df) >= 2:

&#x20;       yesterday = df\['Sinal\_MA\_50\_200'].iloc\[-2]

&#x20;       today = df\['Sinal\_MA\_50\_200'].iloc\[-1]

&#x20;       

&#x20;       if yesterday == -1 and today == 1:

&#x20;           ticker = file.replace('.csv', '')

&#x20;           golden\_cross\_stocks.append(ticker)



print(f"🟢 Recent Golden Cross signals: {golden\_cross\_stocks}")

```



\### Finding Top Dividend Payers



```python

import pandas as pd



dividends = pd.read\_csv('resumo\_dividendos.csv')



\# Top 10 by dividend yield

top\_yield = dividends.nlargest(10, 'dividend\_yield')

print("Top 10 Dividend Yields:")

print(top\_yield\[\['Symbol', 'dividend\_yield', 'total\_dividends\_1y', 'payout\_ratio']])

```



\---



\## 🛠️ Technology Stack



| Technology | Purpose |

|-----------|---------|

| \*\*Python 3.8+\*\* | Core programming language |

| \*\*yfinance\*\* | Yahoo Finance data extraction API |

| \*\*pandas\*\* | Data manipulation and analysis |

| \*\*numpy\*\* | Numerical computations |

| \*\*Google Colab\*\* | Cloud execution environment (optional) |



\---



\## ⚠️ Limitations



\- \*\*API Rate Limiting\*\*: Yahoo Finance restricts request frequency (\~10 requests/minute on free tier)

\- \*\*Data Coverage\*\*: Some delisted or very old symbols may not return data

\- \*\*Market Cap Calculation\*\*: Uses current shares outstanding adjusted backwards through split history

\- \*\*Corporate Actions\*\*: Complex events (spin-offs, mergers) may affect adjusted price accuracy

\- \*\*Real-time Data\*\*: This pipeline focuses on historical end-of-day data only



\---



\## 📝 License



This project is licensed under the MIT License — see the \[LICENSE](LICENSE) file for details.



\---



\## 🤝 Contributing



Contributions are welcome! Feel free to:



1\. Open issues for bug reports or feature requests

2\. Submit pull requests with improvements

3\. Share ideas for new indicators or data sources



\---



<p align="center">

&#x20; <b>⭐ If this project was helpful, please consider giving it a star!</b>

</p>

```

