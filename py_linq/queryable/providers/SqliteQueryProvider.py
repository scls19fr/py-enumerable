from ..providers import IQueryProvider


class SqliteQueryProvider(IQueryProvider):

    def __init__(self, db_provider):
        self.__provider = db_provider

    @property
    def db_provider(self):
        return self.__provider

    @property
    def sql(self):
        raise NotImplementedError()

    def createQuery(self, expression):
        raise NotImplementedError()

    def execute(self, expression):
        self.visitor.visit(expression)
        expression.visit_children(self.visitor)
        cursor = self.db_provider.connection.cursor()
        cursor.execute(self.sql)
        return cursor
