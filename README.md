# Monitor EMA Wave

Painel Streamlit para acompanhar uma lista editável de ações e ETFs nos tempos 1D, 1S e 1M.

## O que o painel mostra

- A onda formada por três EMAs de 34 candles (máxima, fechamento e mínima).
- Classificação da inclinação em cada tempo gráfico.
- Alinhamento forte entre semanal e mensal.
- Proximidade do preço diário à onda como alerta de possível pullback.
- Gráfico diário com candles e faixa da onda.

## Rodar localmente

Instale as dependências de requirements.txt e execute streamlit run app.py.

## Publicar no Streamlit Community Cloud

Este repositório pode ser conectado ao Streamlit Community Cloud usando app.py como arquivo de entrada. O repositório precisa conter requirements.txt.

## Dados e critérios

O protótipo obtém candles diários pelo pacote yfinance e agrega esses dados em candles semanais e mensais. A lista inicial inclui exemplos dos EUA e do Brasil; tickers brasileiros usam o sufixo .SA. O cache é renovado a cada 30 minutos, com opção de atualização manual.

A inclinação é calculada como variação percentual média por candle da EMA central, em janelas de cinco candles diários, três semanais e dois mensais. A classificação de forte e a distância máxima até a onda são ajustáveis no painel. O alerta de pullback não verifica um candle-gatilho, stop ou alvo e não representa recomendação de investimento.

Yahoo Finance/yfinance pode apresentar atrasos, indisponibilidade ou diferenças de ajuste. Verifique a qualidade e a permissão de uso dos dados antes de publicar ou usar operacionalmente.
