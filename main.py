import sys
import os

print("Coucou ! (from print)")
sys.stdout.write("Coucou ! (from sys.stdout.write)")
sys.stdout.flush()

import rq
print(u"'rq' module loaded")
import redis
print(u"'redis' module loaded")


listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with rq.Connection(conn):
        worker = rq.Worker(map(rq.Queue, listen))
        worker.work()
