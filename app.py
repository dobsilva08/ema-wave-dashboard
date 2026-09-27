import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf


st.set_page_config(page_title="EMA Wave | Monitor", page_icon="📈", layout="wide")
st.title("Monitor EMA Wave")
st.caption("Acompanhamento de ações e ETFs em 1D, 1S e 1M")

DEFAULT_TICKERS = "AAPL, MSFT, SPY, QQQ, PETR4.SA, VALE3.SA, BOVA11.SA, IVVB11.SA"

# Tickers da tabela de ETFs da Renova Invest; disponíveis para seleção.
B3_ETF_TICKERS = [
    "CHIP11.SA",
    "ARGE11.SA",
    "HTEK11.SA",
    "QQQQ11.SA",
    "UTEC11.SA",
    "USTK11.SA",
    "CMDB11.SA",
    "ELAS11.SA",
    "PIBB11.SA",
    "SPXR11.SA",
    "BBOI11.SA",
    "BBOV11.SA",
    "BOVV11.SA",
    "BOVA11.SA",
    "BOVX11.SA",
    "BOVB11.SA",
    "IBOB11.SA",
    "BRAX11.SA",
    "BOVS11.SA",
    "XBOV11.SA",
    "GOVE11.SA",
    "AUVP11.SA",
    "LVOL11.SA",
    "FIND11.SA",
    "DIVO11.SA",
    "UTLL11.SA",
    "MATB11.SA",
    "NASD11.SA",
    "BMMT11.SA",
    "NSDV11.SA",
    "TECK11.SA",
    "ECOO11.SA",
    "SVAL11.SA",
    "BXPO11.SA",
    "MILL11.SA",
    "REVE11.SA",
    "VWRA11.SA",
    "BDEF11.SA",
    "SPXB11.SA",
    "ACWI11.SA",
    "WRLD11.SA",
    "GPUS11.SA",
    "SPXI11.SA",
    "IVVB11.SA",
    "GOAT11.SA",
    "ISUS11.SA",
    "BRXC11.SA",
    "DVER11.SA",
    "BBSD11.SA",
    "BEST11.SA",
    "BREW11.SA",
    "BDOM11.SA",
    "BCIC11.SA",
    "GLDX11.SA",
    "NDIV11.SA",
    "GOLD11.SA",
    "ESGB11.SA",
    "CORN11.SA",
    "XFIX11.SA",
    "DOLA11.SA",
    "DOLB11.SA",
    "TECX11.SA",
    "GENB11.SA",
    "TRIG11.SA",
    "SMAL11.SA",
    "SMAC11.SA",
    "SMAB11.SA",
    "FIXX11.SA",
    "HERT11.SA",
    "QQQI11.SA",
    "SPYI11.SA",
    "ALUG11.SA",
    "IWMI11.SA",
    "PKIN11.SA",
    "GBTC11.SA",
    "RICO11.SA",
    "AGRI11.SA",
    "USDB11.SA",
    "BNDX11.SA",
    "SCVB11.SA",
    "AURO11.SA",
    "HIGH11.SA",
    "CASA11.SA",
    "XINA11.SA",
    "JOGO11.SA",
    "NUCL11.SA",
    "BITC11.SA",
    "HODL11.SA",
    "QBTC11.SA",
    "BITH11.SA",
    "BITI11.SA",
    "NBIT11.SA",
    "DEFI11.SA",
    "HASH11.SA",
    "QDFI11.SA",
    "ETHE11.SA",
    "FOMO11.SA",
    "QETH11.SA",
    "EETH11.SA",
    "CRPT11.SA",
    "SOLH11.SA",
    "COIN11.SA",
    "QSOL11.SA",
    "XRPH11.SA",
    "WEB311.SA",
    "META11.SA",
    "5PRE11.SA",
    "AREA11.SA",
    "B5P211.SA",
    "BLFT11.SA",
    "BOL511.SA",
    "BPRE11.SA",
    "BTER11.SA",
    "CLOB11.SA",
    "DEBB11.SA",
    "DOLX11.SA",
    "ETHY11.SA",
    "FIXA11.SA",
    "GBIT11.SA",
    "GDIV11.SA",
    "GICP11.SA",
    "GLDI11.SA",
    "GLFT11.SA",
    "GOLB11.SA",
    "GPCA11.SA",
    "GXUS11.SA",
    "HYBR11.SA",
    "IB5M11.SA",
    "IDKA11.SA",
    "IMAB11.SA",
    "IRFM11.SA",
    "IVWO11.SA",
    "LFIN11.SA",
    "LFIX11.SA",
    "LFTB11.SA",
    "LFTS11.SA",
    "LIQB11.SA",
    "LLFT11.SA",
    "LTBX11.SA",
    "LTNB11.SA",
    "MARG11.SA",
    "NTNS11.SA",
    "OURO11.SA",
    "PACB11.SA",
    "PACC11.SA",
    "PIPE11.SA",
    "POSB11.SA",
    "QLBR11.SA",
    "RARA11.SA",
    "SLVR11.SA",
    "SPBZ11.SA",
    "T10R11.SA",
]

# Tickers da lista de ETFs americanos do Investidor10.
US_ETF_TICKERS = [
    "IVV",
    "VOO",
    "JEPI",
    "JEPQ",
    "QQQ",
    "SCHD",
    "TFLO",
    "SPY",
    "VT",
    "SGOV",
    "VNQ",
    "SPHD",
    "IXUS",
    "VXUS",
    "QQQM",
    "VTI",
    "SMH",
    "DHS",
    "IAU",
    "SOXX",
    "QQQI",
    "SHY",
    "SPYI",
    "VGT",
    "VEA",
    "VTV",
    "TLT",
    "VWO",
    "QTUM",
    "IBIT",
    "GLD",
    "DIVO",
    "SPMO",
    "BIL",
    "QYLD",
    "SLVO",
    "SCHH",
    "AIQ",
    "BND",
    "XLE",
    "GLDM",
    "AVUV",
    "VGK",
    "VIG",
    "USOI",
    "IEMG",
    "SLV",
    "VYM",
    "CIBR",
    "VUG",
    "AVDV",
    "COPX",
    "XBCI",
    "GLDI",
    "VYMI",
    "EWZ",
    "NVDY",
    "MSTY",
    "URA",
    "XLK",
    "SHV",
    "FEZ",
    "AGG",
    "BWET",
    "MRNY",
    "REMX",
    "SCHG",
    "DRAM",
    "GRID",
    "VCLT",
    "MCHI",
    "SDIV",
    "TSLY",
    "AMDY",
    "DGRO",
    "EWY",
    "SPYM",
    "NOBL",
    "CHPY",
    "ULTY",
    "BNDX",
    "XLV",
    "SPHQ",
    "PLTY",
    "SOXL",
    "IXC",
    "IJR",
    "GDX",
    "USHY",
    "BTCI",
    "DRAL",
    "IEFA",
    "ACWI",
    "IYW",
    "IAUM",
    "CONY",
    "YMAX",
    "AMDW",
    "HOOY",
    "WNTR",
    "XLU",
    "MAGS",
    "DTCR",
    "DIV",
    "GDXY",
    "BITA",
    "FLSW",
    "SCHX",
    "QUAL",
    "USMV",
    "HDV",
    "ITA",
    "IEUR",
    "VNQI",
    "IWMI",
    "AOK",
    "QQQY",
    "IWMW",
    "FIAT",
    "SCHF",
    "XLF",
    "SCHB",
    "TQQQ",
    "VDE",
    "IBB",
    "BOTZ",
    "CHAT",
    "HYGH",
    "VO",
    "JPST",
    "GOVT",
    "XLI",
    "LQD",
    "SCHA",
    "VHT",
    "XLP",
    "IDV",
    "XLRE",
    "ARTY",
    "SCHY",
    "DGS",
    "AVES",
    "XQQI",
    "XDTE",
    "XLEI",
    "MST",
    "COYY",
    "IWF",
    "IWD",
    "IWM",
    "VBR",
    "VOOG",
    "EWJ",
    "DVY",
    "VTIP",
    "DGRW",
    "BOXX",
    "PAVE",
    "UPRO",
    "PFFD",
    "ROBO",
    "QDTE",
    "IGLD",
    "SVOL",
    "TSPY",
    "LQDW",
    "XPAY",
    "IEUS",
    "YBTC",
    "NVII",
    "XSPI",
    "HYGW",
    "EXUS",
    "USOY",
    "SOXY",
    "AMYY",
    "RSP",
    "VCIT",
    "EEM",
    "EFV",
    "FTEC",
    "EMB",
    "XBI",
    "SIL",
    "EWU",
    "XYLD",
    "SOXQ",
    "HACK",
    "IGPT",
    "RYLD",
    "JPRE",
    "EEMS",
    "KBWD",
    "YMAG",
    "GPTY",
    "SNOY",
    "ARMW",
    "OARK",
    "YSPC",
    "IVW",
    "VEU",
    "DIA",
    "JAAA",
    "MTUM",
    "IGSB",
    "PFF",
    "IXN",
    "VIGI",
    "VPL",
    "SPYD",
    "INDA",
    "GPIQ",
    "GPIX",
    "MUU",
    "AOA",
    "PSI",
    "ICLN",
    "ARKQ",
    "AVIV",
    "DBC",
    "BITO",
    "LIT",
    "AIPO",
    "MULL",
    "BNO",
    "WSML",
    "IBTM",
    "AIPI",
    "IGBH",
    "SPYT",
    "HOOW",
    "TSMY",
    "YBIT",
    "EART",
    "INYY",
    "QDTY",
    "NVYY",
    "CVNY",
]

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
    selected_etfs = st.multiselect(
        "Adicionar ETFs da B3",
        options=B3_ETF_TICKERS,
        format_func=lambda ticker: ticker.removesuffix(".SA"),
        help="Escolha os ETFs que deseja acompanhar. Os dados serão buscados ao selecioná-los.",
    )
    st.caption(
        f"{len(B3_ETF_TICKERS)} ETFs disponíveis · "
        "[fonte: Renova Invest](https://renovainvest.com.br/etfs/)"
    )
    selected_us_etfs = st.multiselect(
        "Adicionar ETFs americanos",
        options=US_ETF_TICKERS,
        help="Lista do Investidor10. Selecione apenas os ETFs que deseja acompanhar.",
    )
    st.caption(
        f"{len(US_ETF_TICKERS)} ETFs disponíveis · "
        "[fonte: Investidor10](https://investidor10.com.br/etfs-global/)"
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

tickers = list(dict.fromkeys(
    [t.strip().upper() for t in ticker_text.split(",") if t.strip()]
    + selected_etfs
    + selected_us_etfs
))
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
graph_tickers = list(frames)
preferred_ticker = (
    selected_us_etfs[-1]
    if selected_us_etfs
    else selected_etfs[-1] if selected_etfs else None
)
if preferred_ticker in graph_tickers:
    graph_tickers.remove(preferred_ticker)
    graph_tickers.insert(0, preferred_ticker)
selected = st.selectbox(
    "Ativo nos três gráficos",
    graph_tickers,
    help="Os ativos selecionados e com cotações disponíveis aparecem nesta lista.",
)
st.caption(f"{len(graph_tickers)} ativos com dados disponíveis para os gráficos.")

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
