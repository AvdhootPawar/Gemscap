Here is a **short, clean, and precise `README.md`** with proper `#` headings, ready to **copy-paste directly**:

---

#  Real-Time Quant Analytics Dashboard

##  Overview

A real-time analytics dashboard for quantitative traders. The system streams live **Binance Futures** tick data via WebSockets, resamples it into multiple timeframes, and computes key **statistical arbitrage metrics** for monitoring market dynamics.

---

##  Architecture

<img width="1514" height="85" alt="image" src="https://github.com/user-attachments/assets/b45304a4-2a6b-4764-9696-5e920225de6e" />


### Data Ingestion

* Multi-threaded Binance WebSocket connection
* Non-blocking tick buffer using `deque`
* Captures timestamp, symbol, price, and quantity

### Data Storage

* Centralized in-memory `TickStore`
* Supports resampling to **1s / 1m / 5m** intervals

### Analytics

* **Hedge Ratio**: OLS regression
* **Spread & Z-Score**: Mean-reversion detection
* **ADF Test**: Spread stationarity check
* **Rolling Correlation**: Dynamic asset relationship tracking

---

##  Features

* Real-time interactive charts (Plotly)
* Customizable symbols, timeframes, and rolling windows
* Live Z-score alerts (e.g. |Z| > 2.0)
* One-click CSV data export

---

##  Setup

### Requirements

* Python **3.8+**

### Install Dependencies

```bash
pip install streamlit pandas numpy statsmodels plotly websocket-client
```

### Run

```bash
streamlit run your_filename.py
```

---

##  System Flow

**WebSocket → TickStore → Resampling → Quant Analytics → Streamlit UI**

(Architecture diagram available as `Architecture_Diagram.png`)

---

##  AI Usage

* **Tool**: ChatGPT/Gemini
* **Used For**:

  * Thread-safe TickStore design
  * Optimizing ADF test integration
  * Streamlit layout structuring


