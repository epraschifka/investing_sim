# getPricesApi.py
import sys
sys.path.append("..")
from my_app.models import Holding, Coin, CustomUser
import requests
from datetime import datetime
import json
from django.utils import timezone
from decimal import Decimal

# tracks all coin ids we need to fetch data for
coinID_set = set({})

# tracks number of times func has been called
func_run_count = 0

def func():

    global coinID_set
    global func_run_count

    """ on the first run of the app and every 1000th run of the app:
            1. fetch the top 100 coins.
            2. for each fetched coin:
                    If the fetched coin is not in the coins set:
                        add it to the coins set.
                        make it a coin object in the database """
    

    if (func_run_count % 1000 == 0):
        func_run_count = func_run_count + 1
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en&x_cg_demo_api_key=CG-JPtjy3AuuzkAk31PNjSnUfUC' 
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
        
        # for each fetched coin:
        for coin in data:
            # If the fetched coin is not in the coins set:
            if coin['id'] not in coinID_set:
                # add the coin's id to the coinID_set.
                coinID_set.add(coin['id'])

                # save the coin into our database.
                new_coin = Coin(symbol= coin['symbol'],
                                name= coin['name'],
                                image_url=coin['image'],
                                price=coin['current_price'],
                                market_cap=coin['market_cap'],
                                volume=coin['total_volume'],
                                high_24h=coin['high_24h'],
                                low_24h=coin['low_24h'],
                                change_24h=coin['price_change_24h'],
                                percent_change_24h=coin['price_change_percentage_24h'])
                new_coin.save()
                 
    """ on every run of the app,
            1. fetch data on every coin in the coinID_set
            2. For each fetched coin:
                update its entry in the database            """
    
    base_url = 'https://api.coingecko.com/api/v3/coins/markets'

    params = {
        'vs_currency': "aud",
        'ids': ','.join(coinID_set),  # Join the list elements with commas
        'order': 'market_cap_desc',  # Order by market cap descending
        'per_page': len(coinID_set),  # Set per_page to the number of coins in the list
        'page': 1,
        'sparkline': False,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

    # For each fetched coin:
    for coin in data:
        # find coin in database
        existing_coin = Coin.objects.get(symbol=coin['symbol'])

        # get previous price for later use
        old_price = existing_coin.price

        # update database entry for this coin
        existing_coin.price = coin['current_price']
        existing_coin.market_cap = coin['market_cap']
        existing_coin.volume=coin['total_volume']
        existing_coin.high_24h=coin['high_24h']
        existing_coin.low_24h=coin['low_24h']
        existing_coin.change_24h=coin['price_change_24h']
        existing_coin.percent_change_24h=coin['price_change_percentage_24h']

        # update coin's graph
        coin_graph_dict = json.loads(existing_coin.graph)
        coin_graph_dict["date"].append(str(datetime.now()))
        coin_graph_dict["value"].append(float(existing_coin.price))
        existing_coin.graph = json.dumps(coin_graph_dict)

        # save changes to database
        existing_coin.save()

        # for every holding of this coin:
        for holding in Holding.objects.filter(coin__symbol=coin['symbol']):
            # update the owner's portfolio value by the difference between the 
            # old price and the new price, times the quantity in the holding
            holding.owner.portfolio_value += (Decimal(existing_coin.price)-old_price)*holding.quantity
            holding.owner.save()

        
    

    # everyone's portfolio value has been updated, so push portfolio values
    # to the portfolio graph for each user
    for user in CustomUser.objects.all():
        # convert user.portfolio_graph back into a python dictionary
        portfolio_graph_dict = json.loads(user.portfolio_graph)

        # update date and value lists in the json
        portfolio_graph_dict["date"].append(str(datetime.now()))
        portfolio_graph_dict["value"].append(float(user.portfolio_value))

        # convert back to json, save in user.portfolio_graph
        user.portfolio_graph = json.dumps(portfolio_graph_dict)
        user.save()

    print("database updated.")

