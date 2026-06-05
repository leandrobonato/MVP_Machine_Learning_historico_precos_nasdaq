```markdown
<div align="center">

# 📊 NASDAQ Financial Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Yahoo Finance](https://img.shields.io/badge/Yahoo_Finance-API-7B2D8E?style=for-the-badge&logo=yahoo&logoColor=white)](https://finance.yahoo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Indicators](https://img.shields.io/badge/Indicators-55+-success?style=for-the-badge)]()

**Pipeline automatizado para coleta de cotações históricas, dividendos, valor de mercado e 55+ indicadores técnicos de ações listadas na NASDAQ.**

</div>

---

## 📁 Project Structure

```
📦 nasdaq-financial-pipeline
├── 📂 data/
│   └── 📄 nasdaq-listed-symbols.csv
├── 📂 scripts/
│   ├── 📜 download_cotacoes.py
│   ├── 📜 download_indicadores.py
│   └── 📜 pipeline_completo.py
├── 📂 historicos/
│   ├── 📂 cotacoes/
│   ├── 📂 dividendos/
│   ├── 📂 valor_mercado/
│   └── 📂 indicadores/
│       ├── 📂 rsi/
│       ├── 📂 macd/
│       ├── 📂 bollinger/
│       ├── 📂 fibonacci/
│       ├── 📂 medias_moveis/
│       ├── 📂 volatilidade/
│       └── 📂 tendencia/
├── 📄 resumo_dividendos.csv
├── 📄 resumo_valor_mercado.csv
└── 📄 symbols_valid.csv
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📈 Historical Stock Quotes
- **OHLCV Data**: Open, High, Low, Close, Adj Close, Volume
- Configurable period (default: 2016–present)
- 5,000+ NASDAQ symbols supported
- Prices rounded to 2 decimal places

### 💰 Dividends & Corporate Actions
- Complete dividend payment history
- Dividend Yield, Rate, Payout Ratio
- Trailing 12-month totals
- Ex-dividend date tracking
- Stock split history

### 💎 Market Capitalization
- Daily Market Cap = Close × Shares Outstanding
- Auto-adjusted for historical splits
- Dollar volume traded

</td>
<td width="50%">

### 🔬 Technical Indicators (55+)

| Category | Key Indicators |
|----------|---------------|
| **Moving Averages** | MA_7, MA_14, MA_30, MA_50, MA_200, Golden/Death Cross |
| **RSI** | RSI_7, RSI_14, Overbought/Oversold signals |
| **MACD** | Line, Signal, Histogram, Buy/Sell signals |
| **Bollinger Bands** | Upper, Middle, Lower, Width, Position |
| **Fibonacci** | 9 retracement levels, Extensions, Confluence |
| **Volatility** | Returns, Annualized Vol, Range, Gap, Volume Ratio |
| **Trend** | Direction, Strength, Consecutive Candles |

</td>
</tr>
</table>

---

## 📊 Data Dictionary

<details open>
<summary><b>📈 Stock Quotes</b> — <code>historicos/cotacoes/{SYMBOL}.csv</code></summary>
<br>

| # | Field | Type | Example | Description |
|---|-------|------|---------|-------------|
| 1 | Date | Date | 2024-01-15 | Trading date (YYYY-MM-DD) |
| 2 | Open | Decimal(2) | 185.50 | Opening price |
| 3 | High | Decimal(2) | 188.75 | Highest price |
| 4 | Low | Decimal(2) | 184.20 | Lowest price |
| 5 | Close | Decimal(2) | 187.30 | Closing price |
| 6 | Adj Close | Decimal(2) | 187.30 | Adjusted close (splits/dividends) |
| 7 | Volume | Integer | 52,456,700 | Shares traded |

</details>

<details>
<summary><b>💰 Dividends</b> — <code>historicos/dividendos/{SYMBOL}.csv</code></summary>
<br>

| # | Field | Type | Example | Description |
|---|-------|------|---------|-------------|
| 1 | Date | Date | 2024-03-15 | Payment/event date |
| 2 | Dividends | Decimal(4) | 0.2500 | Dividend per share ($) |
| 3 | Stock_Splits | Decimal(4) | 2.0000 | Split ratio (2.0 = 2:1) |
| 4 | Dividend_Yield | Decimal(2) | 2.50 | Annual dividend yield (%) |
| 5 | Dividend_Rate | Decimal(2) | 1.00 | Annual dividend per share ($) |
| 6 | Payout_Ratio | Decimal(2) | 35.00 | % of earnings paid as dividends |
| 7 | Dividend_1Y_Total | Decimal(4) | 1.0000 | Total dividends (12 months) |
| 8 | Dividend_1Y_Count | Integer | 4 | Payments in last year |
| 9 | Last_Dividend | Decimal(4) | 0.2500 | Last dividend amount |
| 10 | Ex_Dividend_Date | Date | 2024-06-15 | Next ex-dividend date |

</details>

<details>
<summary><b>💎 Market Cap</b> — <code>historicos/valor_mercado/{SYMBOL}.csv</code></summary>
<br>

| # | Field | Type | Example | Description |
|---|-------|------|---------|-------------|
| 1 | Date | Date | 2024-01-15 | Trading date |
| 2 | Close | Decimal(2) | 187.30 | Closing price |
| 3 | Shares_Outstanding | Integer | 15,500,000,000 | Shares outstanding |
| 4 | Market_Cap | Decimal(2) | 2,903,150,000,000 | Market capitalization ($) |
| 5 | Market_Cap_B | Decimal(2) | 2,903.15 | Market Cap in billions ($B) |
| 6 | Market_Cap_Change_Pct | Decimal(2) | 1.25 | Daily % change |
| 7 | Volume_Dollar | Decimal(2) | 9,825,345,100 | Dollar volume traded ($) |

</details>

---

## 🔬 Technical Indicators Detail

<details>
<summary><b>📈 Moving Averages</b> — <code>indicadores/medias_moveis/</code></summary>
<br>

| Field | Type | Period | Signal |
|-------|------|--------|--------|
| MA_7 | Decimal(2) | 7 days | Short-term trend |
| MA_14 | Decimal(2) | 14 days | Short-term trend |
| MA_30 | Decimal(2) | 30 days | Monthly S/R |
| MA_50 | Decimal(2) | 50 days | Medium-term trend |
| MA_200 | Decimal(2) | 200 days | Long-term trend |
| Sinal_MA_7_14 | Integer | — | 1 = Bullish cross, -1 = Bearish cross |
| Sinal_MA_50_200 | Integer | — | 1 = Golden Cross, -1 = Death Cross |

</details>

<details>
<summary><b>📉 RSI</b> — <code>indicadores/rsi/</code></summary>
<br>

| Field | Type | Period | Signal |
|-------|------|--------|--------|
| RSI_7 | Decimal(2) | 7 periods | Fast signal |
| RSI_14 | Decimal(2) | 14 periods | Standard |
| RSI_Sinal | Text | — | >70 Overbought / <30 Oversold / Neutral |

</details>

<details>
<summary><b>📊 MACD</b> — <code>indicadores/macd/</code></summary>
<br>

| Field | Type | Description |
|-------|------|-------------|
| MACD_Line | Decimal(2) | EMA12 − EMA26 |
| MACD_Signal | Decimal(2) | EMA9 of MACD Line |
| MACD_Histogram | Decimal(2) | Line − Signal |
| MACD_Sinal | Text | Buy / Sell / Neutral |

</details>

<details>
<summary><b>🎯 Bollinger Bands</b> — <code>indicadores/bollinger/</code></summary>
<br>

| Field | Type | Description |
|-------|------|-------------|
| BB_Upper | Decimal(2) | MA20 + 2σ |
| BB_Middle | Decimal(2) | MA20 |
| BB_Lower | Decimal(2) | MA20 − 2σ |
| BB_Width | Decimal(2) | Bandwidth (%) |
| BB_Position | Decimal(2) | 0 = Lower, 1 = Upper |
| BB_Sinal | Text | Overbought / Oversold / Neutral |

</details>

<details>
<summary><b>🔢 Fibonacci</b> — <code>indicadores/fibonacci/</code></summary>
<br>

| Field | Type | Level | Description |
|-------|------|-------|-------------|
| Fib_0 | Decimal(2) | 0% | Support (bottom) |
| Fib_236 | Decimal(2) | 23.6% | Weak retracement |
| Fib_382 | Decimal(2) | 38.2% | Moderate S/R |
| Fib_50 | Decimal(2) | 50% | Equilibrium |
| Fib_618 | Decimal(2) | 61.8% | **Golden Ratio** |
| Fib_786 | Decimal(2) | 78.6% | Deep retracement |
| Fib_1 | Decimal(2) | 100% | Resistance (top) |
| Fib_1_272 | Decimal(2) | 127.2% | Extension |
| Fib_1_618 | Decimal(2) | 161.8% | **Golden Ratio** extension |
| Fib_Zone | Text | — | Support / Resistance / Consolidation |
| Fib_Confluencia | Integer | — | Converging levels (≥2 Strong, ≥4 Very Strong) |

</details>

<details>
<summary><b>📊 Volatility</b> — <code>indicadores/volatilidade/</code></summary>
<br>

| Field | Type | Description |
|-------|------|-------------|
| Returns | Decimal(4) | Daily return (%) |
| Returns_Log | Decimal(4) | Logarithmic return |
| Volatilidade_20 | Decimal(2) | Annualized volatility (%) |
| Range_Diario | Decimal(2) | High − Low |
| Range_Percentual | Decimal(2) | Range / Close × 100 |
| Gap | Decimal(2) | Open − Previous Close |
| Gap_Percentual | Decimal(2) | Gap / Previous Close × 100 |
| Volume_Medio_20 | Integer | 20-day avg volume |
| Volume_Ratio | Decimal(2) | Volume / Avg (>1.5 = abnormal) |

</details>

<details>
<summary><b>🔍 Trend</b> — <code>indicadores/tendencia/</code></summary>
<br>

| Field | Type | Description |
|-------|------|-------------|
| Tendencia_7d | Text | Close vs MA7 (Alta/Baixa) |
| Tendencia_50d | Text | Close vs MA50 (Alta/Baixa) |
| Forca_Tendencia | Decimal(2) | MA50 slope over 5 days (%) |
| Forca_Movimento | Decimal(2) | 1 = Closed at High, -1 = Closed at Low |
| Velas_Alta_Consecutivas | Integer | Consecutive bullish candles |

</details>

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install yfinance pandas numpy
```

### Installation

```bash
git clone https://github.com/your-username/nasdaq-financial-pipeline.git
cd nasdaq-financial-pipeline
```

### Usage

| Command | Description |
|---------|-------------|
| `python scripts/pipeline_completo.py` | Run complete pipeline |
| `python scripts/download_cotacoes.py` | Download quotes only |
| `python scripts/download_indicadores.py` | Calculate indicators only |

### Configuration

```python
# Edit in scripts:
offset = 0              # Start index
limit = 100             # Number of symbols
start_date = '2016-01-01'  # Start date
```

---

## 💻 Examples

### Multi-Signal Detection

```python
import pandas as pd

# Load indicators
rsi = pd.read_csv('historicos/indicadores/rsi/AAPL.csv')
macd = pd.read_csv('historicos/indicadores/macd/AAPL.csv')
fib = pd.read_csv('historicos/indicadores/fibonacci/AAPL.csv')

# Check aligned buy signals
buy = (
    (rsi['RSI_Sinal'].iloc[-1] == 'Sobrevendido') &
    (macd['MACD_Sinal'].iloc[-1] == 'Compra') &
    (fib['Fib_Buy_Signal'].iloc[-1] == 1)
)
print(f"BUY Signal: {buy}")
```

### Golden Cross Scanner

```python
import os

for file in os.listdir('historicos/indicadores/medias_moveis/'):
    df = pd.read_csv(f'historicos/indicadores/medias_moveis/{file}')
    if df['Sinal_MA_50_200'].iloc[-1] == 1:
        print(f"✅ {file.replace('.csv', '')}: Golden Cross")
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **yfinance** | Yahoo Finance API |
| **pandas** | Data manipulation |
| **numpy** | Numerical computing |
| **Google Colab** | Cloud execution (optional) |

---

## ⚠️ Limitations

- **Rate Limit**: ~10 requests/minute (Yahoo Finance free tier)
- **Delisted Stocks**: Historical data may be unavailable
- **Market Cap**: Uses current shares outstanding adjusted for historical splits

---

<div align="center">

**⭐ If this project was helpful, please consider giving it a star!**

<sub>Built for the quantitative finance community</sub>

</div>
```