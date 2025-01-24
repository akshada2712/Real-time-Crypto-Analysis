import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, timezone
import pandas as pd
import time
from dotenv import load_dotenv
from supabase import create_client, Client
from data_fetcher import CoinbaseAPI
import os

class LiveCryptoDashboard:
    def __init__(self):
        self.api = CoinbaseAPI()
        load_dotenv()
        self.supabase_url = st.secrets["SUPABASE_URL"]
        self.supabase_key = st.secrets["SUPABASE_KEY"]
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    def get_last_database_timestamp(self, product_id):
        query = (
            self.supabase.table('crypto_data')
            .select('time')
            .eq('product_id', product_id)
            .order('time', desc=True)
            .limit(1)
            .execute()
        )
        return pd.to_datetime(query.data[0]['time'], utc=True) if query.data else None

    def fetch_and_store_new_data(self, product_id):
        last_timestamp = self.get_last_database_timestamp(product_id)
        current_timestamp = datetime.now(timezone.utc)
        if last_timestamp is None:
            last_timestamp = current_timestamp - timedelta(days=1)
        new_candles = self.api.get_candles(
            product_id,
            last_timestamp.isoformat(),
            current_timestamp.isoformat(),
            900
        )
        if not new_candles.empty:
            new_data = pd.DataFrame(new_candles, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
            new_data['product_id'] = product_id
            new_data['time'] = new_data['time'].apply(lambda x: x.isoformat())
            records = new_data.to_dict('records')
            self.supabase.table('crypto_data').upsert(
                records,
                on_conflict='product_id,time'
            ).execute()
            return new_data
        return pd.DataFrame()

    def fetch_historical_data(self, product_id, days=30):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        query = (
            self.supabase.table('crypto_data')
            .select('*')
            .eq('product_id', product_id)
            .gte('time', start_time.isoformat())
            .lte('time', end_time.isoformat())
            .order('time')
            .execute()
        )
        if query.data:
            df = pd.DataFrame(query.data)
            df['time'] = pd.to_datetime(df['time'], utc=True)
            return df
        return pd.DataFrame()

    def calculate_technical_indicators(self, df):
        df['SMA20'] = df['close'].rolling(window=20).mean()
        df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['Volume_SMA20'] = df['volume'].rolling(window=20).mean()
        df['Daily_Range'] = df['high'] - df['low']
        df['Range_SMA10'] = df['Daily_Range'].rolling(window=10).mean()
        return df

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
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3],
            subplot_titles=(f'{selected_pair} Price Chart', 'Volume')
        )
        fig.add_trace(
            go.Candlestick(
                x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='OHLC',
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            row=1, col=1
        )
        volume_colors = ['green' if close > open else 'red' for close, open in zip(df['close'], df['open'])]
        fig.add_trace(
            go.Bar(
                x=df['time'],
                y=df['volume'],
                marker_color=volume_colors,
                name='Volume'
            ),
            row=2, col=1
        )
        fig.update_layout(
            title=f'{selected_pair} Market Analysis',
            xaxis_title='Time',
            yaxis_title='Price',
            yaxis2_title='Volume',
            xaxis_rangeslider_visible=False,
            height=800,
            template='plotly_white'
        )
        return fig

    def run_dashboard(self):
        st.set_page_config(page_title='Real-time Crypto Dashboard', layout='wide')
        st.title("Real-time Cryptocurrency Dashboard")
        st.sidebar.header("Settings")

        products_df = self.api.get_products()
        counts = products_df['base_currency'].value_counts()
        filtered_products = products_df[
            (products_df['base_currency'].map(counts) >= 5) &
            (products_df['quote_currency'] == 'USD') &
            (products_df['status'] == 'online')
        ]
        trading_pairs = sorted(filtered_products['id'].to_list())
        default_index = trading_pairs.index('BTC-USD') if 'BTC-USD' in trading_pairs else 0
        selected_pair = st.sidebar.selectbox("Select Trading Pair", trading_pairs, index=default_index)
        timeframe_options = {
            "Last 24 Hours": 1,
            "Last 3 Days": 3,
            "Last Week": 7,
            "Last 2 Weeks": 14,
            "Last Month": 30
        }
        selected_timeframe = st.sidebar.selectbox("Select Timeframe", list(timeframe_options.keys()))
        lookback_days = timeframe_options[selected_timeframe]

        metrics_placeholder = st.empty()
        chart_placeholder = st.empty()
        last_updated_placeholder = st.empty()

        while True:
            try:
                self.fetch_and_store_new_data(selected_pair)
                historical_df = self.fetch_historical_data(selected_pair, days=lookback_days)
                ticker_data = self.get_ticker_data(selected_pair)

                if not historical_df.empty:
                    historical_df = self.calculate_technical_indicators(historical_df)
                    with metrics_placeholder.container():
                        latest = historical_df.iloc[-1]
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            price_change = ((ticker_data['price'] - latest['open']) / latest['open']) * 100
                            st.metric("Current Price", f"${ticker_data['price']:.2f}", f"{price_change:.2f}%")
                        with col2:
                            vol_change = ((ticker_data['volume'] - historical_df['volume'].mean()) / historical_df['volume'].mean())
                            st.metric("Volume", f"{ticker_data['volume']:.2f}", f"{vol_change:.2f}%")
                        with col3:
                            st.metric("Daily Range", f"${latest['Daily_Range']:.2f}", f"Avg: ${latest['Range_SMA10']:.2f}")
                        with col4:
                            st.metric("SMA20", f"${latest['SMA20']:.2f}")
                        with col5:
                            st.metric("EMA20", f"${latest['EMA20']:.2f}")

                    fig = self.create_candlestick_chart(historical_df, selected_pair)
                    chart_placeholder.plotly_chart(fig, use_container_width=True)

                    last_updated_placeholder.text(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                time.sleep(60)

            except Exception as e:
                st.error(f"Error updating dashboard: {str(e)}")
                time.sleep(5)


if __name__ == '__main__':
    dashboard = LiveCryptoDashboard()
    dashboard.run_dashboard()
