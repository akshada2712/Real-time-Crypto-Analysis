# **Real-Time Crypto Dashboard**

## **Overview**
The **CryptoDashboard** is a real-time cryptocurrency analysis tool designed for beginners. It provides insights into cryptocurrency price movements, trends, and market patterns through an intuitive interface.

Key Features:
- Real-time price updates and metrics.
- Historical price analysis using candlestick charts.
- Technical indicators like SMA (Simple Moving Average) and EMA (Exponential Moving Average).
- Visual market sentiment analysis with price patterns.

---


## **How to Use**
1. **Select Trading Pair**:
   - Use the **dropdown menu** to choose the trading pair (e.g., BTC-USD, ETH-USD).

2. **Choose Timeframe**:
   - Select a timeframe (e.g., Last 24 Hours, Last Week) to view historical price trends.

3. **Explore Metrics**:
   - View real-time metrics such as:
     - **Current Price**: Latest price of the selected trading pair.
     - **Volume**: Total volume traded during the selected period.
     - **Daily Range**: Difference between the highest and lowest prices.

4. **Analyze Charts**:
   - Use the candlestick chart to understand historical price movements and volume trends.

---

## **Understanding Candlestick Charts**

A **candlestick chart** is a graphical representation of an asset's price movement over a specific period. Each candlestick provides:

### **Candlestick Components**
- **Open Price**: The price at the start of the period.
- **Close Price**: The price at the end of the period.
- **High Price**: The highest price reached during the period.
- **Low Price**: The lowest price reached during the period.

### **Candle Colors**
- **Green Candle**: The closing price is higher than the opening price (price increase).
- **Red Candle**: The closing price is lower than the opening price (price decrease).

### **What Candlesticks Show**
- **Price Change**: Indicates how much the price changed during the period.
- **Lowest and Highest Prices**: The wicks (shadows) represent the high and low prices.

---

## **Market Patterns and Sentiment**

### **Price Patterns**
- **Neutral**: Prices fluctuate within a narrow range, showing no significant trend.
- **Bullish (Uptrend)**: A series of green candles indicates increasing prices, driven by optimism and buying pressure.
- **Bearish (Downtrend)**: A series of red candles indicates decreasing prices, driven by pessimism and selling pressure.

### **Fear and Greed Patterns**
- **Fear**: High fear leads to bearish trends as investors sell assets.
- **Greed**: High greed leads to bullish trends as investors buy assets.

---

## **Data Points**
The data for the dashboard is obtained from Coinbase Exchange APIs.

### **1. Ticker Data**
- Retrieved using the **Ticker API** to provide real-time information about the selected trading pair.

#### **Key Fields**:
| Field      | Description                                      |
|------------|--------------------------------------------------|
| `price`    | Current price of the cryptocurrency.             | 
| `volume`   | Trading volume in the last 24 hours.             |
| `bid`      | Highest price a buyer is willing to pay.         | 
| `ask`      | Lowest price a seller is willing to accept.      |
| `time`     | Timestamp of the latest trade (ISO format).      | 

#### **Usage**:
- **Price**: Displayed as "Current Price" in the dashboard.
- **Volume**: Used in metrics to calculate volume change.
- **Bid/Ask**: Provides insight into market demand.

---

### **2. Candlestick Data**
- Retrieved using the **Candles API** for historical price analysis.

#### **Key Fields**:
| Field      | Description                                       | 
|------------|---------------------------------------------------|
| `time`     | Timestamp of the start of the candle period.      | 
| `open`     | Opening price during the candle period.           | 
| `high`     | Highest price during the candle period.           |
| `low`      | Lowest price during the candle period.            | 
| `close`    | Closing price during the candle period.           | 
| `volume`   | Total volume traded during the candle period.     | 

#### **Usage**:
- **OHLC Data**: Plotted on candlestick charts to visualize price trends.
- **Volume**: Shown below the candlestick chart for market activity analysis.

---

### **3. Technical Indicators**
- Computed from candlestick data to provide additional insights.

#### **Key Indicators**:
| Indicator        | Description                                                     | 
|------------------|-----------------------------------------------------------------|
| `SMA20`          | Simple Moving Average over 20 periods.                          | 
| `EMA20`          | Exponential Moving Average with more weight on recent prices.   | 
| `Volume_SMA20`   | Moving average of volume over 20 periods.                       | 
| `Daily_Range`    | Difference between high and low prices for a period.            | 
| `Range_SMA10`    | Average daily range over 10 periods.                            | 

#### **Usage**:
- **SMA20/EMA20**: Used for analyzing price trends and momentum.
- **Daily Range**: Highlights market volatility.

---

### **4. Products Data**
- Retrieved using the **Products API** to provide available trading pairs.

#### **Key Fields**:
| Field             | Description                                    | Example Value |
|-------------------|------------------------------------------------|---------------|
| `id`              | Identifier for the trading pair.               | BTC-USD       |
| `base_currency`   | The cryptocurrency being traded.               | BTC           |
| `quote_currency`  | The currency used for quoting the base asset.  | USD           |
| `status`          | Trading status of the pair (e.g., online).     | online        |

#### **Usage**:
- Used in the **dropdown menu** for selecting trading pairs.

---

## **Analysis Features**

### **Candlestick Chart**
- Displays historical price trends for the selected trading pair.
- Includes **volume bars** to show market activity.

### **Technical Indicators**
1. **Simple Moving Average (SMA20)**:
   - Average closing price over the last 20 periods.
   - Identifies overall trends.
   
2. **Exponential Moving Average (EMA20)**:
   - A weighted moving average with emphasis on recent prices.
   - Highlights price momentum.

3. **Volume SMA20**:
   - Average trading volume over the last 20 periods.
   - Shows high or low trading activity trends.

### **Daily Range**
- Difference between the highest and lowest prices during the selected period.
- Indicates market volatility.

### **Real-Time Metrics**
- **Current Price**: Latest traded price of the cryptocurrency.
- **Volume**: Total volume traded.
- **Price Change**: Percentage change compared to the previous period.

---

## **Summary**
The **CryptoDashboard** is an ideal starting point for anyone new to cryptocurrency trading. It helps users:
- Understand market trends with candlestick charts.
- Analyze price movements using technical indicators.
- Recognize market sentiment and patterns like bullish and bearish trends.

This tool bridges the gap for beginners looking to explore the cryptocurrency market and make informed decisions.

---