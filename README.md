````markdown
# 📊 Portfolio Optimizer

A Python-based portfolio optimization tool using **Modern Portfolio Theory (MPT)**.  
It fetches real financial data via Yahoo Finance, computes risk and return metrics, and optimizes the **Sharpe Ratio** using constrained optimization.

---

## 🧠 Features

- Fetches historical price data using `yfinance`
- Calculates daily returns, annualized expected return, and volatility
- Supports **long-only** and **long-short** portfolios
- Computes and visualizes the **efficient frontier**
- Identifies and highlights the **optimal portfolio** based on Sharpe Ratio
- Clean object-oriented architecture and customizable asset list

---

## 🚀 Quick Start

```bash
pip install numpy pandas matplotlib scipy yfinance
python main.py
````

---

## 📈 Example Output

* ✅ Optimal Weights
* ✅ Annual Expected Return
* ✅ Annual Volatility
* ✅ Sharpe Ratio
* 📉 Efficient Frontier Plot with color-coded Sharpe Ratios and optimal portfolio marked

![Efficient Frontier Example](https://github.com/user-attachments/assets/4f5f74f3-ad41-41c7-a1c8-6865bccccdd3)

---

## ⚙️ Configuration

You can change the ticker list and date range in the constructor:

```python
optimizer = PortfolioOptimizer(
    tickers=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
    start_date='2021-01-01',
    end_date='2024-01-01'
)
```

---

## 📚 Dependencies

* `numpy`
* `pandas`
* `matplotlib`
* `scipy`
* `yfinance`

---

## 📜 License

MIT License

---

## 🧑‍💻 Author

Built by a self-taught quant dev with a passion for financial modeling, optimization, and real-world applications of math and code.



