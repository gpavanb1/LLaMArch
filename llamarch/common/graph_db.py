# Replace with a library appropriate to your graph DB
from neo4j import GraphDatabase


class GraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def write_data(self, query, parameters=None):
        with self.driver.session() as session:
            session.write_transaction(self._execute_query, query, parameters)

    def read_data(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._execute_query, query, parameters)
            return result

    @staticmethod
    def _execute_query(tx, query, parameters):
        return tx.run(query, parameters)
