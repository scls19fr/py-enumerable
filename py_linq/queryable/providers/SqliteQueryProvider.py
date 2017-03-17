from ..providers import IQueryProvider
from ..query.queryable import Queryable
from ..visitors.SqliteExpressionVisitor import SqliteExpressionVisitor


class SqliteQueryProvider(IQueryProvider):

    def __init__(self, db_provider):
        self.__visitor = SqliteExpressionVisitor()
        self.__provider = db_provider

    @property
    def visitor(self):
        return self.__visitor

    @property
    def db_provider(self):
        return self.__provider

    @property
    def sql(self):
        query = u"{0}{1}".format(self.__selects, self.__from)
        return u"{0};".format(query)

    def createQuery(self, expression):
        return Queryable(self, expression)

    def execute(self, expression):
        self.visitor.visit(expression)
        expression.visit_children(self.visitor)
        cursor = self.db_provider.connection.cursor()
        cursor.execute(self.sql)
        return cursor

    @property
    def __selects(self):
        if self.visitor.sql_expression_result.projection is None:
            raise Exception("Projection is None")
        selects = u", ".join(self.visitor.sql_expression_result.projection.value)
        return u"SELECT {0} ".format(selects)

    @property
    def __from(self):
        if not self.visitor.sql_expression_result.has_source_name:
            raise Exception("no source or table name found for expression")
        return u"FROM {0}".format(self.visitor.sql_expression_result.source)
