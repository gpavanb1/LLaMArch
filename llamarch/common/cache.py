import redis  # or any other cache library you prefer


class Cache:
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value, expiration=None):
        self.client.set(key, value, ex=expiration)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)

    def exists(self, key):
        return self.client.exists(key) == 1

    def get_all_values(self):
        """
        Retrieve all values stored in the cache.
        """
        keys = self.client.keys('*')  # Get all keys
        return [self.client.get(key) for key in keys if self.client.exists(key)]
