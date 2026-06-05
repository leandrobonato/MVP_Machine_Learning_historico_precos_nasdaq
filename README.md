# \# 📊 Dashboard Financeiro - Dados Históricos de Ações NASDAQ

# 

# !\[Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

# !\[Yahoo Finance](https://img.shields.io/badge/Yahoo%20Finance-API-green.svg)

# !\[License](https://img.shields.io/badge/License-MIT-yellow.svg)

# 

# Sistema completo para download, processamento e análise de dados históricos de ações listadas na NASDAQ. O pipeline coleta cotações (OHLCV), dividendos, valor de mercado e calcula \*\*55+ indicadores técnicos\*\* avançados.

# 

# \---

# 

# \## 📁 Estrutura do Projeto

# 

# ```

# .

# ├── data/

# │   └── nasdaq-listed-symbols.csv    # Lista de símbolos NASDAQ

# │

# ├── scripts/

# │   ├── download\_cotacoes.py         # Download de cotações OHLCV

# │   ├── download\_indicadores.py      # Cálculo de indicadores técnicos

# │   └── pipeline\_completo.py         # Pipeline unificado

# │

# ├── historicos/

# │   ├── cotacoes/                    # Preços OHLCV

# │   │   └── {SIMBOLO}.csv

# │   ├── dividendos/                  # Dividendos + métricas

# │   │   └── {SIMBOLO}.csv

# │   ├── valor\_mercado/               # Market Cap histórico

# │   │   └── {SIMBOLO}.csv

# │   └── indicadores/

# │       ├── rsi/                     # RSI (7 e 14 períodos)

# │       │   └── {SIMBOLO}.csv

# │       ├── macd/                    # MACD

# │       │   └── {SIMBOLO}.csv

# │       ├── bollinger/               # Bandas de Bollinger

# │       │   └── {SIMBOLO}.csv

# │       ├── fibonacci/               # Fibonacci Retracement

# │       │   └── {SIMBOLO}.csv

# │       ├── medias\_moveis/           # Médias Móveis

# │       │   └── {SIMBOLO}.csv

# │       ├── volatilidade/            # Volatilidade e Retornos

# │       │   └── {SIMBOLO}.csv

# │       └── tendencia/               # Tendências e Sinais

# │           └── {SIMBOLO}.csv

# │

# ├── resumo\_dividendos.csv            # Consolidado de dividendos

# ├── resumo\_valor\_mercado.csv         # Consolidado de market cap

# ├── symbols\_valid.csv                # Símbolos processados

# └── README.md

# ```

# 

# \---

# 

# \## 🚀 Funcionalidades

# 

# \### 1. Download de Cotações Históricas

# \- \*\*Preços OHLCV\*\*: Open, High, Low, Close, Adj Close, Volume

# \- \*\*Período configurável\*\*: Padrão 2016 até data atual

# \- \*\*Escalabilidade\*\*: Suporte a 5.000+ símbolos NASDAQ

# \- \*\*Precisão\*\*: Preços com 2 casas decimais, Volume como inteiro

# 

# \### 2. Dividendos e Proventos

# \- Histórico completo de pagamentos de dividendos

# \- Dividend Yield, Dividend Rate, Payout Ratio

# \- Total de dividendos nos últimos 12 meses

# \- Número de pagamentos no ano

# \- Próxima data ex-dividendo

# \- Histórico de desdobramentos (Stock Splits)

# 

# \### 3. Valor de Mercado Histórico

# \- \*\*Market Cap\*\* = Close × Shares Outstanding (diário)

# \- Ajuste automático para splits históricos

# \- Volume financeiro negociado (Volume × Close)

# \- Market Cap em bilhões para facilitar leitura

# \- Variação percentual diária

# 

# \### 4. Indicadores Técnicos (55+ indicadores)

# 

# \#### 📈 Médias Móveis (`indicadores/medias\_moveis/`)

# | Indicador | Período | Uso Principal |

# |-----------|---------|---------------|

# | MA\_7 | 7 dias | Tendência de curtíssimo prazo |

# | MA\_14 | 14 dias | Tendência de curto prazo |

# | MA\_30 | 30 dias | Suporte/Resistência mensal |

# | MA\_50 | 50 dias | Tendência de médio prazo |

# | MA\_200 | 200 dias | Tendência de longo prazo |

# | Sinal\_MA\_7\_14 | - | 1 = Cruzamento de alta, -1 = Cruzamento de baixa |

# | Sinal\_MA\_50\_200 | - | 1 = Golden Cross, -1 = Death Cross |

# 

# \#### 📉 RSI - Índice de Força Relativa (`indicadores/rsi/`)

# | Indicador | Período | Uso Principal |

# |-----------|---------|---------------|

# | RSI\_7 | 7 períodos | Sinal rápido, mais sensível a mudanças |

# | RSI\_14 | 14 períodos | Padrão do mercado |

# | RSI\_Sinal | - | Acima de 70 = Sobrecomprado (vender) |

# | | | Abaixo de 30 = Sobrevendido (comprar) |

# | | | Entre 30-70 = Neutro |

# 

# \#### 📊 MACD (`indicadores/macd/`)

# | Indicador | Descrição | Uso Principal |

# |-----------|-----------|---------------|

# | MACD\_Line | Diferença entre EMA 12 e EMA 26 | Linha principal do indicador |

# | MACD\_Signal | EMA 9 do MACD | Linha de sinal |

# | MACD\_Histogram | MACD\_Line - MACD\_Signal | Positivo = momentum cresce |

# | | | Negativo = momentum diminui |

# | MACD\_Sinal | - | Compra = MACD cruza acima do Sinal |

# | | | Venda = MACD cruza abaixo do Sinal |

# 

# \#### 🎯 Bandas de Bollinger (`indicadores/bollinger/`)

# | Indicador | Descrição | Uso Principal |

# |-----------|-----------|---------------|

# | BB\_Upper | Média + 2 desvios padrão | Resistência dinâmica |

# | BB\_Middle | Média Móvel de 20 dias | Linha central |

# | BB\_Lower | Média - 2 desvios padrão | Suporte dinâmico |

# | BB\_Width | Largura das bandas (%) | Baixo = consolidação |

# | | | Alto = volatilidade elevada |

# | BB\_Position | 0 a 1 | 0 = Banda inferior, 1 = Banda superior |

# | BB\_Sinal | - | Preço na Upper = Sobrecomprado |

# | | | Preço na Lower = Sobrevendido |

# 

# \#### 🔢 Fibonacci Retracement (`indicadores/fibonacci/`)

# | Indicador | Nível | Uso Principal |

# |-----------|-------|---------------|

# | Fib\_0 | 0% | Suporte (fundo da tendência) |

# | Fib\_236 | 23.6% | Retração fraca |

# | Fib\_382 | 38.2% | Suporte/Resistência moderada |

# | Fib\_50 | 50% | Ponto de equilíbrio |

# | Fib\_618 | 61.8% | \*\*Golden Ratio\*\* - Forte suporte/resistência |

# | Fib\_786 | 78.6% | Retração profunda |

# | Fib\_1 | 100% | Resistência (topo da tendência) |

# | Fib\_1\_272 | 127.2% | Projeção de extensão |

# | Fib\_1\_618 | 161.8% | \*\*Golden Ratio\*\* - Alvo de projeção |

# | Fib\_Position | 0-2 | 0 = Fundo, 1 = Topo, >1 = Rompimento |

# | Fib\_Zone | Texto | Suporte Forte / Suporte / Consolidação / Resistência / Resistência Forte / Rompimento |

# | Fib\_Buy\_Signal | 0/1 | Preço tocou suporte (38.2% ou 61.8%) |

# | Fib\_Sell\_Signal | 0/1 | Preço tocou resistência (78.6% ou 100%) |

# | Fib\_Confluencia | 0-6 | Quantos níveis convergem (≥2 = Forte, ≥4 = Muito Forte) |

# 

# \#### 📊 Volatilidade e Retornos (`indicadores/volatilidade/`)

# | Indicador | Descrição | Uso Principal |

# |-----------|-----------|---------------|

# | Returns | Retorno diário (%) | Variação percentual do dia |

# | Returns\_Log | Retorno logarítmico | Para cálculos estatísticos |

# | Volatilidade\_20 | Volatilidade anualizada (20d) | Alta = risco elevado |

# | Range\_Diario | High - Low | Amplitude do movimento |

# | Range\_Percentual | Range / Close × 100 | Volatilidade intradiária (%) |

# | Gap | Open - Close anterior | Força da abertura |

# | Gap\_Percentual | Gap / Close anterior × 100 | Positivo = força compradora |

# | Volume\_Medio\_20 | Média de volume 20 dias | Linha base de volume |

# | Volume\_Ratio | Volume / Volume\_Medio\_20 | >1.5 = volume anormal |

# 

# \#### 🔍 Tendências e Sinais (`indicadores/tendencia/`)

# | Indicador | Descrição | Uso Principal |

# |-----------|-----------|---------------|

# | Tendencia\_7d | Alta/Baixa | Close vs MA7 |

# | Tendencia\_50d | Alta/Baixa | Close vs MA50 |

# | Forca\_Tendencia | Inclinação da MA50 em 5 dias (%) | Positivo = acelerando alta |

# | Forca\_Movimento | (Close-Open)/(High-Low) | 1 = Fechou na máxima |

# | | | -1 = Fechou na mínima |

# | Velas\_Alta\_Consecutivas | Contagem | ≥3 = tendência consolidada |

# 

# \---

# 

# \## 📊 Dicionário de Dados Completo

# 

# \### Cotações (`historicos/cotacoes/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão (YYYY-MM-DD) |

# | 2 | Open | Decimal(2) | 185.50 | Preço de abertura do dia |

# | 3 | High | Decimal(2) | 188.75 | Preço máximo do dia |

# | 4 | Low | Decimal(2) | 184.20 | Preço mínimo do dia |

# | 5 | Close | Decimal(2) | 187.30 | Preço de fechamento do dia |

# | 6 | Adj Close | Decimal(2) | 187.30 | Preço ajustado (splits/dividendos) |

# | 7 | Volume | Inteiro | 52456700 | Quantidade de ações negociadas |

# 

# \### Dividendos (`historicos/dividendos/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-03-15 | Data do pagamento/evento |

# | 2 | Dividends | Decimal(4) | 0.2500 | Valor do dividendo pago por ação |

# | 3 | Stock\_Splits | Decimal(4) | 2.0000 | Ratio (2.0 = split 2:1) |

# | 4 | Dividend\_Yield | Decimal(2) | 2.50 | Rendimento anual de dividendos (%) |

# | 5 | Dividend\_Rate | Decimal(2) | 1.00 | Valor anual estimado por ação ($) |

# | 6 | Payout\_Ratio | Decimal(2) | 35.00 | % do lucro distribuído como dividendos |

# | 7 | Dividend\_1Y\_Total | Decimal(4) | 1.0000 | Total de dividendos nos últimos 12 meses |

# | 8 | Dividend\_1Y\_Count | Inteiro | 4 | Número de pagamentos no último ano |

# | 9 | Last\_Dividend | Decimal(4) | 0.2500 | Valor do último dividendo pago |

# | 10 | Ex\_Dividend\_Date | Data | 2024-06-15 | Próxima data ex-dividendo |

# 

# \### Valor de Mercado (`historicos/valor\_mercado/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | Close | Decimal(2) | 187.30 | Preço de fechamento |

# | 3 | Shares\_Outstanding | Inteiro | 15500000000 | Ações em circulação |

# | 4 | Market\_Cap | Decimal(2) | 2903150000000 | Valor de mercado ($) |

# | 5 | Market\_Cap\_B | Decimal(2) | 2903.15 | Market Cap em bilhões ($B) |

# | 6 | Market\_Cap\_Change\_Pct | Decimal(2) | 1.25 | Variação percentual diária (%) |

# | 7 | Volume\_Dollar | Decimal(2) | 9825345100 | Volume financeiro negociado ($) |

# 

# \### Indicadores - RSI (`historicos/indicadores/rsi/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | RSI\_7 | Decimal(2) | 65.32 | RSI de 7 períodos |

# | 3 | RSI\_14 | Decimal(2) | 58.45 | RSI de 14 períodos (padrão) |

# | 4 | RSI\_Sinal | Texto | Neutro | Sobrecomprado/Sobrevendido/Neutro |

# 

# \### Indicadores - MACD (`historicos/indicadores/macd/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | MACD\_Line | Decimal(2) | 2.45 | Linha MACD (EMA12 - EMA26) |

# | 3 | MACD\_Signal | Decimal(2) | 1.80 | Linha de Sinal (EMA9 do MACD) |

# | 4 | MACD\_Histogram | Decimal(2) | 0.65 | Histograma (MACD - Sinal) |

# | 5 | MACD\_Sinal | Texto | Compra | Compra/Neutro/Venda |

# 

# \### Indicadores - Bollinger (`historicos/indicadores/bollinger/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | BB\_Upper | Decimal(2) | 195.30 | Banda Superior (+2 desvios) |

# | 3 | BB\_Middle | Decimal(2) | 185.00 | Média Móvel 20 dias |

# | 4 | BB\_Lower | Decimal(2) | 174.70 | Banda Inferior (-2 desvios) |

# | 5 | BB\_Width | Decimal(2) | 11.14 | Largura das bandas (%) |

# | 6 | BB\_Position | Decimal(2) | 0.65 | Posição (0=Lower, 1=Upper) |

# | 7 | BB\_Sinal | Texto | Neutro | Sobrecomprado/Sobrevendido/Neutro |

# 

# \### Indicadores - Fibonacci (`historicos/indicadores/fibonacci/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | Fib\_0 | Decimal(2) | 150.00 | Nível 0% (fundo) |

# | 3 | Fib\_236 | Decimal(2) | 158.50 | Nível 23.6% |

# | 4 | Fib\_382 | Decimal(2) | 163.80 | Nível 38.2% |

# | 5 | Fib\_50 | Decimal(2) | 167.50 | Nível 50% |

# | 6 | Fib\_618 | Decimal(2) | 171.20 | Nível 61.8% (Golden Ratio) |

# | 7 | Fib\_786 | Decimal(2) | 175.80 | Nível 78.6% |

# | 8 | Fib\_1 | Decimal(2) | 185.00 | Nível 100% (topo) |

# | 9 | Fib\_1\_272 | Decimal(2) | 193.20 | Extensão 127.2% |

# | 10 | Fib\_1\_618 | Decimal(2) | 203.50 | Extensão 161.8% (Golden Ratio) |

# | 11 | Fib\_Position | Decimal(2) | 0.65 | Posição relativa (0-2) |

# | 12 | Fib\_Level\_Current | Texto | 0.62 | Nível Fibonacci atual |

# | 13 | Fib\_Distance\_Next | Decimal(2) | 0.15 | Distância para próximo nível |

# | 14 | Fib\_Zone | Texto | Resistência | Zona de atuação do preço |

# | 15 | Fib\_Buy\_Signal | Inteiro | 0 | 1 = Sinal de compra |

# | 16 | Fib\_Sell\_Signal | Inteiro | 0 | 1 = Sinal de venda |

# 

# \### Indicadores - Médias Móveis (`historicos/indicadores/medias\_moveis/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | MA\_7 | Decimal(2) | 186.50 | Média Móvel 7 dias |

# | 3 | MA\_14 | Decimal(2) | 184.30 | Média Móvel 14 dias |

# | 4 | MA\_30 | Decimal(2) | 181.20 | Média Móvel 30 dias |

# | 5 | MA\_50 | Decimal(2) | 178.50 | Média Móvel 50 dias |

# | 6 | MA\_200 | Decimal(2) | 165.80 | Média Móvel 200 dias |

# | 7 | Sinal\_MA\_7\_14 | Inteiro | 1 | 1=MA7>MA14 (alta), -1=MA7<MA14 |

# | 8 | Sinal\_MA\_50\_200 | Inteiro | 1 | 1=Golden Cross, -1=Death Cross |

# 

# \### Indicadores - Volatilidade (`historicos/indicadores/volatilidade/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | Returns | Decimal(4) | 0.0125 | Retorno diário (1.25%) |

# | 3 | Returns\_Log | Decimal(4) | 0.0124 | Retorno logarítmico |

# | 4 | Volatilidade\_20 | Decimal(2) | 25.30 | Volatilidade anualizada (%) |

# | 5 | Range\_Diario | Decimal(2) | 4.55 | Amplitude (High - Low) |

# | 6 | Range\_Percentual | Decimal(2) | 2.43 | Amplitude percentual (%) |

# | 7 | Gap | Decimal(2) | 1.20 | Gap de abertura ($) |

# | 8 | Gap\_Percentual | Decimal(2) | 0.64 | Gap percentual (%) |

# | 9 | Volume\_Medio\_20 | Inteiro | 48500000 | Volume médio 20 dias |

# | 10 | Volume\_Ratio | Decimal(2) | 1.08 | Volume / Média (1.08 = 8% acima) |

# 

# \### Indicadores - Tendência (`historicos/indicadores/tendencia/{SIMBOLO}.csv`)

# | # | Campo | Tipo | Exemplo | Descrição |

# |---|-------|------|---------|-----------|

# | 1 | Date | Data | 2024-01-15 | Data do pregão |

# | 2 | Tendencia\_7d | Texto | Alta | Direção curto prazo |

# | 3 | Tendencia\_50d | Texto | Alta | Direção médio prazo |

# | 4 | Forca\_Tendencia | Decimal(2) | 2.35 | Inclinação MA50 em 5 dias (%) |

# | 5 | Forca\_Movimento | Decimal(2) | 0.75 | 1=Fechou na máxima, -1=Fechou na mínima |

# | 6 | Velas\_Alta\_Consecutivas | Inteiro | 3 | Dias consecutivos de alta |

# 

# \---

# 

# \## 📈 Exemplos de Uso

# 

# \### Análise de Sinais de Compra/Venda

# ```python

# import pandas as pd

# 

# \# Carregar indicadores

# rsi = pd.read\_csv('historicos/indicadores/rsi/AAPL.csv')

# macd = pd.read\_csv('historicos/indicadores/macd/AAPL.csv')

# fib = pd.read\_csv('historicos/indicadores/fibonacci/AAPL.csv')

# 

# \# Verificar múltiplos sinais alinhados

# sinais\_compra = (

# &#x20;   (rsi\['RSI\_Sinal'].iloc\[-1] == 'Sobrevendido') \&

# &#x20;   (macd\['MACD\_Sinal'].iloc\[-1] == 'Compra') \&

# &#x20;   (fib\['Fib\_Buy\_Signal'].iloc\[-1] == 1)

# )

# 

# if sinais\_compra:

# &#x20;   print("✅ Múltiplos sinais de COMPRA alinhados!")

# ```

# 

# \### Identificar Ações com Golden Cross Recente

# ```python

# import os

# 

# golden\_cross\_stocks = \[]

# for arquivo in os.listdir('historicos/indicadores/medias\_moveis/'):

# &#x20;   df = pd.read\_csv(f'historicos/indicadores/medias\_moveis/{arquivo}')

# &#x20;   if df\['Sinal\_MA\_50\_200'].iloc\[-1] == 1 and df\['Sinal\_MA\_50\_200'].iloc\[-2] == -1:

# &#x20;       golden\_cross\_stocks.append(arquivo.replace('.csv', ''))

# 

# print(f"Ações com Golden Cross recente: {golden\_cross\_stocks}")

# ```

# 

# \---

# 

# \## 🛠️ Tecnologias Utilizadas

# 

# \- \*\*Python 3.8+\*\* - Linguagem principal

# \- \*\*yfinance\*\* - API do Yahoo Finance

# \- \*\*pandas\*\* - Manipulação de dados

# \- \*\*numpy\*\* - Cálculos numéricos

# \- \*\*Google Colab\*\* - Execução em nuvem (opcional)

# 

# \---

# 

# \## ⚠️ Limitações

# 

# \- \*\*Rate Limit\*\*: Yahoo Finance limita requisições frequentes (\~10/min)

# \- \*\*Dados Gratuitos\*\*: API gratuita tem limitações de acesso

# \- \*\*Ações Delistadas\*\*: Símbolos antigos podem não ter dados disponíveis

# \- \*\*Market Cap\*\*: Usa shares outstanding atual ajustado por splits históricos

# 

# \---

# 

# \## 📝 Licença

# 

# Este projeto está sob a licença MIT.

# 

# \---

# 

# \*\*⭐ Se este projeto foi útil, considere dar uma estrela no repositório!\*\*

