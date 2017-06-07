from ..expressions.tree import ExpressionTree


class QueryOptimizer(object):
    def __init__(self, expression_tree):
        if not isinstance(expression_tree, ExpressionTree):
            raise Exception("QueryOptimizer Instantiation: arg is not an ExpressionTree instance")
        self.__expression_tree = expression_tree

    @property
    def expression_tree(self):
        return self.__expression_tree

    def optimize_tree(self):
        for node in self.expression_tree:
            while node.can_reduce(self.expression_tree.peek):
                self.expression_tree.remove_expression(self.expression_tree.peek)