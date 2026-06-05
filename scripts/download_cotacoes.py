import yfinance as yf
import pandas as pd
import time
from pathlib import Path

# --- CONFIGURAÇÕES ---
# Nome do arquivo com os tickers (mude para 'tickers_teste.txt' enquanto testa)
ARQUIVO_TICKERS = 'tickers.txt'
# Pasta onde os CSVs serão salvos
PASTA_SAIDA = 'dados_historicos'
# Período dos dados (ex: '1y', '2y', '5y', 'max')
PERIODO = 'max'
# Intervalo dos dados ('1d' para diário)
INTERVALO = '1d'
# --------------------

# Cria a pasta de saída se ela não existir
Path(PASTA_SAIDA).mkdir(parents=True, exist_ok=True)

# Lê a lista de tickers do arquivo
with open(ARQUIVO_TICKERS, 'r') as f:
    tickers = [linha.strip() for linha in f if linha.strip()]

print(f"🚀 Iniciando download para {len(tickers)} tickers...")
print(f"📁 Os arquivos serão salvos em: {PASTA_SAIDA}")
print("-" * 30)

tickers_com_erro = []

for i, ticker in enumerate(tickers):
    print(f"[{i+1}/{len(tickers)}] Baixando dados para {ticker}...", end=" ")
    try:
        # Baixa os dados
        dados = yf.download(ticker, period=PERIODO, interval=INTERVALO, progress=False)

        if dados.empty:
            print("⚠️ Nenhum dado encontrado.")
            tickers_com_erro.append(ticker)
            continue

        # Salva em um arquivo CSV
        nome_arquivo = f"{PASTA_SAIDA}/{ticker}.csv"
        dados.to_csv(nome_arquivo)
        print(f"✅ OK! ({len(dados)} registros salvos)")

    except Exception as e:
        print(f"❌ ERRO: {e}")
        tickers_com_erro.append(ticker)

    # Pequena pausa para evitar sobrecarregar o servidor
    time.sleep(0.5)

# --- RELATÓRIO FINAL ---
print("\n" + "="*30)
print("✅ Download concluído!")
print(f"Arquivos salvos em: {PASTA_SAIDA}")
if tickers_com_erro:
    print(f"\n⚠️ Erro ao baixar os seguintes {len(tickers_com_erro)} tickers:")
    for erro in tickers_com_erro:
        print(f"  - {erro}")
