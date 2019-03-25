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
