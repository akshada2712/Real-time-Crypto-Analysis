import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client
import time
from data_fetcher import CoinbaseAPI

class LiveCryptoDashboard:
    def __init__(self):
        load_dotenv()
        self.api = CoinbaseAPI()
        self.supabase_url = st.secrets["SUPABASE_URL"]
        self.supabase_key = st.secrets["SUPABASE_KEY"]
        self.supabase = create_client(self.supabase_url, self.supabase_key)

    def get_products_from_database(self):
        """Retrieve product IDs from the `crypto_products` table."""
        query = self.supabase.table('crypto_products').select('product_id').execute()
        if query.data:
            return [item['product_id'] for item in query.data]
        return []
    
    def fetch_historical_data(self, product_id, days):
        """Fetch historical data for the selected trading pair."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        print(start_time, end_time)
        query = (
            self.supabase.table('coinbase_data')
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

    def fetch_predictions(self, product_id, days):
        """Fetch prediction data for the selected trading pair."""
        current_time = datetime.now()
        start_time = current_time - timedelta(days=days)
        print('f',start_time, current_time)
        query = (
            self.supabase.table('coinbase_predictions')
            .select('*')
            .eq('product_id', product_id)
            .gte('prediction_date', start_time.isoformat())  # Predictions for the last day
            .order('prediction_date')
            .execute()
        )
        if query.data:
            df = pd.DataFrame(query.data)
            #print(df.iloc[0])

            # Convert 'prediction_date' to datetime
            df['prediction_date'] = pd.to_datetime(
                df['prediction_date'], utc=True  # Use 'mixed' to handle variations
            )
            return df
        return pd.DataFrame()


    def predictions_chart(self, historical_df, prediction_df, selected_pair):
        """Create an enhanced combined chart of historical data and predictions."""
        fig = make_subplots(
            rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.03,
            subplot_titles=(f'{selected_pair} Price Chart with Predictions',)
        )

        # Historical data line with markers
        fig.add_trace(
            go.Scatter(
                x=historical_df['time'], 
                y=historical_df['close'],
                mode='lines+markers', 
                name='Testing Data', 
                line=dict(color='blue'),
                marker=dict(symbol='circle', size=6),
                hovertemplate="<b>Time:</b> %{x}<br><b>Price:</b> %{y:.2f}<extra></extra>"
            )
        )

        # Prediction data line with markers
        if not prediction_df.empty:
            fig.add_trace(
                go.Scatter(
                    x=prediction_df['prediction_date'], 
                    y=prediction_df['predicted_price'],
                    mode='lines+markers', 
                    name='Predictions', 
                    line=dict(color='orange'),
                    marker=dict(symbol='circle', size=4),
                    hovertemplate="<b>Prediction Time:</b> %{x}<br><b>Predicted Price:</b> %{y:.2f}<extra></extra>"
                )
            )

        # Customize the layout
        fig.update_layout(
            title=f'{selected_pair} Market Analysis with Predictions',
            xaxis_title='Time',
            yaxis_title='Closing Price',
            xaxis=dict(
                showgrid=True,
                tickformat='%Y-%m-%d %H:%M',
                tickangle=45),
            yaxis=dict(showgrid=True),
            template='plotly_white',
            legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.2),
            hovermode='x unified'  # Unified hover mode for better insights
        )

        # Highlight the current price or last prediction if available
        if not prediction_df.empty:
            fig.add_trace(
                go.Scatter(
                    x=[prediction_df.iloc[-1]['prediction_date']],
                    y=[prediction_df.iloc[-1]['predicted_price']],
                    mode='markers+text',
                    name='Latest Prediction',
                    marker=dict(size=10, color='red', symbol='star'),
                    text=[f"Pred: {prediction_df.iloc[-1]['predicted_price']:.2f}"],
                    textposition="top center",
                    showlegend=False
                )
            )

        return fig
    

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

        product_ids = self.get_products_from_database()
        trading_pairs = sorted(product_ids)
        default_index = trading_pairs.index('ETH-USD') if 'ETH-USD' in trading_pairs else 0
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
        chart_selection_placeholder = st.empty()
        visualization_placeholder = st.empty()

        st.markdown(
        """
        <style>
        .last-updated {
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: gray;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        last_updated_placeholder = st.empty()

        while True: 
            try:
                historical_df = self.fetch_historical_data(selected_pair, days=lookback_days)
                prediction_df = self.fetch_predictions(selected_pair, days=lookback_days)
                ticker_data = self.get_ticker_data(selected_pair)

                if not historical_df.empty:
                    historical_df = self.calculate_technical_indicators(historical_df)

                    # Display technical indicators
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

                    tab1, tab2 = st.tabs(["📈 Candlestick Chart", "🔮 Prediction Chart"])
                    timestamp_key = int(time.time()) 
                    # Tab 1: Candlestick Chart
                    with tab1:
                        candlestick_chart = self.create_candlestick_chart(historical_df, selected_pair)
                        st.plotly_chart(candlestick_chart, use_container_width=True, key=f"candlestick_chart_{timestamp_key}")  # Use `st.plotly_chart` directly for this tab

                    # Tab 2: Prediction Chart
                    with tab2:
                        pred_chart = self.predictions_chart(historical_df, prediction_df, selected_pair)
                        st.plotly_chart(pred_chart, use_container_width=True, key=f"prediction_chart_{timestamp_key}")  # Use `st.plotly_chart` directly for this tab
                 
                    last_updated_placeholder.markdown(
                    f"<div class='last-updated'>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(60)

            except Exception as e:
                st.error(f"Error updating dashboard: {str(e)}")
                time.sleep(5)

if __name__ == '__main__':
    dashboard = LiveCryptoDashboard()
    dashboard.run_dashboard()