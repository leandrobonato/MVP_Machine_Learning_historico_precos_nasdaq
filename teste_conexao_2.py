import yfinance as yf

# O yfinance moderno já gerencia os cabeçalhos se estiver atualizado
tickers = ["PETR4.SA", "VALE3.SA", "AAPL"]

print("Tentando baixar os dados...")
dados = yf.download(tickers, period="1mo", group_by='ticker')

# Mostra os dados de fechamento se o DataFrame não estiver vazio
if not dados.empty:
    print("\n--- Dados Baixados com Sucesso ---")
    print(dados.xs('Close', level=1, axis=1).head())
else:
    print("\nO DataFrame continua vazio. Verifique a atualização.")
