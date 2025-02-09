import redis
import sys
from configuration.connection import REDISCACHE
REDISCACHE = REDISCACHE()

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=REDISCACHE.HOST,
            port=int(REDISCACHE.PORT),
            password=REDISCACHE.PASSWORD,
            db=REDISCACHE.DB,
            socket_timeout=int(REDISCACHE.SOCKET_TIMEOUT),
        )
        ping = client.ping()
        if ping is True:
            print('Redis ping is OK')
            return client
        else:
            print('Redis ping is NOK')
    except redis.AuthenticationError:

        print("AuthenticationError")

    except Exception as e:
        print("Redis errror",e)
        # sys.exit(1)



client = redis_connect()