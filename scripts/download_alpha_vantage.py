from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
from pathlib import Path

# Pegue uma chave gratuita em: https://www.alphavantage.co/support/#api-key
API_KEY = 'demo'  # Substitua por sua chave

ts = TimeSeries(key=API_KEY, output_format='pandas')

with open('tickers.txt', 'r') as f:
    tickers = [linha.strip() for linha in f if linha.strip()][:10000]

Path('dados_alpha').mkdir(exist_ok=True)

for ticker in tickers:
    print(f"Baixando {ticker}...")
    try:
        data, meta = ts.get_daily(symbol=ticker, outputsize='compact')
        if not data.empty:
            data.to_csv(f"dados_alpha/{ticker}.csv")
            print(f"  ✅ {len(data)} registros")
        else:
            print(f"  ⚠️ Sem dados")
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    time.sleep(12)  # Alpha Vantage tem limite de 5 chamadas por minuto
