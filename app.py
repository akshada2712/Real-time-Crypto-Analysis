import streamlit as st 
import plotly.graph_objects as go 
from datetime import datetime, timedelta
import pandas as pd 
import time 
from plotly.subplots import make_subplots
from data_fetcher import CoinbaseAPI

class CryptoDashboard: 

    def __init__(self):
        self.api = CoinbaseAPI()

    def get_optimal_granularity(self, days):
        if days <= 3:
            return 900  
        elif days <= 7:
            return 3600  
        elif days <= 14:
            return 21600 
        else:
            return 86400
        
    def get_ticker_data(self, product_id):
        ticker = self.api.get_ticker(product_id)
        return {
            'price': float(ticker['price']),
            'volume': float(ticker['volume']),
            'bid': float(ticker['bid']),
            'ask': float(ticker['ask']),
            'time': datetime.fromisoformat(ticker['time'].replace('Z', '+00:00'))
        }
        
    def create_candlestick_chart(self, df, selected_pair):
        fig = make_subplots(rows = 2, cols = 1, 
                            shared_xaxes=True,
                            vertical_spacing=0.03,
                            row_heights=[0.7, 0.3])
        
        fig.add_trace(go.Candlestick(
            x=df['time'],
            open = df['open'],
            high = df['high'],
            low = df['low'],
            close = df['close'],
            name = 'OHLC'
        ), 
        row = 1, col = 1)

        colors = ['red' if close < open else 'green' 
                 for close, open in zip(df['close'], df['open'])]
        

        fig.add_trace(go.Bar(
            x=df['time'],
            y = df['volume'],
            marker_color = colors,
            name= 'Volume'
        ),
        row = 2, col = 1)


        fig.update_layout(
            title=f'{selected_pair} Market Analysis',
            yaxis_title='Price',
            yaxis2_title='Volume',
            xaxis_rangeslider_visible=False,
            height=800
        )

        return fig
    

    def get_technical_analysis(self, df):
        # simple moving average, for 20 windos 

        df['SMA20'] = df['close'].rolling(window=20).mean()

        # exponnetial moving average
        df['EMA20'] = df['close'].ewm(span = 20, adjust = False).mean()
       
        # Volume analysis
        df['Volume_SMA20'] = df['volume'].rolling(window=20).mean()
        
        # Price range analysis
        df['Daily_Range'] = df['high'] - df['low']
        
        df['Range_SMA10'] = df['Daily_Range'].rolling(window=10).mean()
        
        return df
    
    def run_dashboard(self): 
        st.set_page_config(
            page_title='Real-time Crypto Dashboard', 
            layout = 'wide'
        )
        st.title("Real-time Cryptocurrency Dashboard")

        st.sidebar.header("Settings")

        products_df = self.api.get_products()
        counts = products_df['base_currency'].value_counts()

        # Filter rows where base_currency count is greater than 5 and quote_currency is 'USD'
        filtered_products = products_df[
            (products_df['base_currency'].map(counts) >= 5) & 
            (products_df['quote_currency'] == 'USD') & 
            (products_df['status'] == 'online')
        ]

        trading_pairs = sorted(filtered_products['id'].to_list())

        # Set default to BTC-USD
        default_index = trading_pairs.index('BTC-USD') if 'BTC-USD' in trading_pairs else 0
        selected_pair = st.sidebar.selectbox(
            "Select Trading Pair",
            trading_pairs,
            index=default_index
        )

        timeframe_options = {
            "Last 24 Hours": 1,
            "Last 3 Days": 3,
            "Last Week": 7,
            "Last 2 Weeks": 14,
            "Last Month": 30
        }

        selected_timeframe = st.sidebar.selectbox(
            "Select Timeframe",
            list(timeframe_options.keys())
        )
        lookback_days = timeframe_options[selected_timeframe]

        metrics_placeholder = st.empty()
        chart_placeholder = st.empty()

        while True: 
            try:
                end_time = datetime.now()
                start_time = end_time - timedelta(days=lookback_days)

                granularity = self.get_optimal_granularity(lookback_days)

                df = self.api.get_candles(
                    product_id=selected_pair,
                    start = start_time.isoformat(),
                    end = end_time.isoformat(),
                    granularity=granularity
                )

                ticker_data = self.get_ticker_data(selected_pair)

                df = self.get_technical_analysis(df)

                with metrics_placeholder.container():
                    latest = df.iloc[-1]
                    col1, col2, col3, col4, col5 = st.columns(5)

                    with col1:
                        price_change = ((ticker_data['price'] - latest['open']) / latest['open']) * 100 
                        st.metric(
                            "Current Price", 
                            f"${ticker_data['price']:.2f}", 
                            f"{price_change:.2f}%"
                        )

                    with col2:
                        vol_change = ((ticker_data['volume'] - df['volume'].mean()) / df['volume']. mean())

                        st.metric("Volume", 
                                  f"{ticker_data['volume']:.2f}", 
                                f"{vol_change:.2f}%"
                                )
                        
                    
                    with col3:
                        st.metric("Daily Range",
                                f"${latest['Daily_Range']:.2f}",
                                f"Avg: ${latest['Range_SMA10']:.2f}")
                    
                    with col4:
                        st.metric("SMA20",
                                f"${latest['SMA20']:.2f}")
                    
                    with col5:
                        st.metric("EMA20",
                                f"${latest['EMA20']:.2f}")
                        
                
                fig = self.create_candlestick_chart(df, selected_pair)
                chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"chart_{time.time()}") 

                time.sleep(60)


            except Exception as e:
                st.error(f"Error updating dashboard: {str(e)}")
                time.sleep(5)
                continue


if __name__ == '__main__':
    dashboard = CryptoDashboard()
    dashboard.run_dashboard()
