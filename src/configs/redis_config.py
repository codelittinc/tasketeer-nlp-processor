import redis
import os

def redis_instance():
    url = os.environ.get('REDIS_URL', '')
    return redis.Redis.from_url(url=url)