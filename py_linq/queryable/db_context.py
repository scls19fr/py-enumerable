__author__ = 'ViraLogic Software'

from py_linq.queryable import ConnectionManager

class DbContext(object):
    """
    Base class used to handle database context. Application DbContext should inherit from this class
    """

    def __init__(self, connection_uri, provider=None):
        self.provider = provider if provider is not None else ConnectionManager.get_connection(connection_uri)
        self.connection = self.provider.connection()
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def execute(self, sql, parameters=()):
        """
        Constructs a prepared SQL statement and sends to database
        :param sql: sql statement as string
        :param parameters: tuple of values to substitute into sql string
        :return: result from database as cursor object
        """
        return self.cursor.execute(sql, parameters)

    def save_changes(self):
        """
        Commits transaction to database
        :return: void
        """
        return self.connection.commit()







