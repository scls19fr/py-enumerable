__author__ = 'ViraLogic Software'

import inspect
import db_connect
from db_connect import *

class ConnectionManager(object):
    """
    ConnectionManager is used to dynamically determine which database connection to use based on connection string
    """
    @staticmethod
    def find_connections():
        """
        Gets a 'provider_name': connection class dictionary of all possible db connection classes
        :return: dict object
        """
        connections = [cls for name, cls in inspect.getmembers(db_connect) if inspect.isclass(cls) and issubclass(IDbConnection)]
        result = {}
        for cls in connections:
            result.setdefault(getattr(cls, '__provider__'), cls)
        return result

    @staticmethod
    def get_connection(self, connection_string):
        """
        Gets the appropriate connection
        :param connection_string: connection string
        :return: connection object
        """
        base_conn = DbConnectionBase(connection_string)
        provider_name = base_conn.provider_name

