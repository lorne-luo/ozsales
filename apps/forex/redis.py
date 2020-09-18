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

def set_btcusdt_resistance(price):
    price_redis.set(BTCUSDT_RESISTANCE_KEY, price)

def get_btcusdt_resistance():
    return price_redis.get(BTCUSDT_RESISTANCE_KEY)

def set_btcusdt_support(price):
    price_redis.set(BTCUSDT_SUPPORT_KEY, price)

def get_btcusdt_support():
    return price_redis.get(BTCUSDT_SUPPORT_KEY)
