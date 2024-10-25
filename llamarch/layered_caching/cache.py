class Cache:
    def __init__(self):
        self.store = {}

    def get(self, query):
        # Retrieve result from cache if available
        return self.store.get(query)

    def set(self, query, result):
        # Cache the query result
        self.store[query] = result
