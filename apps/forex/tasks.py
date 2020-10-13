import logging
from decimal import Decimal

from celery.task import task

from apps.forex.binance import get_btcusdt_price
from apps.forex.redis import get_btcusdt_resistance, set_btcusdt_resistance, set_btcusdt_support, get_btcusdt_support
from core.sms.telstra_api_v2 import send_to_admin

log = logging.getLogger(__name__)


@task
def monitor_btcusdt_price():
    btcusdt_supports = get_btcusdt_support()
    btcusdt_resistances = get_btcusdt_resistance()

    # try:
    #     btcusdt_support = Decimal(str(btcusdt_support))
    # except Exception as ex:
    #     btcusdt_support = None
    # try:
    #     btcusdt_resistance = Decimal(str(btcusdt_resistance))
    # except Exception as ex:
    #     btcusdt_resistance = None

    if not any(btcusdt_supports) or not any(btcusdt_resistances):
        return

    price = get_btcusdt_price()

    if not price:
        return

    alert_support = None
    for index, support in enumerate(btcusdt_supports):
        if support and price < support:
            alert_support = support
            btcusdt_supports[index] = ''
    if alert_support:
        send_to_admin(f'BTC cross down {alert_support}')
        set_btcusdt_support(btcusdt_supports)

    alert_resistance = None
    for index, resistance in enumerate(btcusdt_resistances):
        if resistance and price > resistance:
            alert_resistance = resistance
            btcusdt_resistances[index] = ''
    if alert_resistance:
        send_to_admin(f'BTC cross up {alert_resistance}.')
        set_btcusdt_resistance(btcusdt_resistances)
