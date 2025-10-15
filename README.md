﻿\# 💼 Investment Portfolio Performance Tracker



\### 📘 Overview

This project is designed to \*\*track investment portfolios\*\* and calculate performance and risk metrics using \*\*Python\*\* and \*\*Power BI\*\*.  

It automates:

\- Price data fetching (via Yahoo Finance)

\- Portfolio valuation and daily metrics computation

\- Risk KPIs like Sharpe, Beta, Drawdown, and Tracking Error

\- Dashboard visualization using Power BI



---



\### 🧩 Tech Stack

\- \*\*Python 3.10+\*\*

\- \*\*Pandas\*\*, \*\*NumPy\*\*, \*\*yfinance\*\*

\- \*\*Matplotlib / Power BI\*\* for visualization

\- \*(Optional)\* Microsoft Power Apps for front-end integration



---



\### ⚙️ How to Run



```bash

python -m venv .venv

.venv\\Scripts\\activate

pip install -r requirements.txt

python src\\fetch\_prices.py

python src\\compute\_metrics.py

Output Files



All analytics will be stored in the output/ folder:



File	Description

prices\_daily.csv	Adjusted close prices for portfolio tickers

positions\_daily.csv	Daily position values

portfolio\_daily.csv	Portfolio KPIs – returns, volatility, Sharpe, Beta, Alpha

🧠 Key Metrics



Cumulative Return



Annual Volatility



Sharpe Ratio



Maximum Drawdown



Beta vs Benchmark (SPY)



Tracking Error



Alpha (Annualized)



🖼️ Power BI Dashboard (optional)



Visualize portfolio trends using Power BI:



Total portfolio value over time



Risk metrics charts (Volatility, Drawdown)



Holdings breakdown by ticker or sector



📁 Project Structure

portfolio-tracker/

│

├── data/                # Holdings \& transactions CSVs

├── output/              # Auto-generated analytics

├── src/                 # Python source files

├── powerbi/             # Power BI dashboard (.pbix)

├── .venv/               # Virtual environment (ignored)

└── README.md

