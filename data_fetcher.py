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
        """
        Ensures the API calls comply with the rate limit by adding delays if necessary.
        Note:
        - The API returns a maximum of 300 candles per request. 
        - Granularity is set to 900 seconds (15 minutes)
        - To avoid overloading the server and stay within the rate limits, a delay is introduced between requests.
        """
        if self.last_request_time:
            elapsed_time = time.time() - self.last_request_time
            wait_time = max(0, 1 / self.rate_limit - elapsed_time)
            if wait_time > 0:
                time.sleep(wait_time)
        self.last_request_time = None 

    def get_products(self):
        """
        Fetches a list of available trading products (e.g., BTC-USD, ETH-USD) from the API.
        Returns:
        - A DataFrame containing product details if successful.
        Raises:
        - Exception if the API request fails.
        """
        self.rate_limiter() 

        url = f'{self.base_url}/products'
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        
        else:
            raise Exception(f'Error fetching products: {response.status_code}, {response.text}')
        
    
    def get_ticker(self, product_id):
        """
        Fetches the latest ticker information for a specific product.
        Parameters:
        - product_id: The trading pair to fetch data for (e.g., BTC-USD).
        Returns:
        - JSON response containing ticker information if successful.
        Raises:
        - Exception if the API request fails.
        """
        self.rate_limiter()

        url = f'{self.base_url}/products/{product_id}/ticker'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Error fetching ticker data for {product_id}: {response.status_code}, {response.text}')
        
    def get_candles(self, product_id, start, end, granularity):
        """
        Fetches historical candlestick (OHLCV) data for a specific product.
        Parameters:
        - product_id: The trading pair to fetch data for (e.g., BTC-USD).
        - start: Start time for the data (ISO8601 format).
        - end: End time for the data (ISO8601 format).
        - granularity: Time interval between data points in seconds (e.g., 60, 300, 900).
        Returns:
        - A DataFrame containing candlestick data with columns ['time', 'low', 'high', 'open', 'close', 'volume'].
        Raises:
        - Exception if the API request fails.
        """
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
        """
        Fetches 24-hour statistics for a specific product.
        Parameters:
        - product_id: The trading pair to fetch statistics for (e.g., BTC-USD).
        Returns:
        - JSON response containing statistics if successful.
        Raises:
        - Exception if the API request fails.
        """
        url = f'{self.base_url}/products/{product_id}/stats'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        
        else:
            raise Exception(f"Error fetching stats for {product_id}: {response.status_code}, {response.text}")