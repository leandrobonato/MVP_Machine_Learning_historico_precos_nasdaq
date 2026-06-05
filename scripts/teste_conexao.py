import yfinance as yf
import requests
import sys

print("=" * 50)
print("DIAGNÓSTICO DE CONEXÃO")
print("=" * 50)

# Teste 1: Conexão com Yahoo Finance
print("\n1. Testando conexão com Yahoo Finance...")
try:
    r = requests.get('https://finance.yahoo.com', timeout=10)
    print(f"   ✅ Status: {r.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 2: Versão do yfinance
print(f"\n2. Versão do yfinance: {yf.__version__}")

# Teste 3: Tentar com diferentes períodos
print("\n3. Testando AAPL com diferentes períodos...")
for period in ['1d', '5d', '1mo']:
    try:
        print(f"   Período {period}...", end=" ")
        aapl = yf.download('AAPL', period=period, progress=False)
        if len(aapl) > 0:
            print(f"✅ OK! {len(aapl)} registros")
        else:
            print("❌ Sem dados")
    except Exception as e:
        print(f"❌ Erro: {str(e)[:50]}")

# Teste 4: Tentar com proxy (se necessário)
print("\n4. Tentando com User-Agent personalizado...")
try:
    import yfinance as yf
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    yf.set_tz_cache_location('./cache')
    aapl = yf.download('AAPL', period='5d', progress=False, session=session)
    if len(aapl) > 0:
        print(f"   ✅ Sucesso! {len(aapl)} registros")
        print(aapl.tail())
    else:
        print("   ❌ Sem dados")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "=" * 50)