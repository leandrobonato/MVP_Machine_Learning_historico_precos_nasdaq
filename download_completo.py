"""
================================================================================
DOWNLOAD COMPLETO - COTAÇÕES + DIVIDENDOS + MARKET CAP + FUNDAMENTOS + INFO GERAL + COMMODITIES
================================================================================
Descrição: Pipeline completo de download e processamento de dados financeiros
Fonte: Yahoo Finance (via yfinance)
Período: 2000-01-01 até data atual

ESTRUTURA DE PASTAS:
├── historicos/
│   ├── cotacoes/              # Preços OHLCV
│   │   └── {SIMBOLO}.csv
│   ├── dividendos/            # Histórico de dividendos + métricas
│   │   └── {SIMBOLO}.csv
│   ├── valor_mercado/         # Market Cap histórico
│   │   └── {SIMBOLO}.csv
│   ├── fundamentos/           # Dados fundamentalistas
│   │   └── {SIMBOLO}.csv
│   ├── info_geral/            # Informações gerais da empresa
│   │   └── {SIMBOLO}.csv
│   ├── commodities/           # Influência de commodities por empresa
│   │   └── {SIMBOLO}.csv
│   └── indicadores/
│       ├── rsi/               # RSI (7 e 14 períodos)
│       │   └── {SIMBOLO}.csv
│       ├── macd/              # MACD
│       │   └── {SIMBOLO}.csv
│       ├── bollinger/         # Bandas de Bollinger
│       │   └── {SIMBOLO}.csv
│       ├── fibonacci/         # Fibonacci Retracement
│       │   └── {SIMBOLO}.csv
│       ├── medias_moveis/     # Médias Móveis
│       │   └── {SIMBOLO}.csv
│       ├── volatilidade/      # Volatilidade e Retornos
│       │   └── {SIMBOLO}.csv
│       └── tendencia/         # Tendências e Sinais
│           └── {SIMBOLO}.csv
├── resumo_dividendos.csv
├── resumo_valor_mercado.csv
├── resumo_fundamentos.csv
├── resumo_info_geral.csv
├── resumo_commodities.csv
└── symbols_valid.csv

================================================================================
"""

import pandas as pd
import yfinance as yf
import numpy as np
import os
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============================================
# LISTA DE SÍMBOLOS QUE QUEREMOS CARREGAR
# ============================================

simbolos_usados = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'MRVL',
                   'PEP', 'NFLX', 'AMD', 'GOOG', 'AVGO', 'META', 'MU', 'WMT',
                   'COST', 'ADBE', 'CMCSA', 'CSCO', 'INTC', 'QCOM', 'TXN',
                   'AMGN', 'ISRG', 'TMUS', 'HON', 'BKNG', 'AMAT', 'LRCX', 'TEAM',
                   'GILD', 'CSX', 'ADI', 'VRTX', 'ADP', 'REGN', 'KLAC', 'MELI',
                   'MPWR', 'PCAR', 'SNPS', 'KDP', 'CDNS', 'MRNA', 'ABNB', 'WDAY', 
                   'CHTR', 'LIN', 'KHC']

# ============================================
# MApeamento de Commodities
# ============================================

# Lista completa de commodities com tickers, nomes e descrições
COMMODITIES_LIST = [
    {'ticker': 'GC=F', 'nome': 'Ouro', 'descricao': 'Gold Futures'},
    {'ticker': 'SI=F', 'nome': 'Prata', 'descricao': 'Silver Futures'},
    {'ticker': 'CL=F', 'nome': 'Petroleo_WTI', 'descricao': 'Crude Oil WTI Futures'},
    {'ticker': 'BZ=F', 'nome': 'Petroleo_Brent', 'descricao': 'Brent Oil Futures'},
    {'ticker': 'HG=F', 'nome': 'Cobre', 'descricao': 'Copper Futures'},
    {'ticker': 'ZC=F', 'nome': 'Milho', 'descricao': 'Corn Futures'},
    {'ticker': 'ZW=F', 'nome': 'Trigo', 'descricao': 'Wheat Futures'},
    {'ticker': 'ZS=F', 'nome': 'Soja', 'descricao': 'Soybean Futures'},
    {'ticker': 'KC=F', 'nome': 'Cafe', 'descricao': 'Coffee Futures'},
    {'ticker': 'SB=F', 'nome': 'Acucar', 'descricao': 'Sugar Futures'},
    {'ticker': 'NG=F', 'nome': 'Gas_Natural', 'descricao': 'Natural Gas Futures'}
]

# Mapeamento de setores para commodities com direção de influência
SECTOR_COMMODITY_MAP = {
    'Energy': [
        ('Petroleo_WTI', 'positiva'),
        ('Petroleo_Brent', 'positiva'),
        ('Gas_Natural', 'positiva'),
    ],
    'Oil & Gas': [
        ('Petroleo_WTI', 'positiva'),
        ('Petroleo_Brent', 'positiva'),
        ('Gas_Natural', 'positiva'),
    ],
    'Basic Materials': [
        ('Cobre', 'positiva')
    ],
    'Metals & Mining': [
        ('Ouro', 'positiva'),
        ('Prata', 'positiva'),
        ('Cobre', 'positiva')
    ],
    'Gold': [
        ('Ouro', 'positiva'),
        ('Prata', 'positiva'),
    ],
    'Agriculture': [
        ('Soja', 'positiva'),
        ('Milho', 'positiva'),
        ('Trigo', 'positiva'),
        ('Cafe', 'positiva'),
        ('Acucar', 'positiva')
    ],
    'Consumer Defensive': [
        ('Soja', 'positiva'),
        ('Milho', 'positiva'),
        ('Trigo', 'positiva'),
        ('Cafe', 'positiva'),
        ('Acucar', 'positiva'),
    ],
    'Technology': [
        ('Cobre', 'positiva'),
        ('Ouro', 'positiva'),
        ('Prata', 'positiva')
    ],
    'Semiconductors': [
        ('Cobre', 'positiva'),
        ('Ouro', 'positiva'),
        ('Prata', 'positiva')
    ],
    'Utilities': [
        ('Gas_Natural', 'positiva')
    ],
    'Renewable Energy': [
        ('Cobre', 'positiva')
    ],
    'Airlines': [
        ('Petroleo_WTI', 'negativa'),
        ('Petroleo_Brent', 'negativa'),
    ],
    'Transportation': [
        ('Petroleo_WTI', 'negativa'),
        ('Petroleo_Brent', 'negativa'),
    ],
    'Food & Beverage': [
        ('Soja', 'negativa'),
        ('Milho', 'negativa'),
        ('Trigo', 'negativa'),
        ('Cafe', 'negativa'),
        ('Acucar', 'negativa'),
    ],
}

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def obter_commodities_por_empresa(ticker, setor):
    """
    Obtém lista de commodities que influenciam a empresa com base no setor.
    
    Retorna uma lista de dicionários com:
    - commodity: nome da commodity
    - ticker: ticker da commodity
    - descricao: descrição da commodity
    - direcao: 'positiva' ou 'negativa'
    - impacto: descrição do impacto
    """
    commodities_empresa = []
    
    # Buscar commodities do setor
    if setor in SECTOR_COMMODITY_MAP:
        for comm_nome, direcao in SECTOR_COMMODITY_MAP[setor]:
            # Encontrar o ticker e descrição da commodity
            for comm in COMMODITIES_LIST:
                if comm['nome'] == comm_nome:
                    impacto = 'positivo' if direcao == 'positiva' else 'negativo'
                    descricao_impacto = f"Preço da {comm['descricao']} {impacto} influencia o preço da ação na mesma direção" if direcao == 'positiva' else f"Preço da {comm['descricao']} influencia o preço da ação na direção oposta"
                    
                    commodities_empresa.append({
                        'commodity': comm['nome'],
                        'ticker_commodity': comm['ticker'],
                        'descricao': comm['descricao'],
                        'direcao': direcao,
                        'impacto': descricao_impacto
                    })
                    break
    
    # Se não encontrou commodities específicas, adicionar genéricas
    if not commodities_empresa:
        # Commodities genéricas por tipo de empresa
        if 'Bank' in setor or 'Financial' in setor:
            # Bancos e financeiras são influenciados por juros, mas não diretamente por commodities
            pass
        elif 'Healthcare' in setor or 'Pharmaceutical' in setor:
            # Saúde e farmacêuticas têm baixa exposição direta a commodities
            pass
        else:
            # Adicionar commodities genéricas para outros setores
            for comm in ['Ouro', 'Prata', 'Petroleo_WTI', 'Cobre']:
                for c in COMMODITIES_LIST:
                    if c['nome'] == comm:
                        commodities_empresa.append({
                            'commodity': c['nome'],
                            'ticker_commodity': c['ticker'],
                            'descricao': c['descricao'],
                            'direcao': 'positiva',
                            'impacto': f"Preço da {c['descricao']} influencia indiretamente o preço da ação"
                        })
                        break
    
    return commodities_empresa

def obter_fundamentos(ticker):
    """
    Obtém dados fundamentalistas completos do ticker.
    
    Retorna um dicionário com:
    - Margem Líquida
    - ROE (Return on Equity)
    - ROA (Return on Assets)
    - Margem EBITDA
    - P/L (Preço/Lucro) - histórico
    - PE (P/L projetado)
    - P/VPA (Preço/Valor Patrimonial)
    - EV/EBITDA
    - EBITDA
    - DY (Dividend Yield)
    - Dívida Líquida / EBITDA
    - Crescimento da Receita (vs. ano anterior)
    - Crescimento do Lucro (vs. ano anterior)
    """
    try:
        info = ticker.info
        
        # Indicadores de Valuation
        pe_historico = info.get('trailingPE', np.nan)
        pe_projetado = info.get('forwardPE', np.nan)
        p_vpa = info.get('priceToBook', np.nan)
        ev_ebitda = info.get('enterpriseToEbitda', np.nan)
        
        # Indicadores de Rentabilidade
        margem_liquida = info.get('profitMargins', np.nan)
        if margem_liquida:
            margem_liquida = margem_liquida * 100
        
        roe = info.get('returnOnEquity', np.nan)
        if roe:
            roe = roe * 100
        
        roa = info.get('returnOnAssets', np.nan)
        if roa:
            roa = roa * 100
        
        margem_ebitda = info.get('ebitdaMargins', np.nan)
        if margem_ebitda:
            margem_ebitda = margem_ebitda * 100
        
        # EBITDA e Dívida
        ebitda = info.get('ebitda', np.nan)
        divida_liquida = info.get('totalDebt', np.nan)
        
        # Calcular Dívida Líquida / EBITDA
        divida_ebitda = np.nan
        if not np.isnan(divida_liquida) and not np.isnan(ebitda) and ebitda > 0:
            divida_ebitda = divida_liquida / ebitda
        
        # Dividend Yield (já vem em %)
        dy = info.get('dividendYield', np.nan)
        if dy:
            dy = dy * 100
        
        # Crescimento (dados do Yahoo)
        crescimento_receita = info.get('revenueGrowth', np.nan)
        if crescimento_receita:
            crescimento_receita = crescimento_receita * 100
        
        crescimento_lucro = info.get('earningsGrowth', np.nan)
        if crescimento_lucro:
            crescimento_lucro = crescimento_lucro * 100
        
        return {
            'Margem_Liquida': round(margem_liquida, 2) if not np.isnan(margem_liquida) else np.nan,
            'ROE': round(roe, 2) if not np.isnan(roe) else np.nan,
            'ROA': round(roa, 2) if not np.isnan(roa) else np.nan,
            'Margem_EBITDA': round(margem_ebitda, 2) if not np.isnan(margem_ebitda) else np.nan,
            'PL_Historico': round(pe_historico, 2) if not np.isnan(pe_historico) else np.nan,
            'PL_Projetado': round(pe_projetado, 2) if not np.isnan(pe_projetado) else np.nan,
            'P_VPA': round(p_vpa, 2) if not np.isnan(p_vpa) else np.nan,
            'EV_EBITDA': round(ev_ebitda, 2) if not np.isnan(ev_ebitda) else np.nan,
            'EBITDA': round(ebitda, 2) if not np.isnan(ebitda) else np.nan,
            'DY': round(dy, 2) if not np.isnan(dy) else np.nan,
            'Divida_Liquida_EBITDA': round(divida_ebitda, 2) if not np.isnan(divida_ebitda) else np.nan,
            'Crescimento_Receita': round(crescimento_receita, 2) if not np.isnan(crescimento_receita) else np.nan,
            'Crescimento_Lucro': round(crescimento_lucro, 2) if not np.isnan(crescimento_lucro) else np.nan,
        }
    except:
        return {}

def obter_info_geral(ticker):
    """
    Obtém informações gerais da empresa.
    
    Retorna um dicionário com:
    - Nome completo da empresa
    - País sede (nome completo)
    - Sigla do país
    - Setor da empresa
    """
    try:
        info = ticker.info
        
        # Nome completo
        nome = info.get('longName', info.get('shortName', info.get('name', '')))
        
        # País
        pais = info.get('country', '')
        
        # Mapeamento de siglas para países comuns
        siglas_paises = {
            'United States': 'US', 'USA': 'US', 'America': 'US',
            'Brazil': 'BR', 'Brasil': 'BR',
            'United Kingdom': 'UK', 'UK': 'UK', 'England': 'UK',
            'Germany': 'DE', 'Alemanha': 'DE',
            'France': 'FR', 'França': 'FR',
            'Japan': 'JP', 'Japão': 'JP',
            'China': 'CN', 'China': 'CN',
            'Canada': 'CA', 'Canadá': 'CA',
            'Australia': 'AU', 'Austrália': 'AU',
            'India': 'IN', 'Índia': 'IN',
            'Switzerland': 'CH', 'Suíça': 'CH',
            'Netherlands': 'NL', 'Holanda': 'NL',
            'Spain': 'ES', 'Espanha': 'ES',
            'Italy': 'IT', 'Itália': 'IT',
            'South Korea': 'KR', 'Coreia do Sul': 'KR',
            'Hong Kong': 'HK',
            'Taiwan': 'TW', 'Taiwan': 'TW',
            'Singapore': 'SG', 'Singapura': 'SG'
        }
        sigla_pais = siglas_paises.get(pais, pais[:2].upper() if pais else '')
        
        # Setor
        setor = info.get('sector', info.get('industry', ''))
        
        return {
            'Nome': nome,
            'Pais': pais,
            'Sigla_Pais': sigla_pais,
            'Setor': setor,
        }
    except:
        return {}

def obter_historico_valor_mercado(ticker, dados_ohlcv):
    """Calcula Market Cap histórico = Close × Shares Outstanding"""
    try:
        info = ticker.info
        shares_atual = info.get('sharesOutstanding', 0)
        
        if shares_atual <= 0:
            market_cap_atual = info.get('marketCap', 0)
            preco_atual = dados_ohlcv['Close'].iloc[-1] if len(dados_ohlcv) > 0 else 0
            if market_cap_atual > 0 and preco_atual > 0:
                shares_atual = market_cap_atual / preco_atual
            else:
                return pd.DataFrame()
        
        splits = ticker.splits
        df_mc = pd.DataFrame(index=dados_ohlcv.index)
        df_mc['Close'] = dados_ohlcv['Close']
        df_mc['Shares_Outstanding'] = shares_atual
        
        if len(splits) > 0:
            splits = splits.sort_index(ascending=False)
            for split_date, split_ratio in splits.items():
                mask = df_mc.index < split_date
                df_mc.loc[mask, 'Shares_Outstanding'] = df_mc.loc[mask, 'Shares_Outstanding'] / split_ratio
        
        df_mc['Shares_Outstanding'] = df_mc['Shares_Outstanding'].round(0).astype(int)
        df_mc['Market_Cap'] = (df_mc['Close'] * df_mc['Shares_Outstanding']).round(2)
        df_mc['Market_Cap_B'] = (df_mc['Market_Cap'] / 1_000_000_000).round(2)
        df_mc['Market_Cap_Change_Pct'] = (df_mc['Market_Cap'].pct_change() * 100).round(2)
        
        if 'Volume' in dados_ohlcv.columns:
            df_mc['Volume_Dollar'] = (dados_ohlcv['Volume'] * dados_ohlcv['Close']).round(2)
        
        return df_mc
    except:
        return pd.DataFrame()

def obter_info_dividendos(ticker):
    """Obtém TODAS as informações de dividendos"""
    info = {
        'dividend_yield': 0.0,
        'dividend_rate': 0.0,
        'payout_ratio': 0.0,
        'ex_dividend_date': 'N/A',
        'last_dividend': 0.0,
        'dividend_count_1y': 0,
        'total_dividends_1y': 0.0
    }
    try:
        si = ticker.info
        info['dividend_yield'] = round(si.get('dividendYield', 0) * 100, 2) if si.get('dividendYield') else 0.0
        info['dividend_rate'] = round(si.get('dividendRate', 0), 2) if si.get('dividendRate') else 0.0
        info['payout_ratio'] = round(si.get('payoutRatio', 0) * 100, 2) if si.get('payoutRatio') else 0.0
        
        ex_date = si.get('exDividendDate')
        if ex_date:
            info['ex_dividend_date'] = datetime.fromtimestamp(ex_date).strftime('%Y-%m-%d')
        
        dividendos = ticker.dividends
        if len(dividendos) > 0:
            info['last_dividend'] = round(dividendos.iloc[-1], 4)
            one_year_ago = datetime.now() - timedelta(days=365)
            div_1y = dividendos[dividendos.index >= one_year_ago]
            info['dividend_count_1y'] = len(div_1y)
            info['total_dividends_1y'] = round(div_1y.sum(), 4)
    except:
        pass
    return info

def criar_dataframe_dividendos(ticker, info_div):
    """
    Cria DataFrame completo de dividendos com TODOS os campos solicitados:
    - Dividends (histórico de pagamentos por data)
    - Stock_Splits (histórico de splits)
    - Dividend_Yield, Dividend_Rate, Payout_Ratio
    - Dividend_1Y_Total, Dividend_1Y_Count
    - Last_Dividend, Ex_Dividend_Date
    """
    dividendos = ticker.dividends
    splits = ticker.splits
    
    if len(dividendos) == 0 and len(splits) == 0:
        return pd.DataFrame()
    
    # Criar índice combinado de todas as datas (dividendos + splits)
    todas_datas = set()
    if len(dividendos) > 0:
        todas_datas.update(dividendos.index)
    if len(splits) > 0:
        todas_datas.update(splits.index)
    
    todas_datas = sorted(todas_datas)
    
    # Criar DataFrame
    df_div = pd.DataFrame(index=todas_datas)
    df_div.index.name = 'Date'
    
    # ── Dividends (valor pago por ação na data) ──
    df_div['Dividends'] = 0.0
    if len(dividendos) > 0:
        for dt, val in dividendos.items():
            df_div.loc[dt, 'Dividends'] = round(val, 4)
    
    # ── Stock Splits (ratio de desdobramento) ──
    df_div['Stock_Splits'] = 1.0
    if len(splits) > 0:
        for dt, val in splits.items():
            df_div.loc[dt, 'Stock_Splits'] = round(val, 4)
    
    # ── Métricas consolidadas (mesmo valor em todas as linhas) ──
    df_div['Dividend_Yield'] = info_div['dividend_yield']        # Rendimento anual (%)
    df_div['Dividend_Rate'] = info_div['dividend_rate']          # Valor anual estimado por ação
    df_div['Payout_Ratio'] = info_div['payout_ratio']            # % do lucro pago
    df_div['Dividend_1Y_Total'] = info_div['total_dividends_1y'] # Total 12 meses
    df_div['Dividend_1Y_Count'] = info_div['dividend_count_1y']  # Nº pagamentos 12 meses
    df_div['Last_Dividend'] = info_div['last_dividend']          # Último dividendo pago
    df_div['Ex_Dividend_Date'] = info_div['ex_dividend_date']    # Próxima data ex
    
    # Ordenar por data (mais recente primeiro)
    df_div = df_div.sort_index(ascending=False)
    
    return df_div

def formatar_valor_monetario(valor):
    if valor >= 1_000_000_000_000: return f"${valor/1_000_000_000_000:.2f}T"
    elif valor >= 1_000_000_000: return f"${valor/1_000_000_000:.2f}B"
    elif valor >= 1_000_000: return f"${valor/1_000_000:.2f}M"
    elif valor >= 1_000: return f"${valor/1_000:.2f}K"
    else: return f"${valor:.2f}"

# ============================================
# INDICADORES TÉCNICOS
# ============================================

def calcular_rsi(series, periodo=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=periodo, min_periods=1).mean()
    avg_loss = loss.rolling(window=periodo, min_periods=1).mean()
    rs = avg_gain / avg_loss
    return (100 - (100 / (1 + rs))).round(2)

def calcular_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = (ema_fast - ema_slow).round(2)
    signal_line = macd_line.ewm(span=signal, adjust=False).mean().round(2)
    macd_histogram = (macd_line - signal_line).round(2)
    return macd_line, signal_line, macd_histogram

def calcular_bollinger_bands(series, periodo=20, num_std=2):
    sma = series.rolling(window=periodo).mean()
    std = series.rolling(window=periodo).std()
    upper = (sma + (std * num_std)).round(2)
    lower = (sma - (std * num_std)).round(2)
    bandwidth = (((upper - lower) / sma) * 100).round(2)
    return upper, sma.round(2), lower, bandwidth

def calcular_fibonacci_retracement(high, low, close, window=50):
    fib = pd.DataFrame(index=close.index)
    hh = high.rolling(window=window, min_periods=1).max()
    ll = low.rolling(window=window, min_periods=1).min()
    diff = hh - ll
    fib['Fib_0'] = ll.round(2)
    fib['Fib_236'] = (ll + diff * 0.236).round(2)
    fib['Fib_382'] = (ll + diff * 0.382).round(2)
    fib['Fib_50'] = (ll + diff * 0.5).round(2)
    fib['Fib_618'] = (ll + diff * 0.618).round(2)
    fib['Fib_786'] = (ll + diff * 0.786).round(2)
    fib['Fib_1'] = hh.round(2)
    fib['Fib_1_272'] = (hh + diff * 0.272).round(2)
    fib['Fib_1_618'] = (hh + diff * 0.618).round(2)
    return fib

def calcular_fibonacci_position(close, high, low, window=50):
    fp = pd.DataFrame(index=close.index)
    hh = high.rolling(window=window, min_periods=1).max()
    ll = low.rolling(window=window, min_periods=1).min()
    diff = hh - ll
    fp['Fib_Position'] = ((close - ll) / diff.replace(0, np.nan)).round(2).clip(0, 2)
    niveis = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618]
    def encontrar_nivel(pos):
        if pd.isna(pos): return 'N/A', 0
        for i in range(len(niveis)-1):
            if niveis[i] <= pos < niveis[i+1]: return f'{niveis[i]:.2f}', round(niveis[i+1]-pos, 2)
        return f'{niveis[-1]:.2f}', 0
    na = fp['Fib_Position'].apply(encontrar_nivel)
    fp['Fib_Level_Current'] = na.apply(lambda x: x[0])
    fp['Fib_Distance_Next'] = na.apply(lambda x: x[1])
    fp['Fib_Zone'] = 'Neutra'
    fp.loc[fp['Fib_Position'] < 0.236, 'Fib_Zone'] = 'Suporte Forte'
    fp.loc[(fp['Fib_Position'] >= 0.236) & (fp['Fib_Position'] < 0.382), 'Fib_Zone'] = 'Suporte'
    fp.loc[(fp['Fib_Position'] >= 0.382) & (fp['Fib_Position'] < 0.618), 'Fib_Zone'] = 'Zona de Consolidação'
    fp.loc[(fp['Fib_Position'] >= 0.618) & (fp['Fib_Position'] < 0.786), 'Fib_Zone'] = 'Resistência'
    fp.loc[(fp['Fib_Position'] >= 0.786) & (fp['Fib_Position'] <= 1.0), 'Fib_Zone'] = 'Resistência Forte'
    fp.loc[fp['Fib_Position'] > 1.0, 'Fib_Zone'] = 'Rompimento'
    return fp

def processar_indicadores(dados):
    """Calcula todos os indicadores técnicos"""
    if dados.empty: return {}
    
    if isinstance(dados.columns, pd.MultiIndex):
        dados.columns = ['_'.join(col).strip() for col in dados.columns.values]
        rename = {}
        for col in dados.columns:
            if 'open' in col.lower(): rename[col] = 'Open'
            elif 'high' in col.lower(): rename[col] = 'High'
            elif 'low' in col.lower(): rename[col] = 'Low'
            elif 'close' in col.lower(): rename[col] = 'Close'
            elif 'volume' in col.lower(): rename[col] = 'Volume'
        dados = dados.rename(columns=rename)
    
    if 'Close' not in dados.columns: return {}
    
    close = dados['Close'].round(2)
    high = dados['High'].round(2) if 'High' in dados.columns else close
    low = dados['Low'].round(2) if 'Low' in dados.columns else close
    open_p = dados['Open'].round(2) if 'Open' in dados.columns else close
    volume = dados['Volume'].round(0) if 'Volume' in dados.columns else pd.Series(0, index=dados.index)
    
    resultado = {}
    
    # RSI
    rsi = pd.DataFrame(index=dados.index)
    rsi['RSI_7'] = calcular_rsi(close, 7)
    rsi['RSI_14'] = calcular_rsi(close, 14)
    rsi['RSI_Sinal'] = 'Neutro'
    rsi.loc[rsi['RSI_14'] > 70, 'RSI_Sinal'] = 'Sobrecomprado'
    rsi.loc[rsi['RSI_14'] < 30, 'RSI_Sinal'] = 'Sobrevendido'
    resultado['rsi'] = rsi
    
    # MACD
    macd = pd.DataFrame(index=dados.index)
    ml, sl, mh = calcular_macd(close)
    macd['MACD_Line'] = ml
    macd['MACD_Signal'] = sl
    macd['MACD_Histogram'] = mh
    macd['MACD_Sinal'] = 'Neutro'
    macd.loc[macd['MACD_Line'] > macd['MACD_Signal'], 'MACD_Sinal'] = 'Compra'
    macd.loc[macd['MACD_Line'] < macd['MACD_Signal'], 'MACD_Sinal'] = 'Venda'
    resultado['macd'] = macd
    
    # Bollinger
    boll = pd.DataFrame(index=dados.index)
    bu, bm, bl, bw = calcular_bollinger_bands(close)
    boll['BB_Upper'] = bu
    boll['BB_Middle'] = bm
    boll['BB_Lower'] = bl
    boll['BB_Width'] = bw
    bb_range = (boll['BB_Upper'] - boll['BB_Lower']).replace(0, np.nan)
    boll['BB_Position'] = ((close - boll['BB_Lower']) / bb_range).round(2).clip(0, 1)
    boll['BB_Sinal'] = 'Neutro'
    boll.loc[close > boll['BB_Upper'], 'BB_Sinal'] = 'Sobrecomprado'
    boll.loc[close < boll['BB_Lower'], 'BB_Sinal'] = 'Sobrevendido'
    resultado['bollinger'] = boll
    
    # Fibonacci
    fib_levels = calcular_fibonacci_retracement(high, low, close)
    fib_pos = calcular_fibonacci_position(close, high, low)
    fib = pd.concat([fib_levels, fib_pos], axis=1)
    fib['Fib_Buy_Signal'] = ((close <= fib['Fib_382']*1.01) & (close >= fib['Fib_382']*0.99) | 
                              (close <= fib['Fib_618']*1.01) & (close >= fib['Fib_618']*0.99)).astype(int)
    fib['Fib_Sell_Signal'] = ((close <= fib['Fib_786']*1.01) & (close >= fib['Fib_786']*0.99) | 
                               (close <= fib['Fib_1']*1.01) & (close >= fib['Fib_1']*0.99)).astype(int)
    resultado['fibonacci'] = fib
    
    # Médias Móveis
    ma = pd.DataFrame(index=dados.index)
    ma['MA_7'] = close.rolling(7, min_periods=1).mean().round(2)
    ma['MA_14'] = close.rolling(14, min_periods=1).mean().round(2)
    ma['MA_30'] = close.rolling(30, min_periods=1).mean().round(2)
    ma['MA_50'] = close.rolling(50, min_periods=1).mean().round(2)
    ma['MA_200'] = close.rolling(200, min_periods=1).mean().round(2)
    ma['Sinal_MA_7_14'] = np.where(ma['MA_7'] > ma['MA_14'], 1, -1)
    ma['Sinal_MA_50_200'] = np.where(ma['MA_50'] > ma['MA_200'], 1, -1)
    resultado['medias_moveis'] = ma
    
    # Volatilidade
    vol = pd.DataFrame(index=dados.index)
    vol['Returns'] = close.pct_change().round(4)
    vol['Returns_Log'] = np.log(close / close.shift(1)).round(4)
    vol['Volatilidade_20'] = (close.pct_change().rolling(20).std() * np.sqrt(252)).round(2)
    vol['Range_Diario'] = (high - low).round(2)
    vol['Range_Percentual'] = ((vol['Range_Diario'] / close.replace(0, np.nan)) * 100).round(2)
    vol['Gap'] = (open_p - close.shift(1)).round(2)
    vol['Gap_Percentual'] = ((vol['Gap'] / close.shift(1).replace(0, np.nan)) * 100).round(2)
    vol['Volume_Medio_20'] = volume.rolling(20, min_periods=1).mean().round(0)
    vol['Volume_Ratio'] = (volume / vol['Volume_Medio_20'].replace(0, np.nan)).round(2).fillna(1.0)
    resultado['volatilidade'] = vol
    
    # Tendência
    tend = pd.DataFrame(index=dados.index)
    tend['Tendencia_7d'] = 'Baixa'
    tend.loc[close > ma['MA_7'], 'Tendencia_7d'] = 'Alta'
    tend['Tendencia_50d'] = 'Baixa'
    tend.loc[close > ma['MA_50'], 'Tendencia_50d'] = 'Alta'
    ma50_shift = ma['MA_50'].shift(5).replace(0, np.nan)
    tend['Forca_Tendencia'] = (((ma['MA_50'] - ma['MA_50'].shift(5)) / ma50_shift) * 100).round(2)
    tend['Forca_Movimento'] = ((close - open_p) / (high - low).replace(0, np.nan)).round(2).fillna(0)
    tend['Velas_Alta_Consecutivas'] = 0
    count = 0
    sinal = (close > open_p).astype(int)
    for i in range(len(tend)):
        count = count + 1 if sinal.iloc[i] == 1 else 0
        tend.iloc[i, tend.columns.get_loc('Velas_Alta_Consecutivas')] = count
    resultado['tendencia'] = tend
    
    return resultado

# ============================================
# CONFIGURAÇÕES PRINCIPAIS
# ============================================

offset = 0
limit = 10000
start_date = '2015-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# Criar estrutura de pastas
PASTAS = {
    'cotacoes': 'historicos/cotacoes',
    'dividendos': 'historicos/dividendos',
    'valor_mercado': 'historicos/valor_mercado',
    'fundamentos': 'historicos/fundamentos',
    'info_geral': 'historicos/info_geral',
    'commodities': 'historicos/commodities',
    'rsi': 'historicos/indicadores/rsi',
    'macd': 'historicos/indicadores/macd',
    'bollinger': 'historicos/indicadores/bollinger',
    'fibonacci': 'historicos/indicadores/fibonacci',
    'medias_moveis': 'historicos/indicadores/medias_moveis',
    'volatilidade': 'historicos/indicadores/volatilidade',
    'tendencia': 'historicos/indicadores/tendencia'
}

for nome, pasta in PASTAS.items():
    Path(pasta).mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("📁 ESTRUTURA DE PASTAS CRIADA")
print("=" * 70)
for nome, pasta in PASTAS.items():
    print(f"   ✅ {pasta}/")

# ============================================
# CARREGAR SÍMBOLOS SELECIONADOS
# ============================================

# Carregar o CSV completo
try:
    data = pd.read_csv("data/nasdaq-listed-symbols.csv")
    print(f"\n✅ Arquivo carregado: {data.shape[0]} linhas, {data.shape[1]} colunas")
except FileNotFoundError:
    print("\n❌ Arquivo 'data/nasdaq-listed-symbols.csv' não encontrado!")
    print("   Verifique o caminho do arquivo.")
    exit()

# Verificar qual coluna contém os símbolos
coluna_simbolos = None
for col in data.columns:
    if col.upper() in ['SYMBOL', 'TICKER', 'SECURITY ID', 'Symbol']:
        coluna_simbolos = col
        break

# Se não encontrou nenhuma das colunas padrão, usa a primeira coluna
if coluna_simbolos is None:
    coluna_simbolos = data.columns[0]
    print(f"ℹ️ Usando coluna '{coluna_simbolos}' como coluna de símbolos")

# Filtrar apenas os símbolos que estão na lista simbolos_usados
data_filtrado = data[data[coluna_simbolos].isin(simbolos_usados)]

# Extrair a lista de símbolos encontrados
symbols = data_filtrado[coluna_simbolos].tolist()

# Mostrar quantos foram encontrados
print(f"\n📊 Símbolos encontrados: {len(symbols)}/{len(simbolos_usados)}")

# Verificar quais símbolos da lista não foram encontrados
simbolos_nao_encontrados = set(simbolos_usados) - set(symbols)
if simbolos_nao_encontrados:
    print(f"\n⚠️ Símbolos NÃO encontrados no arquivo:")
    for s in sorted(simbolos_nao_encontrados):
        print(f"   ❌ {s}")
else:
    print(f"\n✅ TODOS os {len(simbolos_usados)} símbolos foram encontrados!")

# Verificar se algum símbolo foi encontrado
if not symbols:
    print("\n❌ Nenhum símbolo encontrado! Verifique a lista e o arquivo.")
    exit()

print(f"\n📋 Símbolos que serão processados:")
print(f"   {symbols}")

print("\n" + "=" * 70)
print("📥 DOWNLOAD COMPLETO")
print("=" * 70)
print(f"Símbolos: {offset} a {min(offset + limit, len(symbols))} de {len(symbols):,}")
print(f"Período: {start_date} até {end_date}")
print("=" * 70)

end = min(offset + limit, len(symbols))
valid_symbols = []
div_info_list = []
mc_resumo_list = []
fundamentos_list = []
info_geral_list = []
commodities_list = []

for i in range(offset, end):
    s = symbols[i]
    print(f"[{i+1}/{end}] {s}...", end=" ")
    
    try:
        ticker = yf.Ticker(s)
        dados = ticker.history(start=start_date, end=end_date)
        
        if len(dados) > 0:
            # Arredondar OHLCV
            for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
                if col in dados.columns: 
                    dados[col] = dados[col].round(2)
            if 'Volume' in dados.columns: 
                dados['Volume'] = dados['Volume'].round(0).astype(int)
            
            # Info dividendos
            info_div = obter_info_dividendos(ticker)
            
            # Info fundamentos
            info_fund = obter_fundamentos(ticker)
            
            # Info geral
            info_geral = obter_info_geral(ticker)
            
            # Commodities da empresa
            commodities_empresa = obter_commodities_por_empresa(s, info_geral.get('Setor', ''))
            
            # Market Cap histórico
            df_mc = obter_historico_valor_mercado(ticker, dados)
            mc_atual = df_mc['Market_Cap'].iloc[-1] if not df_mc.empty else 0
            
            # ── 1. SALVAR COTAÇÕES (OHLCV) ──
            dados_out = dados.reset_index()
            dados_out['Date'] = pd.to_datetime(dados_out['Date']).dt.strftime('%Y-%m-%d')
            dados_out.to_csv(f"{PASTAS['cotacoes']}/{s}.csv", index=False, float_format='%.2f')
            
            # ── 2. SALVAR DIVIDENDOS (COMPLETO) ──
            df_div = criar_dataframe_dividendos(ticker, info_div)
            if not df_div.empty:
                df_div_out = df_div.reset_index()
                df_div_out['Date'] = pd.to_datetime(df_div_out['Date']).dt.strftime('%Y-%m-%d')
                df_div_out.to_csv(f"{PASTAS['dividendos']}/{s}.csv", index=False, float_format='%.4f')
            
            # ── 3. SALVAR VALOR DE MERCADO ──
            if not df_mc.empty:
                mc_out = df_mc.reset_index()
                mc_out['Date'] = pd.to_datetime(mc_out['Date']).dt.strftime('%Y-%m-%d')
                cols = ['Date', 'Close', 'Shares_Outstanding', 'Market_Cap', 
                       'Market_Cap_B', 'Market_Cap_Change_Pct', 'Volume_Dollar']
                mc_out[[c for c in cols if c in mc_out.columns]].to_csv(
                    f"{PASTAS['valor_mercado']}/{s}.csv", index=False, float_format='%.2f')
            
            # ── 4. SALVAR FUNDAMENTOS ──
            if info_fund:
                df_fund = pd.DataFrame([info_fund])
                df_fund.insert(0, 'Symbol', s)
                df_fund.to_csv(f"{PASTAS['fundamentos']}/{s}.csv", index=False, float_format='%.2f')
                fundamentos_list.append({'Symbol': s, **info_fund})
            
            # ── 5. SALVAR INFO GERAL ──
            if info_geral:
                df_info = pd.DataFrame([info_geral])
                df_info.insert(0, 'Symbol', s)
                df_info.to_csv(f"{PASTAS['info_geral']}/{s}.csv", index=False)
                info_geral_list.append({'Symbol': s, **info_geral})
            
            # ── 6. SALVAR COMMODITIES ──
            if commodities_empresa:
                df_comm = pd.DataFrame(commodities_empresa)
                df_comm.insert(0, 'Symbol', s)
                df_comm.to_csv(f"{PASTAS['commodities']}/{s}.csv", index=False)
                for comm in commodities_empresa:
                    commodities_list.append({
                        'Symbol': s,
                        'Setor': info_geral.get('Setor', ''),
                        **comm
                    })
            
            # ── 7. CALCULAR E SALVAR INDICADORES ──
            indicadores = processar_indicadores(dados)
            for nome, df_ind in indicadores.items():
                if not df_ind.empty and nome in PASTAS:
                    ind_out = df_ind.reset_index()
                    ind_out['Date'] = pd.to_datetime(ind_out['Date']).dt.strftime('%Y-%m-%d')
                    ind_out.to_csv(f"{PASTAS[nome]}/{s}.csv", index=False, float_format='%.2f')
            
            # Acumular resumos
            div_info_list.append({'Symbol': s, **info_div})
            mc_resumo_list.append({'Symbol': s, 'Market_Cap_Atual': mc_atual})
            valid_symbols.append(s)
            
            mc_str = formatar_valor_monetario(mc_atual)
            div_icon = "💰" if info_div['total_dividends_1y'] > 0 else "  "
            comm_count = len(commodities_empresa)
            print(f"✅ {len(dados)}d | {mc_str} | {div_icon} {len(indicadores)} ind | 📊 Fund | ℹ️ Info | 🛢️ {comm_count} comm")
        else:
            print(f"⚠️ Sem dados")
    except Exception as e:
        print(f"❌ {str(e)[:60]}")
    
    time.sleep(0.3)

# ============================================
# RESUMOS FINAIS
# ============================================

print("\n" + "=" * 70)
print("📊 RESUMOS CONSOLIDADOS")
print("=" * 70)

if div_info_list:
    pd.DataFrame(div_info_list).to_csv('resumo_dividendos.csv', index=False)
    print(f"✅ resumo_dividendos.csv ({len(div_info_list)} ações)")

if mc_resumo_list:
    pd.DataFrame(mc_resumo_list).to_csv('resumo_valor_mercado.csv', index=False)
    print(f"✅ resumo_valor_mercado.csv ({len(mc_resumo_list)} ações)")

if fundamentos_list:
    pd.DataFrame(fundamentos_list).to_csv('resumo_fundamentos.csv', index=False)
    print(f"✅ resumo_fundamentos.csv ({len(fundamentos_list)} ações)")

if info_geral_list:
    pd.DataFrame(info_geral_list).to_csv('resumo_info_geral.csv', index=False)
    print(f"✅ resumo_info_geral.csv ({len(info_geral_list)} ações)")

if commodities_list:
    pd.DataFrame(commodities_list).to_csv('resumo_commodities.csv', index=False)
    print(f"✅ resumo_commodities.csv ({len(commodities_list)} registros)")

if valid_symbols:
    pd.DataFrame({'Symbol': valid_symbols}).to_csv('symbols_valid.csv', index=False)
    print(f"✅ symbols_valid.csv ({len(valid_symbols)} símbolos)")

print(f"\n📁 ARQUIVOS GERADOS:")
for nome, pasta in PASTAS.items():
    count = len([f for f in os.listdir(pasta) if f.endswith('.csv')]) if os.path.exists(pasta) else 0
    print(f"   {pasta}/ → {count} arquivos")

print("=" * 70)
print("✅ DOWNLOAD CONCLUÍDO!")