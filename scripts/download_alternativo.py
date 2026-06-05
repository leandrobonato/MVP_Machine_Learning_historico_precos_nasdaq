import requests
import pandas as pd
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

# Configurações
ARQUIVO_TICKERS = 'tickers.txt'  # Use um arquivo pequeno para testar
PASTA_SAIDA = 'dados_historicos'

Path(PASTA_SAIDA).mkdir(parents=True, exist_ok=True)

# Opção 1: Usar API do Yahoo Finance via yfinance (com retry)
def baixar_com_yfinance(ticker):
    try:
        import yfinance as yf
        # Configurar sessão com headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        yf.set_tz_cache_location(f"{PASTA_SAIDA}/tz_cache")
        
        ticker_obj = yf.Ticker(ticker, session=session)
        dados = ticker_obj.history(period='5y')
        return dados
    except Exception as e:
        print(f"  Erro yfinance: {e}")
        return None

# Opção 2: Usar API Alpha Vantage (gratuita, precisa de chave)
API_KEY_ALPHA = 'demo'  # Substitua por sua chave gratuita em alphavantage.co

def baixar_com_alphavantage(ticker):
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY_ALPHA}&outputsize=full'
        response = requests.get(url)
        data = response.json()
        
        if 'Time Series (Daily)' in data:
            df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.rename(columns={
                '1. open': 'Open',
                '2. high': 'High', 
                '3. low': 'Low',
                '4. close': 'Close',
                '5. volume': 'Volume'
            })
            df = df.astype(float)
            return df.sort_index()
    except:
        pass
    return None

# Opção 3: Usar API do Twelve Data (gratuita)
def baixar_com_twelvedata(ticker):
    try:
        url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=5000&apikey=demo'
        response = requests.get(url)
        data = response.json()
        
        if 'values' in data:
            df = pd.DataFrame(data['values'])
            df = df.rename(columns={
                'datetime': 'Date',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
            return df.astype(float)
    except:
        pass
    return None

# Ler tickers
with open(ARQUIVO_TICKERS, 'r') as f:
    tickers = [linha.strip() for linha in f if linha.strip()][:20]  # Testar só 20

print(f"📊 Testando {len(tickers)} tickers...")

for ticker in tickers[:5]:  # Testar primeiros 5
    print(f"\n🔍 Testando {ticker}:")
    
    # Tentar yfinance primeiro
    print("  Tentando yfinance...")
    dados = baixar_com_yfinance(ticker)
    if dados is not None and not dados.empty:
        print(f"  ✅ Sucesso! {len(dados)} registros")
        dados.to_csv(f"{PASTA_SAIDA}/{ticker}.csv")
        continue
    
    print("  ❌ Falhou. Tentando API alternativa...")
    
    # Se não funcionou, pode ser problema de rede
    print("  ⚠️ Possível bloqueio de rede. Verifique sua conexão.")
    break

print("\n" + "="*50)
print("📋 Diagnóstico:")
print("1. Verifique se consegue acessar: https://finance.yahoo.com")
print("2. Verifique se o firewall está bloqueando")
print("3. Tente executar: pip install --upgrade yfinance")
print("="*50)
