# Real-Time Crypto Dashboard

The **Real-Time Crypto Dashboard** is a dynamic cryptocurrency analysis tool that combines real-time data visualization, predictive analytics, and market trend analysis. It integrates advanced machine learning models like LSTM (Long Short-Term Memory) to forecast cryptocurrency prices, providing users with a powerful interface for exploring and understanding market behavior.

## Features

- **Candlestick Chart**: Visualizes historical price trends with open, high, low, and close prices, accompanied by trading volume.
- **Prediction Chart**: Forecasts future prices using LSTM models, offering insights into market trends.
- **Technical Indicators**:
  - **Exponential Moving Average (EMA)**: Calculated over 20 days for trend analysis.
  - **Simple Moving Average (SMA)**: Computed over 20 days for price movement insights.
  - **Additional Features**: Includes key metrics like high, low, open, close prices, and volume for comprehensive analysis.
- **Year-over-Year (YoY) Change**: Highlights the percentage change in price compared to the same time last year, offering a long-term perspective on market trends.
- **Month-over-Month (MoM) Change**: Tracks the percentage change in price compared to the same time last month, providing insights into recent price movements.
- **Note**: Timezone is in UTC.
## Folder Structure

### Frontend
- `app.py`:
  - Streamlit-based frontend for the dashboard.
  - Connects to Supabase to fetch and display real-time cryptocurrency data.

### Data Fetcher
- `datafetcher.py`:
  - Contains the CoinbaseAPI class to collect live data every 15 minutes from the Coinbase Exchange API.
  - Fetches and stores candlestick data for historical analysis.

### Machine Learning
- `cryptofeatureengineering.ipynb`:
  - The main notebook for LSTM-based price predictions.
  - Features used for training:
    - High, low, open, close prices.
    - Volume.
    - EMA (7 and 30 days).
    - SMA (7 and 30 days).
  - **Error Metric**:
    - **Root Mean Square Error (RMSE)** is used to evaluate model performance.

### Backend
- Other backend files for handling data processing and storage are hidden and not exposed.

## Technical Details

### LSTM Predictions
- LSTM is a type of recurrent neural network (RNN) designed for sequence prediction.
- It processes historical data (e.g., past 48 hours of prices) and predicts the next price.
- Predictions are displayed alongside actual prices in the **Prediction Chart**.

### Key Features in LSTM Model:
- Input sequences of historical data (e.g., 192 timesteps for 15-minute intervals).
- Target values are the next closing price.
- RMSE quantifies the accuracy of predictions.

## Model Evaluation


The following table shows the **Root Mean Square Error (RMSE)** values for each cryptocurrency. RMSE is used to evaluate the accuracy of the LSTM predictions, with lower values indicating better performance.

| Product ID      | RMSE        |
|-----------------|-------------|
| ADA-USD         | 0.0115      |
| ADA-USD         | 0.0125      |
| DOT-USD         | 0.1124      |
| ETH-USD         | 37.8910     |
| BAT-USD         | 0.0022      |
| BTC-USD         | 11302.3387  |
| DOGE-USD        | 0.0793      |
| BTRST-USD       | 0.0255      |
| ATOM-USD        | 0.0845      |
| LINK-USD        | 1.1694      |
| RAD-USD         | 0.0187      |
| MANA-USD        | 0.0080      |
| SUSHI-USD       | 0.0185      |
| SOL-USD         | 10.7063     |
| MATIC-USD       | 0.0039      |
| REQ-USD         | 0.0010      |
| ICP-USD         | 0.1028      |
| XRP-USD         | 0.5542      |

---

### **Insights:**
- **Low RMSE**: Cryptocurrencies like `REQ-USD` (0.0010), `BAT-USD` (0.0022), and `MANA-USD` (0.0080) demonstrate highly accurate predictions.
- **High RMSE**: `BTC-USD` shows a significantly high RMSE (11302.3387), likely due to its large price scale.
- **Moderate RMSE**: Most altcoins, such as `DOT-USD`, `ATOM-USD`, and `XRP-USD`, show moderate prediction accuracy, with RMSE values between 0.1 and 1.0.

This evaluation highlights the effectiveness of the LSTM model in capturing price trends for most cryptocurrencies while identifying areas for further optimization.

## Dashboard

### **1. Real-Time Metrics Chart**

<img width="1448" alt="Screenshot 2025-01-27 at 12 17 33 PM" src="https://github.com/user-attachments/assets/5dca78d8-d659-458c-bc16-b033f998e791" />

This Metrics Chart provides an overview of **real-time cryptocurrency metrics**, offering key insights into the selected trading pair:

- **Price & Volume Metrics**:
  - **Current Price**: Displays the latest price of the selected trading pair.
  - **Volume**: Indicates the trading volume during the selected timeframe.
  - **Daily Range**: Shows the price difference between the highest and lowest value in the last 24 hours.
  - **24h Change**: Reflects the percentage change in price over the past day.

- **Technical & Historical Metrics**:
  - **SMA (20 Days)**: Simple Moving Average over the past 20 days, showing overall price trends.
  - **EMA (20 Days)**: Exponential Moving Average over the past 20 days, focusing on recent price changes.
  - **YoY Change**: Year-over-Year percentage change, comparing the current price with the price from the same day last year.
  - **MoM Change**: Month-over-Month percentage change, comparing the current price with the price from the same day last month.


### **2. Prediction Chart**

![Screenshot 2025-01-26 at 11 45 04 PM](https://github.com/user-attachments/assets/59dacb15-845a-46d0-994f-5f9b3d5f66c0)

The Prediction chart displays **predicted values** for the next six data points, generated using the LSTM model:
- **Markers** indicate the predicted prices at each step.
- A **star marker** highlights the predicted price and time for the final data point (after six minutes).

This setup provides both historical context and forward-looking predictions for informed decision-making.

### **3. Candlestick Chart**
![Screenshot 2025-01-26 at 11 45 27 PM](https://github.com/user-attachments/assets/6301916a-dd82-4d24-992c-5505c6751feb)

The Candlestick chart visualizes historical price trends. It includes:
- **Candlesticks** representing open, high, low, and close prices for each time period.
- **Volume bars** at the bottom to indicate trading activity.



## How to Use

1. **Run the App**:
   - Dashboard Link: https://akshada2712-real-time-crypto-analysis-app-jz2woj.streamlit.app/

2. **Explore the Dashboard**:
   - Select a trading pair (e.g., BTC-USD).
   - Choose a timeframe (e.g., Last Week) for analysis.
   - View:
     - **Real-time metrics**: Current price, volume, daily range.
     - **Candlestick Chart**: Historical trends with technical indicators.
     - **Prediction Chart**: Future price forecasts.

3. **Analyze Results**:
   - Leverage LSTM-based predictions to make informed decisions.
   - Use metrics like RMSE to evaluate prediction accuracy.

## Additional Information

### Key Points from UnderstandingCrypto.md
1. **Candlestick Chart**:
   - Open, high, low, and close prices give a complete view of market activity.
   - Volume bars indicate trading intensity.

2. **Market Sentiment**:
   - Bullish (uptrend): Price increases over time.
   - Bearish (downtrend): Price decreases over time.

3. **Technical Indicators**:
   - SMA and EMA highlight trends and price momentum.
   - Volume analysis shows periods of high and low trading activity.

4. **Data Sources**:
   - All data is fetched from Coinbase Exchange APIs, ensuring accuracy and reliability.
