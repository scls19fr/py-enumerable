__author__ = 'ViraLogic Software'

import abc
import sqlite3
from decimal import Decimal
from .parsers import SqliteUriParser
from .entity.model import Model
from ..exceptions import InvalidArgumentError


class DbConnectionBase(object):
    """
    Abstract database provider implementation. Assumes PEP 249 standard DB-API driver is used.
    """
    __metaclass__ = abc.ABCMeta
    _conn = None
    _provider_config = None

    def __init__(self, connection_uri):
        """
        Default constructor
        :param connection_uri: uri for database, similar in form to sqlalchemy
        (http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html)
        :return: void
        """
        self.connection_uri = connection_uri

    @property
    def provider_config(self):
        """
        Returns the provider config property
        :return: ProviderConfig instance
        """
        if self._provider_config is None:
            raise AttributeError("Provider not configured")
        return self._provider_config

    @property
    def provider_name(self):
        try:
            return getattr(self, '__provider_name__')
        except KeyError:
            raise KeyError("No __provider_name__ attribute found")

    @abc.abstractproperty
    def driver(self):
        """
        Returns the provider determined by connection string
        :return: provider object
        """
        return NotImplementedError()

    @abc.abstractproperty
    def connection(self):
        """
        Opens the connection to the database
        :return: connection object
        """
        return NotImplementedError()

    @abc.abstractproperty
    def provider_data_types(self):
        """
        Gets a mapping of Python type to its representation in the database
        :return: dictionary of <python type, database type mapping>
        """
        return NotImplementedError()

    @abc.abstractmethod
    def create_table(self, model):
        """
        Generates SQL statement to create a table given a data model
        :param model: An child of a py_linq.queryable.entity.model.Model
        :return: sql statement as text
        """
        return NotImplementedError()



class SqliteDbConnection(DbConnectionBase):
    __provider_name__ = u'sqlite'  # This attribute is used as a hook for the ConnectionManager to find it

    def __init__(self, connection_uri):
        super(SqliteDbConnection, self).__init__(connection_uri)
        self._provider_config = SqliteUriParser(connection_uri).parse_uri()

    @property
    def driver(self):
        return sqlite3

    @property
    def connection(self):
        if self._conn is None:
            self._conn = self.driver.connect(self.provider_config.db_uri)
        return self._conn

    @property
    def provider_data_types(self):
        return {
            int: 'INTEGER',
            unicode: 'TEXT',
            float: 'REAL',
            Decimal: 'NUMERIC',
            bytes: 'BLOB'
        }

    def create_table(self, model):
        return NotImplementedError()
