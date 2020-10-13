from decimal import Decimal

import redis
from django.conf import settings

SYSTEM_CHANNEL = 14
PRICE_CHANNEL = 15

forex_redis = redis.StrictRedis(host=settings.REDIS_HOST,
                                port=settings.REDIS_PORT,
                                db=SYSTEM_CHANNEL,
                                decode_responses=True)

price_redis = redis.StrictRedis(host=settings.REDIS_HOST,
                                port=settings.REDIS_PORT,
                                db=PRICE_CHANNEL,
                                decode_responses=True)

BTCUSDT_RESISTANCE_KEY = 'BTCUSDT_RESISTANCE'
BTCUSDT_SUPPORT_KEY = 'BTCUSDT_SUPPORT'
SLOTS = 5


def set_btcusdt_resistance(prices):
    empty = ['' for price in prices if not price]
    prices = [price for price in prices if price]
    prices = sorted(prices)
    prices = empty + prices
    for i in range(min(SLOTS, len(prices))):
        price_redis.set(f'{BTCUSDT_RESISTANCE_KEY}_{i+1}', prices[i])


def get_btcusdt_resistance():
    prices = [price_redis.get(f'{BTCUSDT_RESISTANCE_KEY}_{i+1}') for i in range(SLOTS)]
    prices = [None if not price else Decimal(str(price)) for price in prices]
    return prices


def set_btcusdt_support(prices):
    empty = ['' for price in prices if not price]
    prices = [price for price in prices if price]
    prices = sorted(prices, reverse=True)
    prices = empty + prices
    for i in range(min(SLOTS, len(prices))):
        price_redis.set(f'{BTCUSDT_SUPPORT_KEY}_{i+1}', prices[i])


def get_btcusdt_support():
    prices = [price_redis.get(f'{BTCUSDT_SUPPORT_KEY}_{i+1}') for i in range(SLOTS)]
    prices = [None if not price else Decimal(str(price)) for price in prices]
    return prices
