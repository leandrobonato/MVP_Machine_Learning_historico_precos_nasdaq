"""
================================================================================
DOWNLOAD DE DADOS MACROECONÔMICOS - VERSÃO CORRIGIDA
================================================================================
Baixa dados de: Taxas de Juros, Índices, Commodities e Câmbio
Formato: Date, Open, Close, Change_Pct
================================================================================
"""

import pandas as pd
import yfinance as yf
import os
from pathlib import Path
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURAÇÕES
# ============================================

start_date = '2000-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# ============================================
# DICIONÁRIOS DE TICKERS
# ============================================

COMMODITIES = {
    'GC=F': 'Ouro',
    'SI=F': 'Prata',
    'PL=F': 'Platina',
    'PA=F': 'Paladio',
    'CL=F': 'Petroleo_WTI',
    'BZ=F': 'Petroleo_Brent',
    'NG=F': 'Gas_Natural',
    'HG=F': 'Cobre',
    'ZC=F': 'Milho',
    'ZW=F': 'Trigo',
    'ZS=F': 'Soja',
    'KC=F': 'Cafe',
    'CT=F': 'Algodao',
    'SB=F': 'Acucar',
}

CAMBIO = {
    'EURUSD=X': 'EURUSD',
    'GBPUSD=X': 'GBPUSD',
    'JPYUSD=X': 'JPYUSD',
    'AUDUSD=X': 'AUDUSD',
    'CADUSD=X': 'CADUSD',
    'CHFUSD=X': 'CHFUSD',
    'NZDUSD=X': 'NZDUSD',
    'MXNUSD=X': 'MXNUSD',
    'BRLUSD=X': 'BRLUSD',
    'CNYUSD=X': 'CNYUSD',
}

TAXAS_JUROS = {
    '^TNX': 'Treasury_10Y',
    '^FVX': 'Treasury_5Y',
    '^IRX': 'Treasury_3M',
    '^TYX': 'Treasury_30Y',
}

INDICES = {
    '^VIX': 'VIX',
    '^GSPC': 'SP500',
}

# ============================================
# CRIAÇÃO DE PASTAS
# ============================================

PASTAS = {
    'taxas_juros': 'historicos/macro_economicos/taxas_juros',
    'indices': 'historicos/macro_economicos/indices',
    'commodities': 'historicos/macro_economicos/commodities',
    'cambio': 'historicos/macro_economicos/cambio',
}

for pasta in PASTAS.values():
    Path(pasta).mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("📁 ESTRUTURA DE PASTAS CRIADA")
print("=" * 70)
for nome, pasta in PASTAS.items():
    print(f"   ✅ {pasta}/")

# ============================================
# FUNÇÃO PARA BAIXAR DADOS - CORRIGIDA
# ============================================

def baixar_dados(ticker, nome, pasta):
    """
    Baixa dados de um ticker e salva em CSV.
    Usa o mesmo formato do exemplo do Ouro.
    """
    try:
        print(f"   📥 Baixando {ticker} ({nome})...", end=" ")
        
        # Baixar dados usando o mesmo método do exemplo
        ticker_obj = yf.Ticker(ticker)
        dados = ticker_obj.history(start=start_date, end=end_date)
        
        if dados.empty:
            print("⚠️ Sem dados")
            return None
        
        # Resetar o índice para ter a coluna Date
        dados = dados.reset_index()
        
        # Criar DataFrame simplificado
        df = pd.DataFrame()
        df['Date'] = pd.to_datetime(dados['Date']).dt.strftime('%Y-%m-%d')
        
        # Open e Close
        if 'Open' in dados.columns:
            df['Open'] = dados['Open'].round(4)
        else:
            df['Open'] = dados.iloc[:, 1].round(4)  # Pega a primeira coluna numérica
        
        if 'Close' in dados.columns:
            df['Close'] = dados['Close'].round(4)
        else:
            df['Close'] = dados.iloc[:, 4].round(4)  # Pega a coluna Close
        
        # Variação percentual
        df['Change_Pct'] = ((df['Close'] - df['Open']) / df['Open'] * 100).round(2)
        
        # Salvar
        arquivo = f"{pasta}/{nome}.csv"
        df.to_csv(arquivo, index=False, float_format='%.6f')
        
        data_inicio = df['Date'].iloc[0] if not df.empty else 'N/A'
        data_fim = df['Date'].iloc[-1] if not df.empty else 'N/A'
        print(f"✅ {len(df)} registros ({data_inicio} a {data_fim})")
        return df
    
    except Exception as e:
        print(f"❌ Erro: {str(e)[:60]}")
        return None

# ============================================
# TESTE RÁPIDO - APENAS OURO
# ============================================

print("\n" + "=" * 70)
print("🧪 TESTE: Baixando apenas Ouro (GC=F)")
print("=" * 70)

# Testar apenas ouro primeiro
ticker_teste = yf.Ticker("GC=F")
dados_teste = ticker_teste.history(start='2026-06-01', end='2026-06-25')

print("\n📊 Dados do Ouro (últimos dias):")
print("=" * 70)
print(dados_teste)

if not dados_teste.empty:
    print("\n📊 Formato simplificado:")
    print("=" * 70)
    df_teste = dados_teste.reset_index()
    df_teste['Date'] = pd.to_datetime(df_teste['Date']).dt.strftime('%Y-%m-%d')
    df_simples = df_teste[['Date', 'Open', 'Close']].copy()
    df_simples['Change_Pct'] = ((df_simples['Close'] - df_simples['Open']) / df_simples['Open'] * 100).round(2)
    print(df_simples.to_string())

print("\n" + "=" * 70)
print("📥 INICIANDO DOWNLOAD COMPLETO")
print("=" * 70)
print(f"Período: {start_date} até {end_date}")
print("=" * 70)

dados_consolidados = {}

# 1. Taxas de Juros
print("\n📊 Taxas de Juros")
print("-" * 50)
for ticker, nome in TAXAS_JUROS.items():
    df = baixar_dados(ticker, nome, PASTAS['taxas_juros'])
    if df is not None:
        dados_consolidados[nome] = df
    time.sleep(0.3)

# 2. Índices
print("\n📊 Índices")
print("-" * 50)
for ticker, nome in INDICES.items():
    df = baixar_dados(ticker, nome, PASTAS['indices'])
    if df is not None:
        dados_consolidados[nome] = df
    time.sleep(0.3)

# 3. Commodities
print("\n📊 Commodities")
print("-" * 50)
for ticker, nome in COMMODITIES.items():
    df = baixar_dados(ticker, nome, PASTAS['commodities'])
    if df is not None:
        dados_consolidados[nome] = df
    time.sleep(0.3)

# 4. Câmbio
print("\n📊 Câmbio")
print("-" * 50)
for ticker, nome in CAMBIO.items():
    df = baixar_dados(ticker, nome, PASTAS['cambio'])
    if df is not None:
        dados_consolidados[nome] = df
    time.sleep(0.3)
