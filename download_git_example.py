import pandas as pd
import yfinance as yf
import os
import contextlib
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# CONFIGURACOES
offset = 0
limit = 10000  # Comece com poucos para testar
period = '1d'  # Opcoes: 'max', '10y', '5y', '2y', '1y'
start_date = '2016-01-01'  # Data de inicio para 10 anos atras
end_date = datetime.now().strftime('%Y-%m-%d')  # Data atual

# Criar pasta
Path('hist').mkdir(exist_ok=True)

# Ler CSV
data = pd.read_csv("data/nasdaq-listed-symbols.csv")
symbols = data['Symbol'].tolist() if 'Symbol' in data.columns else data.iloc[:, 0].tolist()

print(f"Total de simbolos: {len(symbols)}")
print(f"Primeiros 10: {symbols[:10]}")
print(f"Periodo: {start_date} ate {end_date}")
print("-" * 50)

end = min(offset + limit, len(symbols))
valid_symbols = []

for i in range(offset, end):
    s = symbols[i]
    print(f"[{i+1}/{end}] Processando {s}...", end=" ")
    
    try:
        # Usar intervalo de datas em vez de period
        dados = yf.download(s, start=start_date, end=end_date, progress=False, timeout=30)
        
        if len(dados) > 0:
            valid_symbols.append(s)
            dados.to_csv(f'hist/{s}.csv')
            print(f"✅ {len(dados)} registros ({dados.index[0].strftime('%Y-%m-%d')} a {dados.index[-1].strftime('%Y-%m-%d')})")
        else:
            print(f"⚠️ Sem dados")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)[:50]}")
    
    time.sleep(0.2)

print("\n" + "="*50)
print(f"DOWNLOAD CONCLUIDO")
print(f"Validos: {len(valid_symbols)} / {end}")

if valid_symbols:
    valid_df = pd.DataFrame({'Symbol': valid_symbols})
    valid_df.to_csv('symbols_valid_meta.csv', index=False)
    print("Lista de simbolos validos salva em: symbols_valid_meta.csv")
    
    # Mostrar exemplo de dados baixados
    print("\nExemplo de dados baixados para AAPL:")
    if 'AAPL' in valid_symbols:
        aapl = pd.read_csv('hist/AAPL.csv')
        print(f"  Registros: {len(aapl)}")
        print(f"  Periodo: {aapl['Date'].iloc[0]} ate {aapl['Date'].iloc[-1]}")
        print(aapl.head())