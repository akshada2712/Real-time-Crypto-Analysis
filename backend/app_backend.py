from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
import pandas as pd
from supabase import create_client, Client
from backend.data_fetcher import CoinbaseAPI
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Initialize Supabase and Coinbase API
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)
api = CoinbaseAPI()

def get_last_database_timestamp(product_id):
    query = (
        supabase.table('crypto_data')
        .select('time')
        .eq('product_id', product_id)
        .order('time', desc=True)
        .limit(1)
        .execute()
    )
    return pd.to_datetime(query.data[0]['time'], utc=True) if query.data else None

def fetch_and_store_new_data(product_id):
    last_timestamp = get_last_database_timestamp(product_id)
    current_timestamp = datetime.now(timezone.utc)
    if last_timestamp is None:
        last_timestamp = current_timestamp - timedelta(days=1)
    new_candles = api.get_candles(
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
        supabase.table('crypto_data').upsert(
            records,
            on_conflict='product_id,time'
        ).execute()
        return new_data
    return pd.DataFrame()

def fetch_historical_data(product_id, days=30):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    query = (
        supabase.table('crypto_data')
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

def calculate_technical_indicators(df):
    df['SMA20'] = df['close'].rolling(window=20).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['Volume_SMA20'] = df['volume'].rolling(window=20).mean()
    df['Daily_Range'] = df['high'] - df['low']
    df['Range_SMA10'] = df['Daily_Range'].rolling(window=10).mean()
    return df

@app.route('/historical-data', methods=['GET'])
def get_historical_data():
    product_id = request.args.get('product_id')
    days = int(request.args.get('days', 30))
    df = fetch_historical_data(product_id, days)
    if not df.empty:
        df = calculate_technical_indicators(df)
    return jsonify(df.to_dict(orient='records'))

@app.route('/ticker-data', methods=['GET'])
def get_ticker_data():
    product_id = request.args.get('product_id')
    ticker = api.get_ticker(product_id)
    return jsonify({
        'price': float(ticker['price']),
        'volume': float(ticker['volume']),
        'bid': float(ticker['bid']),
        'ask': float(ticker['ask']),
        'time': datetime.fromisoformat(ticker['time'].replace('Z', '+00:00')).isoformat()
    })

@app.route('/update-data', methods=['POST'])
def update_data():
    product_id = request.json.get('product_id')
    fetch_and_store_new_data(product_id)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)