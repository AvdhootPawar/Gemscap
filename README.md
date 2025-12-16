📈 Real-Time Quant Analytics Dashboard
📌 Project Overview
This application is a complete analytical suite designed for quantitative traders to monitor and analyze real-time market dynamics. It ingests live tick data from Binance Futures via WebSockets, processes it into selectable timeframes, and computes key statistical arbitrage metrics such as hedge ratios, spreads, and stationarity tests.



🛠️ Methodology & Architecture
The system follows a modular design to ensure high performance and future extensibility.




Data Ingestion: A multi-threaded BinanceWebSocket class manages persistent connections to Binance. It uses a deque buffer to handle high-frequency tick data (timestamp, symbol, price, qty) without blocking the main UI.


Data Handling & Storage: The TickStore class provides a centralized in-memory database that supports dynamic resampling into 1s, 1m, and 5m intervals.

Quantitative Analytics:


Hedge Ratio: Calculated using OLS regression to determine the relationship between two assets.



Spread & Z-Score: Monitors price deviations to identify mean-reversion opportunities.



ADF Test: An integrated Augmented Dickey-Fuller test to check for spread stationarity.



Rolling Correlation: Tracks how closely assets move together over a sliding window.

🚀 Setup & Execution
Prerequisites: Python 3.8 or higher.

Install Dependencies:

Bash

pip install streamlit pandas numpy statsmodels plotly websocket-client
Run the Application:

Bash

streamlit run your_filename.py

The app will automatically begin streaming live data upon startup.

📊 Key Features

Interactive Dashboards: Real-time price charts and statistical plots (Spread, Z-Score, Correlation) built with Plotly for zoom and pan support.



Customizable Controls: Adjust symbols, timeframes, and rolling windows on the fly.


Live Alerting: Visual indicators that trigger when the Z-score breaches user-defined thresholds (e.g., Z > 2.0).



Data Export: A one-click download button to export processed analytics and time-series data as a CSV for further research.


🏗️ Architecture Diagram
The project includes a detailed architecture diagram (found in the repository as Architecture_Diagram.png) illustrating the following flow:

Ingestion Layer: WebSocket Connection → Threaded Buffer.

Storage Layer: TickStore → Resampling Engine.

Analytics Layer: OLS Regression → Statistical Testing.

Presentation Layer: Streamlit UI → Interactive Charts → Alerting System.

🤖 AI Usage Transparency

Tool: [Specify AI used, e.g., ChatGPT/Gemini].



Usage: Assisted in structuring the thread-safe TickStore class, optimizing the statsmodels ADF test integration, and designing the Streamlit multi-column layout.


Prompts Used: "How to run a background websocket thread in Streamlit?", "Calculate rolling OLS hedge ratio in pandas.".
