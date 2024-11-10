# Replace with a library appropriate to your graph DB
from neo4j import GraphDatabase


class GraphDB:
    """
    A class for interacting with a Neo4j graph database.

    Parameters
    ----------
    uri : str
        The URI of the Neo4j database.
    user : str
        The username for authentication.
    password : str
        The password for authentication.

    Attributes
    ----------
    driver : neo4j.Driver
        The Neo4j driver instance for managing database connections.
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Close the connection to the Neo4j database.

        Returns
        -------
        None
        """
        self.driver.close()

    def write_data(self, query: str, parameters: dict = None):
        """
        Execute a write query on the Neo4j database.

        Parameters
        ----------
        query : str
            The Cypher query to execute.
        parameters : dict, optional
            A dictionary of parameters to pass with the query.

        Returns
        -------
        None
        """
        with self.driver.session() as session:
            session.write_transaction(self._execute_query, query, parameters)

    def read_data(self, query: str, parameters: dict = None) -> list:
        """
        Execute a read query on the Neo4j database and return the results.

        Parameters
        ----------
        query : str
            The Cypher query to execute.
        parameters : dict, optional
            A dictionary of parameters to pass with the query.

        Returns
        -------
        list
            A list of records returned by the query.
        """
        with self.driver.session() as session:
            result = session.read_transaction(
                self._execute_query, query, parameters)
            return list(result)

    @staticmethod
    def _execute_query(tx, query: str, parameters: dict = None):
        """
        Helper method to execute a query within a transaction.

        Parameters
        ----------
        tx : neo4j.Transaction
            The transaction object.
        query : str
            The Cypher query to execute.
        parameters : dict, optional
            A dictionary of parameters to pass with the query.

        Returns
        -------
        neo4j.Result
            The result of the query execution.
        """
        return tx.run(query, parameters)
