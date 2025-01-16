import requests
import pandas as pd 
import time 
from datetime import datetime, timedelta

class CoinbaseAPI:

    def __init__(self, base_url="https://api.exchange.coinbase.com", rate_limit=10):
        self.base_url = base_url
        self.rate_limit = rate_limit 
        self.last_request_time = None 

    def rate_limiter(self):
        if self.last_request_time:
            elapsed_time = time.time() - self.last_request_time
            wait_time = max(0, 1 / self.rate_limit - elapsed_time)
            if wait_time > 0:
                time.sleep(wait_time)
        self.last_request_time = None 

    def get_products(self):
        self.rate_limiter() 

        url = f'{self.base_url}/products'
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        
        else:
            raise Exception(f'Error fetching products: {response.status_code}, {response.text}')
        
    
    def get_ticker(self, product_id):
        self.rate_limiter()

        url = f'{self.base_url}/products/{product_id}/ticker'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Error fetching ticker data for {product_id}: {response.status_code}, {response.text}')
        
    def get_candles(self, product_id, start, end, granularity):
        self.rate_limiter()

        url = f'{self.base_url}/products/{product_id}/candles'
        params = {
            'start': start,
            'end': end, 
            'granularity': granularity
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            colums = ['time', 'low', 'high', 'open', 'close', 'volume']
            data = response.json()
            df = pd.DataFrame(data, columns=colums)
            df['time'] = pd.to_datetime(df['time'], unit = 's')
            return df.sort_values('time')
        else:
            raise Exception(f'Error fetching candles: {response.status_code}, {response.text}')
        

    def get_stats(self, product_id):
        url = f'{self.base_url}/products/{product_id}/stats'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching stats for {product_id}: {response.status_code}, {response.text}")