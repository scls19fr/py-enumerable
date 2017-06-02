from ..expressions.tree import ExpressionTree


class Queryable(object):
    def __init__(self, expression, query_provider):
        self.__expression_tree = ExpressionTree()
        self.__expression_tree.add_expression(expression)
        self.__provider = query_provider

    @property
    def provider(self):
        return self.__provider

    @property
    def sql(self):
        sql = []
        for ast in self.__expression_tree:
            sql.append(ast.visit(self.provider.provider_visitor).value)
        result = " ".join(sql)
        return result






