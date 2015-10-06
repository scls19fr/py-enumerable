__author__ = 'Bruce.Fenske'

class Column(object):

    def __init__(self, column_type, column_name=None, foreign_key=None, is_primary_key=False, is_nullable=False, is_unique=False):
        self._column_name = unicode(column_name) if column_name is not None else None
        self._column_type = column_type
        self._foreign_key = foreign_key
        self._is_primary_key = is_primary_key
        self._is_nullable = is_nullable
        self._is_unique = is_unique

    @property
    def column_type(self):
        return self._column_type

    @property
    def column_name(self):
        if self._column_name is None or self._column_name == u'' or len(self._column_name) == 0:
            return None
        return self._column_name

    @property
    def has_foreign_key(self):
        return self._foreign_key != None

    @property
    def is_primary_key(self):
        return self._is_primary_key

    @property
    def is_nullable(self):
        return self._is_nullable

    @property
    def is_unique(self):
        return self._is_unique

    def generate_col_sql(self, provider, column_name):
        """
        :param provider: A DbConnectionBase type
        :return: SQL statement for column as text
        """
        try:
            column_type = provider.provider_data_types[self.column_type]
        except KeyError:
            raise KeyError(u"{0} is not a valid column data type".format(self.column_type))
        sql = u"{0} {1}".format(column_name, column_type)
        sql = u"{0} NULL".format(sql) if self.is_nullable else u"{0} NOT NULL".format(sql)
        if self.is_primary_key:
            sql = u"{0} PRIMARY KEY".format(sql)
        if self.is_unique and not self.is_primary_key:
            sql = u"{0} UNIQUE".format(sql)
        #TODO: Add foreign key syntax here
        return sql


class PrimaryKey(Column):
    def __init__(self, column_type, column_name):
        super(self, Column).__init__(column_type, column_name, foreign_key=False, is_primary_key=True, is_nullable=False, is_unique=False)
