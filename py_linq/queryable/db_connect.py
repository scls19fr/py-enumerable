__author__ = 'ViraLogic Software'

import abc
import sqlite3


class DbConnectionBase(object):
    """
    Abstract database provider implementation. Assumes PEP 249 standard DB-API driver is used.
    """
    __metaclass__ = abc.ABCMeta
    _conn_uri = None
    _host = None
    _user = None
    _pwd = None
    _db_uri = None
    _conn = None

    def __init__(self, connection_uri):
        """
        Default constructor
        :param connection_uri: uri for database, similar in form to sqlalchemy
        (http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html)
        :return: void
        """
        self._conn_uri = connection_uri
        self.parse_uri()

    @property
    def connection_uri(self):
        return self._conn_uri

    @property
    def host(self):
        return self._host

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._pwd

    @property
    def database_uri(self):
        return self._db_uri

    @property
    def provider_name(self):
        try:
            return self.__dict__['__provider_name__']
        except KeyError:
            return None

    @abc.abstractproperty
    def driver(self):
        """
        Returns the provider determined by connection string
        :return: provider object
        """
        return NotImplementedError()

    @abc.abstractmethod
    def parse_uri(self):
        """
        Parses the connection uri to set host, user, password, and database uri
        :return: void
        """
        raise NotImplementedError()

    @abc.abstractproperty
    def connection(self):
        """
        Opens the connection to the database
        :return: connection object
        """
        return NotImplementedError()


class SqliteDbConnection(DbConnectionBase):
    __provider_name__ = 'sqlite'

    def __init__(self, connection_uri):
        super(SqliteDbConnection, self).__init__(connection_uri)

    @property
    def driver(self):
        return sqlite3

    @property
    def connection(self):
        if self._conn is None:
            self._conn = self.driver.connect(self.database_uri)
        return self._conn

    def parse_uri(self):
        self._host = self._user = self._pwd = ''
        self._db_uri = self.connection_uri.split(':')[1]
