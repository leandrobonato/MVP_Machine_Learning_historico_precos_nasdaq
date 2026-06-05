

\---



\## ✨ Features



\### 🔹 1. Historical Stock Quotes

\- \*\*OHLCV Data\*\*: Open, High, Low, Close, Adj Close, Volume

\- \*\*Configurable Period\*\*: Default from 2016 to current date

\- \*\*Scalability\*\*: Supports 5,000+ NASDAQ symbols

\- \*\*Precision\*\*: Prices with 2 decimal places, Volume as integer



\### 🔹 2. Dividends \& Corporate Actions

\- Complete dividend payment history

\- \*\*Key Metrics\*\*: Dividend Yield, Dividend Rate, Payout Ratio

\- Trailing 12-month dividend totals

\- Ex-dividend date tracking

\- Stock split history



\### 🔹 3. Historical Market Capitalization

\- \*\*Daily Market Cap\*\* = Close × Shares Outstanding

\- Automatic adjustment for historical splits

\- Dollar volume traded (Volume × Close)

\- Market Cap in billions for readability

\- Daily percentage change



\### 🔹 4. Technical Indicators (55+)



<table>

&#x20; <tr>

&#x20;   <td width="33%">

&#x20;     <h4>📈 Moving Averages</h4>

&#x20;     <table>

&#x20;       <tr><th>Indicator</th><th>Period</th></tr>

&#x20;       <tr><td>MA\_7</td><td>7 days</td></tr>

&#x20;       <tr><td>MA\_14</td><td>14 days</td></tr>

&#x20;       <tr><td>MA\_30</td><td>30 days</td></tr>

&#x20;       <tr><td>MA\_50</td><td>50 days</td></tr>

&#x20;       <tr><td>MA\_200</td><td>200 days</td></tr>

&#x20;       <tr><td colspan="2"><i>Golden Cross / Death Cross signals</i></td></tr>

&#x20;     </table>

&#x20;   </td>

&#x20;   <td width="33%">

&#x20;     <h4>📉 RSI</h4>

&#x20;     <table>

&#x20;       <tr><th>Indicator</th><th>Period</th></tr>

&#x20;       <tr><td>RSI\_7</td><td>7 periods</td></tr>

&#x20;       <tr><td>RSI\_14</td><td>14 periods</td></tr>

&#x20;       <tr><td colspan="2"><i>>70 Overbought | <30 Oversold</i></td></tr>

&#x20;     </table>

&#x20;   </td>

&#x20;   <td width="33%">

&#x20;     <h4>📊 MACD</h4>

&#x20;     <table>

&#x20;       <tr><th>Indicator</th><th>Component</th></tr>

&#x20;       <tr><td>MACD\_Line</td><td>EMA12 - EMA26</td></tr>

&#x20;       <tr><td>MACD\_Signal</td><td>EMA9 of MACD</td></tr>

&#x20;       <tr><td>MACD\_Histogram</td><td>Line - Signal</td></tr>

&#x20;       <tr><td colspan="2"><i>Buy/Sell crossover signals</i></td></tr>

&#x20;     </table>

&#x20;   </td>

&#x20; </tr>

&#x20; <tr>

&#x20;   <td width="33%">

&#x20;     <h4>🎯 Bollinger Bands</h4>

&#x20;     <table>

&#x20;       <tr><th>Band</th><th>Description</th></tr>

&#x20;       <tr><td>BB\_Upper</td><td>+2 Std Dev</td></tr>

&#x20;       <tr><td>BB\_Middle</td><td>MA 20 days</td></tr>

&#x20;       <tr><td>BB\_Lower</td><td>-2 Std Dev</td></tr>

&#x20;       <tr><td colspan="2"><i>Width, Position \& Overbought/Oversold</i></td></tr>

&#x20;     </table>

&#x20;   </td>

&#x20;   <td width="33%">

&#x20;     <h4>🔢 Fibonacci</h4>

&#x20;     <table>

&#x20;       <tr><th>Level</th><th>Value</th></tr>

&#x20;       <tr><td>Fib\_0</td><td>0%</td></tr>

&#x20;       <tr><td>Fib\_382</td><td>38.2%</td></tr>

&#x20;       <tr><td>Fib\_618</td><td>61.8% ⭐</td></tr>

&#x20;       <tr><td>Fib\_1</td><td>100%</td></tr>

&#x20;       <tr><td colspan="2"><i>Extensions, Confluence \& Signals</i></td></tr>

&#x20;     </table>

&#x20;   </td>

&#x20;   <td width="33%">

&#x20;     <h4>📊 Volatility</h4>

&#x20;     <table>

&#x20;       <tr><th>Metric</th><th>Description</th></tr>

&#x20;       <tr><td>Returns</td><td>Daily %</td></tr>

&#x20;       <tr><td>Volatilidade\_20</td><td>Annualized</td></tr>

&#x20;       <tr><td>Range\_Diario</td><td>High - Low</td></tr>

&#x20;       <tr><td>Gap</td><td>Open - Prev Close</td></tr>

&#x20;       <tr><td>Volume\_Ratio</td><td>vs 20d avg</td></tr>

&#x20;     </table>

&#x20;   </td>

&#x20; </tr>

</table>



\---



\## 📚 Data Dictionary



<details>

<summary><b>📈 Stock Quotes</b> (Click to expand)</summary>

<br>

<table>

&#x20; <tr>

&#x20;   <th>#</th>

&#x20;   <th>Field</th>

&#x20;   <th>Type</th>

&#x20;   <th>Example</th>

&#x20;   <th>Description</th>

&#x20; </tr>

&#x20; <tr><td>1</td><td>Date</td><td>Date</td><td>2024-01-15</td><td>Trading date (YYYY-MM-DD)</td></tr>

&#x20; <tr><td>2</td><td>Open</td><td>Decimal(2)</td><td>185.50</td><td>Opening price</td></tr>

&#x20; <tr><td>3</td><td>High</td><td>Decimal(2)</td><td>188.75</td><td>Highest price</td></tr>

&#x20; <tr><td>4</td><td>Low</td><td>Decimal(2)</td><td>184.20</td><td>Lowest price</td></tr>

&#x20; <tr><td>5</td><td>Close</td><td>Decimal(2)</td><td>187.30</td><td>Closing price</td></tr>

&#x20; <tr><td>6</td><td>Adj Close</td><td>Decimal(2)</td><td>187.30</td><td>Adjusted close (splits/dividends)</td></tr>

&#x20; <tr><td>7</td><td>Volume</td><td>Integer</td><td>52456700</td><td>Shares traded</td></tr>

</table>

</details>



<details>

<summary><b>💰 Dividends</b> (Click to expand)</summary>

<br>

<table>

&#x20; <tr>

&#x20;   <th>#</th>

&#x20;   <th>Field</th>

&#x20;   <th>Type</th>

&#x20;   <th>Example</th>

&#x20;   <th>Description</th>

&#x20; </tr>

&#x20; <tr><td>1</td><td>Date</td><td>Date</td><td>2024-03-15</td><td>Payment/event date</td></tr>

&#x20; <tr><td>2</td><td>Dividends</td><td>Decimal(4)</td><td>0.2500</td><td>Dividend per share</td></tr>

&#x20; <tr><td>3</td><td>Stock\_Splits</td><td>Decimal(4)</td><td>2.0000</td><td>Split ratio (2.0 = 2:1)</td></tr>

&#x20; <tr><td>4</td><td>Dividend\_Yield</td><td>Decimal(2)</td><td>2.50</td><td>Annual dividend yield (%)</td></tr>

&#x20; <tr><td>5</td><td>Dividend\_Rate</td><td>Decimal(2)</td><td>1.00</td><td>Annual dividend per share ($)</td></tr>

&#x20; <tr><td>6</td><td>Payout\_Ratio</td><td>Decimal(2)</td><td>35.00</td><td>% of earnings paid as dividends</td></tr>

&#x20; <tr><td>7</td><td>Dividend\_1Y\_Total</td><td>Decimal(4)</td><td>1.0000</td><td>Total dividends last 12 months</td></tr>

&#x20; <tr><td>8</td><td>Dividend\_1Y\_Count</td><td>Integer</td><td>4</td><td>Payments in last year</td></tr>

&#x20; <tr><td>9</td><td>Last\_Dividend</td><td>Decimal(4)</td><td>0.2500</td><td>Last dividend paid</td></tr>

&#x20; <tr><td>10</td><td>Ex\_Dividend\_Date</td><td>Date</td><td>2024-06-15</td><td>Next ex-dividend date</td></tr>

</table>

</details>



<details>

<summary><b>💎 Market Cap</b> (Click to expand)</summary>

<br>

<table>

&#x20; <tr>

&#x20;   <th>#</th>

&#x20;   <th>Field</th>

&#x20;   <th>Type</th>

&#x20;   <th>Example</th>

&#x20;   <th>Description</th>

&#x20; </tr>

&#x20; <tr><td>1</td><td>Date</td><td>Date</td><td>2024-01-15</td><td>Trading date</td></tr>

&#x20; <tr><td>2</td><td>Close</td><td>Decimal(2)</td><td>187.30</td><td>Closing price</td></tr>

&#x20; <tr><td>3</td><td>Shares\_Outstanding</td><td>Integer</td><td>15.5B</td><td>Shares outstanding</td></tr>

&#x20; <tr><td>4</td><td>Market\_Cap</td><td>Decimal(2)</td><td>2.9T</td><td>Market capitalization ($)</td></tr>

&#x20; <tr><td>5</td><td>Market\_Cap\_B</td><td>Decimal(2)</td><td>2903.15</td><td>Market Cap in billions ($B)</td></tr>

&#x20; <tr><td>6</td><td>Market\_Cap\_Change\_Pct</td><td>Decimal(2)</td><td>1.25</td><td>Daily % change</td></tr>

&#x20; <tr><td>7</td><td>Volume\_Dollar</td><td>Decimal(2)</td><td>9.8B</td><td>Dollar volume traded ($)</td></tr>

</table>

</details>



\---



\## 🚀 Quick Start



\### Prerequisites

```bash

pip install yfinance pandas numpy

