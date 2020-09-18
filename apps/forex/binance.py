from decimal import Decimal
from binance.client import Client
from config import settings


def get_btcusdt_price():
    client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)
    data = client.get_margin_price_index(symbol='BTCUSDT')
    price = data.get('price', None)

    try:
        price = Decimal(str(price))
    except Exception as ex:
        price = None
    return price
