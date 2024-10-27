# Replace with a library appropriate to your graph DB
from neo4j import GraphDatabase


class GraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_node(self, label, properties):
        with self.driver.session() as session:
            session.write_transaction(self._add_node, label, properties)

    @staticmethod
    def _add_node(tx, label, properties):
        query = f"CREATE (n:{label} {{ {', '.join(f'{k}: ${k}' for k in properties)} }})"
        tx.run(query, **properties)

    def find_node(self, label, property_key, property_value):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_node, label, property_key, property_value)
        return result

    @staticmethod
    def _find_node(tx, label, property_key, property_value):
        query = f"MATCH (n:{label} {{ {property_key}: $value }}) RETURN n"
        return tx.run(query, value=property_value).data()
