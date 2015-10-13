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
            int: u'INTEGER',
            unicode: u'TEXT',
            float: u'REAL',
            Decimal: u'NUMERIC',
            bytes: u'BLOB'
        }

    def create_table(self, model):
        try:
            columns = model.inspect_columns()
        except:
            raise InvalidArgumentError("Does not appear to be a proper data model that inherits from Model")
        sql = u"CREATE TABLE {0} ([COLUMNS]);".format(model.table_name())
        columns_sql = u", ".join([self._generate_col_sql(col[0], col[1]) for col in columns])
        sql = sql.replace(u"[COLUMNS]", columns_sql)
        #TODO: Add indexing for unique columns here
        return sql

    def _generate_col_sql(self, column_name, column):
        """
        :param provider: A DbConnectionBase type
        :return: SQL statement for column as text
        """
        try:
            column_type = self.provider_data_types[column.column_type]
        except KeyError:
            raise KeyError(u"{0} is not a valid column data type".format(column_type))
        sql = u"{0} {1}".format(column_name, column_type)
        sql = u"{0} NULL".format(sql) if column.is_nullable else u"{0} NOT NULL".format(sql)
        if column.is_primary_key:
            sql = u"{0} PRIMARY KEY".format(sql)
        if column.is_unique and not column.is_primary_key:
            sql = u"{0} UNIQUE".format(sql)
        #TODO: Add foreign key syntax here
        if column.foreign_key is not None:
            #print column.foreign_key
            #print column.foreign_column
            sql = u"{0}, FOREIGN KEY({1}) REFERENCES {2}({3})".format(sql, column_name, column.foreign_key.table_name(), column.foreign_column.column_name)
        return sql
