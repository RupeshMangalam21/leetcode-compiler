import os
import redis
from rq import Worker, Queue, Connection

# Redis connection settings
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        print("Worker is starting...")
        q = Queue()  # Default queue
        worker = Worker([q])
        worker.work()
