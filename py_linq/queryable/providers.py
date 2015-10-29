__author__ = 'ViraLogic Software'

import abc
import sqlite3
from decimal import Decimal
from .parsers import SqliteUriParser
from .entity.proxy import DynamicModelProxy
from ..exceptions import InvalidArgumentError, NullArgumentError


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
    def save_changes(self):
        """
        Commits the changes to the database
        :return: void
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

    @abc.abstractmethod
    def create_indexes(self, model):
        """
        Executes command to create indexes on all unique columns in a data model
        :param model: A child of py_linq.queryable.entity.model.Model
        :return: void
        """
        return NotImplementedError()

    @abc.abstractmethod
    def query(self, model):
        """
        Generates SQL statement to query a table given an expression model
        :param model: an expression model
        :return: sql statement as text
        """
        return NotImplementedError()

    @abc.abstractmethod
    def update(self, model):
        """
        Executes command to update a table given a data model
        :param model: A proxy class of a py_linq.queryable.entity.model.Model child where the columns hold values
        :return: sql statement as text
        """
        return NotImplementedError()

    @abc.abstractmethod
    def add(self, proxy_instance):
        """
        Executes command to add a record to a given table given a data model
        :param proxy_instance: A proxy class of a py_linq.queryable.entity.model.Model child where the columns hold values
        :return: primary key
        """
        return NotImplementedError()

    @abc.abstractmethod
    def remove(self, proxy_instance):
        """
        Executes command to delete a record from a given table
        :param proxy_instance: A proxy class of a py_linq.queryable.entity.model.Model child where the columns hold values
        :return: void
        """

    def is_valid_proxy_instance(self, instance):
        return isinstance(instance, DynamicModelProxy)



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

    def save_changes(self):
        try:
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            raise ex

    def create_table(self, model):
        try:
            columns = model.inspect_columns()
        except:
            raise InvalidArgumentError(u"Does not appear to be a proper data model that inherits from Model")
        primary_keys = filter(lambda c: c[1].is_primary_key, columns)
        if len(primary_keys) != 1:
            raise InvalidArgumentError(u"{0} appears to have incorrect number of primary key declared: {1}".format(model.table_name(), len(primary_keys)))
        sql = u"CREATE TABLE {table_name} ({columns})"
        columns_sql = u", ".join([self._generate_col_sql(col[0], col[1]) for col in columns])
        sql = sql.format(
            table_name=model.table_name(),
            columns=columns_sql
        )
        self.connection.execute(sql)

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
        if column.foreign_key is not None:
            sql = u"{0}, FOREIGN KEY({1}) REFERENCES {2}({3})".format(sql, column_name, column.foreign_key.table_name(), column.foreign_column.column_name)
        return sql

    def create_indexes(self, model):
        try:
            unique_columns = filter(lambda c: c[1].is_unique, model.inspect_columns())
        except:
            raise InvalidArgumentError(u"Does not appear to be a proper data model that inherits from Model")
        for column_name, column in unique_columns:
            index_name = u"{0}_index".format(column_name)
            sql = u"CREATE INDEX {0} ON {1}({2});".format(index_name, model.table_name(), column_name)
            self.connection.execute(sql)

    def query(self, model):
        raise NotImplementedError()

    def update(self, model):
        raise NotImplementedError()

    def add(self, proxy_instance):
        if not self.is_valid_proxy_instance(proxy_instance):
            raise InvalidArgumentError(u"Trying to add model that is not a DynamicModelProxy")

        columns = []
        column_values = []
        for k,v in filter(lambda c: not c[1].column.is_primary_key or (c[1].column.is_primary_key and c[1].column.column_type != int), proxy_instance.columns.iteritems()):
            columns.append(proxy_instance.column_name(k))
            if v.column.column_type == unicode:
                if v.value is None or len(v.value) == 0:
                    column_values.append(u"NULL")
                else:
                    column_values.append(u"'{0}'".format(v.value.replace("'", "''")))
            else:
                column_values.append(unicode(v.value) if v.value is not None else "NULL")

        if len(columns) > 0:
            sql = u"INSERT INTO {table_name}({columns}) VALUES({column_values});".format(
                table_name=proxy_instance.model.table_name(),
                columns=', '.join(columns),
                column_values=', '.join(column_values)
            )
        else:
            sql = u"INSERT INTO {table_name} VALUES(NULL);".format(
                table_name=proxy_instance.model.table_name()
            )

        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.lastrowid

    def remove(self, proxy_instance):
        if not self.is_valid_proxy_instance(proxy_instance):
            raise InvalidArgumentError(u"Trying to delete a model that is not a DynamicModelProxy")
        primary_key = filter(lambda (k,v): v.column.is_primary_key, proxy_instance.columns.iteritems())
        if len(primary_key) != 1:
            raise InvalidArgumentError(u"There can only be 1 primary key associated with {0}".format(proxy_instance.model.table_name()))
        sql = u"DELETE FROM {table_name} WHERE {primary_name} = {primary_value};"
        primary_name = proxy_instance.column_name(primary_key[0][0])
        primary_value = primary_key[0][1].value
        if primary_key[0][1].column.column_type == unicode:
            if primary_value is None or len(primary_value) == 0:
                raise NullArgumentError(u"Primary key column {0} must have value".format(primary_name))
            primary_value = u"'{0}'".format(primary_value.replace("'", "''"))
        sql = sql.format(
            table_name = proxy_instance.model.table_name(),
            primary_name = primary_name,
            primary_value = primary_value
        )
        print sql
        self.connection.execute(sql)




