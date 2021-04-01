import redis

if __name__ == '__main__':
    r = redis.Redis()
    r.lpush("aisao:start_urls", "https://www.f4mm.com/beauty")
    r.close()