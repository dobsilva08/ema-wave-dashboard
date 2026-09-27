import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf


st.set_page_config(page_title="EMA Wave | Monitor", page_icon="📈", layout="wide")
st.title("Monitor EMA Wave")
st.caption("Acompanhamento de ações e ETFs em 1D, 1S e 1M")

DEFAULT_TICKERS = "AAPL, MSFT, SPY, QQQ, PETR4.SA, VALE3.SA, BOVA11.SA, IVVB11.SA"


@st.cache_data(ttl=1800, show_spinner=False)
def get_daily_data(ticker: str) -> pd.DataFrame:
    data = yf.download(
        ticker,
        period="max",
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    if data is None or data.empty:
        return pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data = data.rename(columns=str.title)
    needed = ["Open", "High", "Low", "Close"]
    if not set(needed).issubset(data.columns):
        return pd.DataFrame()
    data = data[needed].dropna()
    data.index = pd.to_datetime(data.index).tz_localize(None)
    return data


def resample_ohlc(data: pd.DataFrame, rule: str) -> pd.DataFrame:
    return data.resample(rule).agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last"}
    ).dropna()


def wave_frame(data: pd.DataFrame, period: int) -> pd.DataFrame:
    out = data.copy()
    out["Wave High"] = out["High"].ewm(span=period, adjust=False).mean()
    out["Wave Mid"] = out["Close"].ewm(span=period, adjust=False).mean()
    out["Wave Low"] = out["Low"].ewm(span=period, adjust=False).mean()
    return out


def trend_state(frame: pd.DataFrame, lookback: int, threshold_pct: float) -> tuple[str, float]:
    if len(frame) <= lookback:
        return "Dados insuficientes", float("nan")
    now = frame["Wave Mid"].iloc[-1]
    then = frame["Wave Mid"].iloc[-1 - lookback]
    slope = (now / then - 1) * 100 / lookback if then else 0.0
    if slope >= threshold_pct:
        return "Alta forte", slope
    if slope <= -threshold_pct:
        return "Baixa forte", slope
    if slope > 0:
        return "Alta fraca", slope
    if slope < 0:
        return "Baixa fraca", slope
    return "Lateral", slope


def near_wave(close: float, low: float, high: float, tolerance_pct: float) -> bool:
    distance = max(low - close, 0, close - high)
    return distance / close * 100 <= tolerance_pct if close else False


def analyze(ticker: str, daily: pd.DataFrame, threshold: float, tolerance: float):
    daily_w = wave_frame(daily, 34)
    weekly_w = wave_frame(resample_ohlc(daily, "W-FRI"), 34)
    monthly_w = wave_frame(resample_ohlc(daily, "ME"), 34)
    states = {
        "1D": trend_state(daily_w, 5, threshold),
        "1S": trend_state(weekly_w, 3, threshold),
        "1M": trend_state(monthly_w, 2, threshold),
    }
    monthly, weekly = states["1M"][0], states["1S"][0]
    aligned_up = monthly == weekly == "Alta forte"
    aligned_down = monthly == weekly == "Baixa forte"
    d = daily_w.iloc[-1]
    is_near = near_wave(float(d["Close"]), float(d["Wave Low"]), float(d["Wave High"]), tolerance)
    if aligned_up and is_near:
        setup = "Pullback diário na onda (alta alinhada)"
    elif aligned_down and is_near:
        setup = "Pullback diário na onda (baixa alinhada)"
    elif aligned_up or aligned_down:
        setup = "Tendência 1M/1S alinhada; aguardar recuo"
    else:
        setup = "Sem alinhamento forte 1M/1S"
    return {
        "Ativo": ticker,
        "Fechamento": float(d["Close"]),
        "1D": states["1D"][0],
        "Inclinação 1D %/candle": states["1D"][1],
        "1S": weekly,
        "Inclinação 1S %/candle": states["1S"][1],
        "1M": monthly,
        "Inclinação 1M %/candle": states["1M"][1],
        "Perto da onda 1D": is_near,
        "Leitura": setup,
        "Atualizado até": daily_w.index[-1].date().isoformat(),
        "Diário": daily_w,
        "Semanal": weekly_w,
        "Mensal": monthly_w,
    }


with st.sidebar:
    st.header("Configuração")
    ticker_text = st.text_area(
        "Tickers separados por vírgula",
        value=DEFAULT_TICKERS,
        height=110,
        help="Exemplos: AAPL, SPY, PETR4.SA, BOVA11.SA. A lista pode ser editada.",
    )
    slope_threshold = st.number_input(
        "Inclinação mínima para tendência forte (% por candle)",
        min_value=0.01,
        max_value=2.0,
        value=0.10,
        step=0.01,
        format="%.2f",
    )
    pullback_tolerance = st.number_input(
        "Distância máxima da onda diária (%)",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        format="%.1f",
    )
    if st.button("Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("Dados diários; atualização automática do cache a cada 30 min.")

tickers = list(dict.fromkeys(t.strip().upper() for t in ticker_text.split(",") if t.strip()))
if not tickers:
    st.info("Adicione tickers na barra lateral para começar.")
    st.stop()

rows = []
frames = {}
failures = []
with st.spinner("Buscando cotações e calculando as ondas..."):
    for ticker in tickers:
        try:
            daily = get_daily_data(ticker)
            if daily.empty:
                failures.append(ticker)
                continue
            result = analyze(ticker, daily, slope_threshold, pullback_tolerance)
            rows.append({k: v for k, v in result.items() if k not in {"Diário", "Semanal", "Mensal"}})
            frames[ticker] = {
                "Diário": result["Diário"],
                "Semanal": result["Semanal"],
                "Mensal": result["Mensal"],
            }
        except Exception:
            failures.append(ticker)

if failures:
    st.warning("Não foi possível obter dados para: " + ", ".join(failures))
if not rows:
    st.error("Nenhuma série válida foi recebida. Confira os tickers e tente novamente.")
    st.stop()

table = pd.DataFrame(rows)
st.subheader("Visão geral")
st.dataframe(
    table.drop(columns=["Inclinação 1D %/candle", "Inclinação 1S %/candle", "Inclinação 1M %/candle"]),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Fechamento": st.column_config.NumberColumn(format="%.2f"),
        "Perto da onda 1D": st.column_config.CheckboxColumn(),
    },
)

st.subheader("Gráficos para acompanhamento")
selected = st.selectbox("Ativo", list(frames))

def render_wave_chart(label: str, frame: pd.DataFrame, ticker: str, candles: int) -> None:
    st.markdown(f"#### {label}")
    chart = frame.tail(candles)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=chart.index,
        open=chart["Open"],
        high=chart["High"],
        low=chart["Low"],
        close=chart["Close"],
        name=ticker,
    ))
    fig.add_trace(go.Scatter(
        x=chart.index,
        y=chart["Wave High"],
        name="EMA 34 máxima",
        line={"color": "#4c78a8", "width": 1},
    ))
    fig.add_trace(go.Scatter(
        x=chart.index,
        y=chart["Wave Low"],
        name="EMA 34 mínima",
        line={"color": "#4c78a8", "width": 1},
        fill="tonexty",
        fillcolor="rgba(76,120,168,0.12)",
    ))
    fig.add_trace(go.Scatter(
        x=chart.index,
        y=chart["Wave Mid"],
        name="EMA 34 fechamento",
        line={"color": "#f58518", "width": 1.5},
    ))
    fig.update_layout(
        height=480,
        xaxis_rangeslider_visible=False,
        margin={"l": 10, "r": 10, "t": 25, "b": 10},
        legend_orientation="h",
    )
    st.plotly_chart(fig, use_container_width=True)


selected_frames = frames[selected]
render_wave_chart("1D · Diário", selected_frames["Diário"], selected, 250)
render_wave_chart("1S · Semanal", selected_frames["Semanal"], selected, 180)
render_wave_chart("1M · Mensal", selected_frames["Mensal"], selected, 120)

with st.expander("Critérios e limitações"):
    st.markdown(
        """
        - A onda usa três EMAs de 34 candles: máxima, fechamento e mínima.
        - 1D é diário; 1S é semanal; 1M é mensal. As séries semanal e mensal são agregadas a partir dos candles diários.
        - A inclinação é a variação percentual média por candle da EMA central, observada em 5 candles diários, 3 semanais e 2 mensais. O limite configurável classifica inclinações fortes.
        - A leitura de pullback requer 1M e 1S em tendência forte na mesma direção e fechamento diário dentro ou próximo da faixa. Ela é um alerta de monitoramento, não uma ordem nem confirmação de entrada.
        - Este protótipo usa dados fornecidos pelo Yahoo Finance via yfinance; cotações podem atrasar, faltar ou sofrer ajustes. Não é feed de execução nem recomendação de investimento.
        """
    )
st.caption("Monitoramento informativo. Valide os dados e teste as regras antes de qualquer decisão financeira.")
