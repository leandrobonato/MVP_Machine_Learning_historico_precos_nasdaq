import pandas as pd
import yfinance as yf
import numpy as np
import os
import time
import sys
from pathlib import Path
from datetime import datetime

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============================================
# FUNÇÕES PARA CÁLCULO DE INDICADORES TÉCNICOS
# ============================================

def calcular_rsi(series, periodo=14):
    """Calcula o RSI (Relative Strength Index)"""
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    avg_gain = gain.rolling(window=periodo, min_periods=1).mean()
    avg_loss = loss.rolling(window=periodo, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.round(2)

def calcular_macd(series, fast=12, slow=26, signal=9):
    """Calcula o MACD"""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    
    macd_line = (ema_fast - ema_slow).round(2)
    signal_line = macd_line.ewm(span=signal, adjust=False).mean().round(2)
    macd_histogram = (macd_line - signal_line).round(2)
    
    return macd_line, signal_line, macd_histogram

def calcular_bollinger_bands(series, periodo=20, num_std=2):
    """Calcula as Bandas de Bollinger"""
    sma = series.rolling(window=periodo).mean()
    std = series.rolling(window=periodo).std()
    
    upper_band = (sma + (std * num_std)).round(2)
    lower_band = (sma - (std * num_std)).round(2)
    bandwidth = (((upper_band - lower_band) / sma) * 100).round(2)
    
    return upper_band, sma.round(2), lower_band, bandwidth

# ============================================
# FIBONACCI RETRACEMENT
# ============================================

def calcular_fibonacci_retracement(high, low, close, window=50):
    """Calcula os níveis de Fibonacci Retracement"""
    
    fib_levels = pd.DataFrame(index=close.index)
    
    highest_high = high.rolling(window=window, min_periods=1).max()
    lowest_low = low.rolling(window=window, min_periods=1).min()
    diff = highest_high - lowest_low
    
    fib_levels['Fib_0'] = lowest_low.round(2)
    fib_levels['Fib_236'] = (lowest_low + diff * 0.236).round(2)
    fib_levels['Fib_382'] = (lowest_low + diff * 0.382).round(2)
    fib_levels['Fib_50'] = (lowest_low + diff * 0.5).round(2)
    fib_levels['Fib_618'] = (lowest_low + diff * 0.618).round(2)
    fib_levels['Fib_786'] = (lowest_low + diff * 0.786).round(2)
    fib_levels['Fib_1'] = highest_high.round(2)
    fib_levels['Fib_1_272'] = (highest_high + diff * 0.272).round(2)
    fib_levels['Fib_1_618'] = (highest_high + diff * 0.618).round(2)
    
    return fib_levels

def calcular_fibonacci_position(close, high, low, window=50):
    """Calcula a posição atual do preço em relação aos níveis de Fibonacci"""
    fib_pos = pd.DataFrame(index=close.index)
    
    highest_high = high.rolling(window=window, min_periods=1).max()
    lowest_low = low.rolling(window=window, min_periods=1).min()
    diff = highest_high - lowest_low
    
    fib_pos['Fib_Position'] = ((close - lowest_low) / diff.replace(0, np.nan)).round(2)
    fib_pos['Fib_Position'] = fib_pos['Fib_Position'].clip(0, 2)
    
    niveis = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618]
    
    def encontrar_nivel(pos):
        if pd.isna(pos):
            return 'N/A', 0
        for i in range(len(niveis) - 1):
            if niveis[i] <= pos < niveis[i + 1]:
                return f'{niveis[i]:.2f}', round(niveis[i + 1] - pos, 2)
        return f'{niveis[-1]:.2f}', 0
    
    niveis_atual = fib_pos['Fib_Position'].apply(encontrar_nivel)
    fib_pos['Fib_Level_Current'] = niveis_atual.apply(lambda x: x[0])
    fib_pos['Fib_Distance_Next'] = niveis_atual.apply(lambda x: x[1])
    
    fib_pos['Fib_Zone'] = 'Neutra'
    fib_pos.loc[fib_pos['Fib_Position'] < 0.236, 'Fib_Zone'] = 'Suporte Forte'
    fib_pos.loc[(fib_pos['Fib_Position'] >= 0.236) & (fib_pos['Fib_Position'] < 0.382), 'Fib_Zone'] = 'Suporte'
    fib_pos.loc[(fib_pos['Fib_Position'] >= 0.382) & (fib_pos['Fib_Position'] < 0.618), 'Fib_Zone'] = 'Zona de Consolidação'
    fib_pos.loc[(fib_pos['Fib_Position'] >= 0.618) & (fib_pos['Fib_Position'] < 0.786), 'Fib_Zone'] = 'Resistência'
    fib_pos.loc[(fib_pos['Fib_Position'] >= 0.786) & (fib_pos['Fib_Position'] <= 1.0), 'Fib_Zone'] = 'Resistência Forte'
    fib_pos.loc[fib_pos['Fib_Position'] > 1.0, 'Fib_Zone'] = 'Rompimento (Extensão)'
    
    return fib_pos

def calcular_fibonacci_signals(close, fib_levels):
    """Gera sinais de trading baseados em Fibonacci"""
    signals = pd.DataFrame(index=close.index)
    
    signals['Fib_Buy_Signal'] = (
        (close <= fib_levels['Fib_382'] * 1.01) & 
        (close >= fib_levels['Fib_382'] * 0.99)
    ) | (
        (close <= fib_levels['Fib_618'] * 1.01) & 
        (close >= fib_levels['Fib_618'] * 0.99)
    )
    
    signals['Fib_Sell_Signal'] = (
        (close <= fib_levels['Fib_786'] * 1.01) & 
        (close >= fib_levels['Fib_786'] * 0.99)
    ) | (
        (close <= fib_levels['Fib_1'] * 1.01) & 
        (close >= fib_levels['Fib_1'] * 0.99)
    )
    
    signals['Fib_Signal_Strength'] = 0
    signals.loc[signals['Fib_Buy_Signal'], 'Fib_Signal_Strength'] = 1
    signals.loc[signals['Fib_Sell_Signal'], 'Fib_Signal_Strength'] = -1
    
    return signals

def processar_dados(dados):
    """Processa os dados OHLCV e adiciona todos os indicadores técnicos"""
    if dados.empty:
        return dados
    
    if isinstance(dados.columns, pd.MultiIndex):
        dados.columns = ['_'.join(col).strip() for col in dados.columns.values]
        
        rename_map = {}
        for col in dados.columns:
            if 'open' in col.lower():
                rename_map[col] = 'Open'
            elif 'high' in col.lower():
                rename_map[col] = 'High'
            elif 'low' in col.lower():
                rename_map[col] = 'Low'
            elif 'close' in col.lower():
                rename_map[col] = 'Close'
            elif 'volume' in col.lower():
                rename_map[col] = 'Volume'
        
        if rename_map:
            dados = dados.rename(columns=rename_map)
    
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    available_cols = [col for col in required_cols if col in dados.columns]
    
    if len(available_cols) < 3:
        return dados
    
    df = pd.DataFrame(index=dados.index)
    
    for col in available_cols:
        df[col] = dados[col]
    
    if 'Close' not in df.columns:
        return dados
    
    close = df['Close'].round(2)
    volume = df['Volume'].round(0) if 'Volume' in df.columns else pd.Series(0, index=df.index)
    high = df['High'].round(2) if 'High' in df.columns else close
    low = df['Low'].round(2) if 'Low' in df.columns else close
    open_price = df['Open'].round(2) if 'Open' in df.columns else close
    
    # Arredondar colunas OHLCV
    for col in available_cols:
        if col == 'Volume':
            df[col] = df[col].round(0)
        else:
            df[col] = df[col].round(2)
    
    # ==========================================
    # 1. VOLUME
    # ==========================================
    if 'Volume' in df.columns:
        df['Volume_Medio_20'] = volume.rolling(window=20, min_periods=1).mean().round(0)
        df['Volume_Medio_50'] = volume.rolling(window=50, min_periods=1).mean().round(0)
        vol_med_20 = df['Volume_Medio_20'].replace(0, np.nan)
        df['Volume_Ratio'] = (volume / vol_med_20).round(2)
        df['Volume_Ratio'] = df['Volume_Ratio'].fillna(1.0)
    
    # ==========================================
    # 2. MÉDIAS MÓVEIS
    # ==========================================
    df['MA_7'] = close.rolling(window=7, min_periods=1).mean().round(2)
    df['MA_14'] = close.rolling(window=14, min_periods=1).mean().round(2)
    df['MA_30'] = close.rolling(window=30, min_periods=1).mean().round(2)
    df['MA_50'] = close.rolling(window=50, min_periods=1).mean().round(2)
    df['MA_200'] = close.rolling(window=200, min_periods=1).mean().round(2)
    
    df['Sinal_MA_7_14'] = np.where(df['MA_7'] > df['MA_14'], 1, -1)
    df['Sinal_MA_50_200'] = np.where(df['MA_50'] > df['MA_200'], 1, -1)
    
    ma_50_safe = df['MA_50'].replace(0, np.nan)
    ma_200_safe = df['MA_200'].replace(0, np.nan)
    df['Dist_MA_50'] = (((close - df['MA_50']) / ma_50_safe) * 100).round(2)
    df['Dist_MA_200'] = (((close - df['MA_200']) / ma_200_safe) * 100).round(2)
    
    # ==========================================
    # 3. RSI
    # ==========================================
    df['RSI_14'] = calcular_rsi(close, 14).round(2)
    df['RSI_7'] = calcular_rsi(close, 7).round(2)
    
    df['RSI_Sinal'] = 'Neutro'
    df.loc[df['RSI_14'] > 70, 'RSI_Sinal'] = 'Sobrecomprado'
    df.loc[df['RSI_14'] < 30, 'RSI_Sinal'] = 'Sobrevendido'
    
    # ==========================================
    # 4. MACD
    # ==========================================
    macd_line, signal_line, macd_hist = calcular_macd(close)
    df['MACD_Line'] = macd_line
    df['MACD_Signal'] = signal_line
    df['MACD_Histogram'] = macd_hist
    
    df['MACD_Sinal'] = 'Neutro'
    df.loc[df['MACD_Line'] > df['MACD_Signal'], 'MACD_Sinal'] = 'Compra'
    df.loc[df['MACD_Line'] < df['MACD_Signal'], 'MACD_Sinal'] = 'Venda'
    
    # ==========================================
    # 5. BANDAS DE BOLLINGER
    # ==========================================
    bb_upper, bb_middle, bb_lower, bb_width = calcular_bollinger_bands(close)
    df['BB_Upper'] = bb_upper
    df['BB_Middle'] = bb_middle
    df['BB_Lower'] = bb_lower
    df['BB_Width'] = bb_width
    
    bb_range = (df['BB_Upper'] - df['BB_Lower']).replace(0, np.nan)
    df['BB_Position'] = ((close - df['BB_Lower']) / bb_range).round(2)
    df['BB_Position'] = df['BB_Position'].clip(0, 1)
    
    df['BB_Sinal'] = 'Neutro'
    df.loc[close > df['BB_Upper'], 'BB_Sinal'] = 'Sobrecomprado'
    df.loc[close < df['BB_Lower'], 'BB_Sinal'] = 'Sobrevendido'
    
    # ==========================================
    # 6. FIBONACCI
    # ==========================================
    
    fib_levels = calcular_fibonacci_retracement(high, low, close, window=50)
    
    df['Fib_0'] = fib_levels['Fib_0']
    df['Fib_236'] = fib_levels['Fib_236']
    df['Fib_382'] = fib_levels['Fib_382']
    df['Fib_50'] = fib_levels['Fib_50']
    df['Fib_618'] = fib_levels['Fib_618']
    df['Fib_786'] = fib_levels['Fib_786']
    df['Fib_1'] = fib_levels['Fib_1']
    df['Fib_1_272'] = fib_levels['Fib_1_272']
    df['Fib_1_618'] = fib_levels['Fib_1_618']
    
    fib_pos = calcular_fibonacci_position(close, high, low, window=50)
    df['Fib_Position'] = fib_pos['Fib_Position']
    df['Fib_Level_Current'] = fib_pos['Fib_Level_Current']
    df['Fib_Distance_Next'] = fib_pos['Fib_Distance_Next']
    df['Fib_Zone'] = fib_pos['Fib_Zone']
    
    fib_signals = calcular_fibonacci_signals(close, fib_levels)
    df['Fib_Buy_Signal'] = fib_signals['Fib_Buy_Signal'].astype(int)
    df['Fib_Sell_Signal'] = fib_signals['Fib_Sell_Signal'].astype(int)
    df['Fib_Signal_Strength'] = fib_signals['Fib_Signal_Strength']
    
    for window_size in [20, 100]:
        fib_multi = calcular_fibonacci_retracement(high, low, close, window=window_size)
        df[f'Fib_382_{window_size}d'] = fib_multi['Fib_382']
        df[f'Fib_618_{window_size}d'] = fib_multi['Fib_618']
    
    df['Fib_Confluencia'] = 0
    for level in ['382', '618']:
        diff_20_50 = (abs(df[f'Fib_{level}_20d'] - df[f'Fib_{level}']) / df[f'Fib_{level}'].replace(0, np.nan)).round(2)
        diff_50_100 = (abs(df[f'Fib_{level}'] - df[f'Fib_{level}_100d']) / df[f'Fib_{level}'].replace(0, np.nan)).round(2)
        df['Fib_Confluencia'] += (diff_20_50 < 0.02).astype(int)
        df['Fib_Confluencia'] += (diff_50_100 < 0.02).astype(int)
    
    df['Fib_Forca_Sinal'] = 'Normal'
    df.loc[df['Fib_Confluencia'] >= 2, 'Fib_Forca_Sinal'] = 'Forte'
    df.loc[df['Fib_Confluencia'] >= 4, 'Fib_Forca_Sinal'] = 'Muito Forte'
    
    # ==========================================
    # 7. INDICADORES ADICIONAIS
    # ==========================================
    
    df['Returns'] = close.pct_change().round(4)
    df['Returns_Log'] = np.log(close / close.shift(1)).round(4)
    
    returns = close.pct_change()
    df['Volatilidade_20'] = (returns.rolling(window=20).std() * np.sqrt(252)).round(2)
    
    df['Range_Diario'] = (high - low).round(2)
    range_pct = ((df['Range_Diario'] / close.replace(0, np.nan)) * 100).round(2)
    df['Range_Percentual'] = range_pct
    
    df['Gap'] = (open_price - close.shift(1)).round(2)
    close_shift = close.shift(1).replace(0, np.nan)
    df['Gap_Percentual'] = ((df['Gap'] / close_shift) * 100).round(2)
    
    high_low_range = (high - low).replace(0, np.nan)
    df['Forca_Movimento'] = ((close - open_price) / high_low_range).round(2).fillna(0)
    
    df['Sinal_Alta'] = (close > open_price).astype(int)
    
    df['Velas_Alta_Consecutivas'] = 0
    count = 0
    for i in range(len(df)):
        if df['Sinal_Alta'].iloc[i] == 1:
            count += 1
        else:
            count = 0
        df.loc[df.index[i], 'Velas_Alta_Consecutivas'] = count
    
    # ==========================================
    # 8. TENDÊNCIAS
    # ==========================================
    df['Tendencia_7d'] = 'Baixa'
    df.loc[close > df['MA_7'], 'Tendencia_7d'] = 'Alta'
    
    df['Tendencia_50d'] = 'Baixa'
    df.loc[close > df['MA_50'], 'Tendencia_50d'] = 'Alta'
    
    ma_50_shift = df['MA_50'].shift(5).replace(0, np.nan)
    df['Forca_Tendencia'] = (((df['MA_50'] - df['MA_50'].shift(5)) / ma_50_shift) * 100).round(2)
    
    return df

# ============================================
# CONFIGURAÇÕES PRINCIPAIS
# ============================================

offset = 0
limit = 10000
start_date = '2016-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

Path('historico_indicadores').mkdir(exist_ok=True)

data = pd.read_csv("data/nasdaq-listed-symbols.csv")
symbols = data['Symbol'].tolist() if 'Symbol' in data.columns else data.iloc[:, 0].tolist()

print(f"Total de simbolos: {len(symbols)}")
print(f"Processando: {offset} a {min(offset + limit, len(symbols))}")
print(f"Periodo: {start_date} ate {end_date}")
print(f"Salvando em: historico_indicadores/")
print("-" * 60)

end = min(offset + limit, len(symbols))
valid_symbols = []
erros = []

for i in range(offset, end):
    s = symbols[i]
    print(f"[{i+1}/{end}] {s}...", end=" ")
    
    try:
        ticker = yf.Ticker(s)
        dados = ticker.history(start=start_date, end=end_date)
        
        if len(dados) > 0:
            dados_completos = processar_dados(dados)
            
            if len(dados_completos) > 0 and len(dados_completos.columns) > 5:
                # Salvar com 2 casas decimais
                dados_completos.to_csv(
                    f'historico_indicadores/{s}.csv',
                    float_format='%.2f',  # Força 2 casas decimais
                    index=True
                )
                valid_symbols.append(s)
                
                num_indicadores = len(dados_completos.columns) - 5
                print(f"✅ {len(dados)} rows | {num_indicadores} indicadores")
            else:
                print(f"⚠️ Dados insuficientes")
        else:
            print(f"⚠️ Sem dados (possivelmente delisted)")
            
    except Exception as e:
        error_msg = str(e)[:80]
        print(f"❌ {error_msg}")
        erros.append(f"{s}: {error_msg}")
    
    time.sleep(0.3)

# ============================================
# RESUMO
# ============================================

print("\n" + "="*60)
print("DOWNLOAD CONCLUIDO")
print("="*60)
print(f"✅ Validos: {len(valid_symbols)}")
print(f"❌ Erros: {len(erros)}")

if valid_symbols:
    pd.DataFrame({'Symbol': valid_symbols}).to_csv('symbols_valid_indicadores.csv', index=False)
    print("📄 symbols_valid_indicadores.csv")

if erros:
    with open('erros_indicadores.txt', 'w') as f:
        for e in erros:
            f.write(e + '\n')

if valid_symbols:
    exemplo = pd.read_csv(f'historico_indicadores/{valid_symbols[0]}.csv')
    print(f"\n📊 Exemplo: {valid_symbols[0]}")
    print(f"   Colunas: {len(exemplo.columns)}")
    print(f"   Últimos valores:")
    print(exemplo[['Date', 'Close', 'MA_50', 'RSI_14', 'Fib_618']].tail(5).to_string(index=False))