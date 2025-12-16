import streamlit as st
import pandas as pd
import numpy as np
import websocket
import threading
import json
import time
from collections import deque
from statsmodels.tsa.stattools import adfuller
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# ================= CONFIG =================
SYMBOLS = ["BTCUSDT", "ETHUSDT"]

# ================= INGESTION =================
class BinanceWebSocket:
    def __init__(self, symbols):
        self.symbols = symbols
        self.buffer = deque(maxlen=10000)
        self.started = False

    def _on_message(self, ws, message):
        try:
            j = json.loads(message)
            if j.get("e") != "trade":
                return

            self.buffer.append({
                "ts": pd.to_datetime(j["T"], unit="ms"),
                "symbol": j["s"],
                "price": float(j["p"]),
                "qty": float(j["q"])
            })
        except Exception:
            pass

    def start(self):
        if self.started:
            return
        self.started = True

        for sym in self.symbols:
            url = f"wss://fstream.binance.com/ws/{sym.lower()}@trade"
            ws = websocket.WebSocketApp(url, on_message=self._on_message)
            threading.Thread(target=ws.run_forever, daemon=True).start()

# ================= STORAGE =================
class TickStore:
    def __init__(self):
        self.df = pd.DataFrame(columns=["ts", "symbol", "price", "qty"])

    def update(self, ticks):
        if ticks:
            self.df = pd.concat([self.df, pd.DataFrame(ticks)], ignore_index=True)
            self.df.drop_duplicates(inplace=True)

    def resample(self, symbol, timeframe):
        sdf = self.df[self.df["symbol"] == symbol]
        if sdf.empty:
            return sdf
        sdf = sdf.set_index("ts")
        rule = {"1s": "1S", "1m": "1T", "5m": "5T"}[timeframe]
        return sdf.resample(rule).agg({"price": "last", "qty": "sum"}).dropna()

# ================= ANALYTICS =================
def hedge_ratio(x, y):
    return np.polyfit(x, y, 1)[0]

def spread_and_zscore(x, y, window):
    beta = hedge_ratio(x, y)
    spread = y - beta * x
    z = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()
    return beta, spread, z

def rolling_correlation(x, y, window):
    return x.rolling(window).corr(y)

def adf_test(series):
    result = adfuller(series.dropna())
    return {
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Critical Values": result[4]
    }

def check_zscore_alert(z, thresh):
    if abs(z) > thresh:
        return f"ALERT: Z-score breached ({z:.2f})"
    return None

# ================= SESSION STATE =================
if "ws" not in st.session_state:
    st.session_state.ws = BinanceWebSocket(SYMBOLS)
    st.session_state.ws.start()

if "store" not in st.session_state:
    st.session_state.store = TickStore()

# ================= UI =================
st.title("Real-Time Quant Analytics Dashboard")

sym1, sym2, tf = st.columns(3)
s1 = sym1.selectbox("Symbol X", SYMBOLS, 0)
s2 = sym2.selectbox("Symbol Y", [s for s in SYMBOLS if s != s1], 0)
tf = tf.selectbox("Timeframe", ["1s", "1m", "5m"], 1)

window = st.slider("Rolling Window", 10, 100, 30)
z_thresh = st.slider("Z-Score Threshold", 1.0, 3.0, 2.0)

# ================= UPDATE DATA =================
ticks = list(st.session_state.ws.buffer)
st.session_state.ws.buffer.clear()
st.session_state.store.update(ticks)

df_x = st.session_state.store.resample(s1, tf)
df_y = st.session_state.store.resample(s2, tf)

st.caption(f"Ticks collected: {len(st.session_state.store.df)}")

if not df_x.empty and not df_y.empty:
    df = pd.concat([df_x["price"], df_y["price"]], axis=1)
    df.columns = ["x", "y"]
    df.dropna(inplace=True)

    if len(df) < max(window + 5, 50):
        st.warning("Collecting sufficient data...")
    else:
        beta, spread, z = spread_and_zscore(df["x"], df["y"], window)
        corr = rolling_correlation(df["x"], df["y"], window)

        st.subheader("Price Comparison")
        st.line_chart(df)

        st.subheader("Spread & Z-Score")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=spread, name="Spread"))
        fig.add_trace(go.Scatter(y=z, name="Z-Score"))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Rolling Correlation")
        st.line_chart(corr)

        alert = check_zscore_alert(z.iloc[-1], z_thresh)
        if alert:
            st.error(alert)

        if st.button("Run ADF Test"):
            st.json(adf_test(spread))

        st.download_button(
            "Download CSV",
            df.assign(spread=spread, zscore=z).to_csv().encode(),
            "analytics.csv"
        )
else:
    st.info("Streaming live data… analytics will appear shortly.")

st.caption("Auto-refresh every 2 seconds")
time.sleep(2)
st.rerun()

