import sys
sys.path.append("..")
from myapp.models import Coin
import requests

coins = Coin.objects.all()

def func():
    """ url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'aud',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': False,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Successfully retrieved data
        data = response.json()
        
        # for each coin...
        for coin_data in data:
            current_coin = Coin.objects.get(name=coin_data['name'])
            current_coin.price = coin_data['current_price']
            current_coin.market_cap = coin_data['market_cap']
            current_coin.volume = coin_data['total_volume']
            current_coin.high_24h = coin_data['high_24h']
            current_coin.low_24h = coin_data['low_24h']
            current_coin.change_24h = coin_data['price_change_24h']
            current_coin.percent_change_24h = coin_data['price_change_percentage_24h']
            current_coin.save()
        
        print("database updated.")
    else:
        # Handle the error
        print(f"Error: {response.status_code}") """

