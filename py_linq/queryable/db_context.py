__author__ = 'ViraLogic Software'

from py_linq.queryable import ConnectionManager

class DbContext(object):
    """
    Base class used to handle database context
    """
    _conn = None

    def __init__(self, connection_uri, provider=None):
        self.provider = provider if provider is not None else ConnectionManager.get_connection(connection_uri)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.provider.close()

    def execute(self, sql):
        """
        Sends sql statement to the provider
        :param sql: sql statement as string
        :return: result from database
        """
        return self.provider.execute(sql)







