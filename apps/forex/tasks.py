import logging
from decimal import Decimal

from celery.task import task

from apps.forex.redis import get_btcusdt_resistance, set_btcusdt_resistance, set_btcusdt_support, get_btcusdt_support
from binance.client import Client

from config import settings
from core.sms.telstra_api_v2 import send_to_admin

log = logging.getLogger(__name__)


@task
def monitor_btcusdt_price():
    btcusdt_support = get_btcusdt_support()
    btcusdt_resistance = get_btcusdt_resistance()

    try:
        btcusdt_support = Decimal(str(btcusdt_support))
    except Exception as ex:
        btcusdt_support = None
    try:
        btcusdt_resistance = Decimal(str(btcusdt_resistance))
    except Exception as ex:
        btcusdt_resistance = None

    if not btcusdt_support and not btcusdt_resistance:
        return

    client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)
    data = client.get_margin_price_index(symbol='BTCUSDT')
    price = data.get('price', None)

    try:
        price = Decimal(str(price))
    except Exception as ex:
        price = None

    if not price:
        return

    if btcusdt_support and price < btcusdt_support:
        send_to_admin(f'BTCUSDT lower than support {btcusdt_support}.')
        set_btcusdt_support('')

    if btcusdt_resistance and price > btcusdt_resistance:
        send_to_admin(f'BTCUSDT higher than resistance {btcusdt_resistance}.')
        set_btcusdt_resistance('')
