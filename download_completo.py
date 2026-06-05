"""
================================================================================
DOWNLOAD COMPLETO - COTAÇÕES + DIVIDENDOS + MARKET CAP + INDICADORES TÉCNICOS
================================================================================
Descrição: Pipeline completo de download e processamento de dados financeiros
Fonte: Yahoo Finance (via yfinance)
Período: 2016-01-01 até data atual

ESTRUTURA DE PASTAS:
├── historicos/
│   ├── cotacoes/              # Preços OHLCV
│   │   └── {SIMBOLO}.csv
│   ├── dividendos/            # Histórico de dividendos + métricas
│   │   └── {SIMBOLO}.csv
│   ├── valor_mercado/         # Market Cap histórico
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
# FUNÇÕES AUXILIARES
# ============================================

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
# INDICADORES TÉCNICOS (mantidos iguais)
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
start_date = '2016-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# Criar estrutura de pastas
PASTAS = {
    'cotacoes': 'historicos/cotacoes',
    'dividendos': 'historicos/dividendos',
    'valor_mercado': 'historicos/valor_mercado',
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

# Ler símbolos
data = pd.read_csv("data/nasdaq-listed-symbols.csv")
symbols = data['Symbol'].tolist() if 'Symbol' in data.columns else data.iloc[:, 0].tolist()

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
            
            # ── 4. CALCULAR E SALVAR INDICADORES ──
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
            print(f"✅ {len(dados)}d | {mc_str} | {div_icon} {len(indicadores)} ind")
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

if valid_symbols:
    pd.DataFrame({'Symbol': valid_symbols}).to_csv('symbols_valid.csv', index=False)
    print(f"✅ symbols_valid.csv ({len(valid_symbols)} símbolos)")

print(f"\n📁 ARQUIVOS GERADOS:")
for nome, pasta in PASTAS.items():
    count = len([f for f in os.listdir(pasta) if f.endswith('.csv')]) if os.path.exists(pasta) else 0
    print(f"   {pasta}/ → {count} arquivos")

print("=" * 70)
print("✅ DOWNLOAD CONCLUÍDO!")