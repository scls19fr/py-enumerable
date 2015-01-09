__author__ = 'ViraLogic Software'

import abc
import sqlite3
from py_linq.exceptions import NullArgumentError, InvalidArgumentError


class DbConnectionBase(object):
    __metaclass__ = abc.ABCMeta
    _conn_uri = None
    _host = None
    _user = None
    _pwd = None
    _db_uri = None

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

    @abc.abstractproperty
    def provider(self):
        """
        Returns the provider determined by connection string
        :return: provider object
        """
        return

    @abc.abstractmethod
    def parse_uri(self):
        """
        Parses the connection uri to set host, user, password, and database uri
        :return: void
        """
        if self.connection_uri is None:
            raise NullArgumentError("No connection uri")
        if not ':' in self.connection_uri or len(self.connection_uri.split(':')) == 2:
            raise InvalidArgumentError("{0} is not a valid connection uri".format(self.connection_uri))
        return

    @abc.abstractproperty
    def connection(self):
        """
        The connection to the database
        :return: connection object
        """
        return

class SqliteDbConnection(DbConnectionBase):
    @property
    def provider(self):
        return sqlite3

    @property
    def connection(self):
        return self.provider.connect(self.database_uri)

    def parse_uri(self):
        super(SqliteDbConnection, self).parse_uri()
        self._host = self._user = self._pwd = ''
        self._db_uri = self.connection_uri.split(':')[1]
