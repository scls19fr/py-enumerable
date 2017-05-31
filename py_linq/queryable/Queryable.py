
class Queryable(object):
    def __init__(self, expression, query_provider):
        self.__expressions = [expression]
        self.__provider = query_provider

    @property
    def provider(self):
        return self.__provider

    @property
    def sql(self):
        sql = []
        for ast in self.__expressions:
            sql.append(ast.visit(self.provider.provider_visitor).value)
        result = " ".join(sql)
        return result




