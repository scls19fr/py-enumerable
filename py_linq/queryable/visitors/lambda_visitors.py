import ast


class SqlLambdaTranslator(ast.NodeVisitor):

    def visit_Eq(self, node):
        node.sql = u"="

    def visit_LtE(self, node):
        node.sql = u"<="

    def visit_GtE(self, node):
        node.sql = u">="

    def visit_Gt(self, node):
        node.sql = u">"

    def visit_Lt(self, node):
        node.sql = u"<"

    def visit_Add(self, node):
        node.sql = u"+"

    def visit_Sub(self, node):
        node.sql = u"-"

    def visit_Div(self, node):
        node.sql = u"/"

    def visit_Mult(self, node):
        node.sql = u"*"

    def visit_Num(self, node):
        node.sql = u"{0}".format(node.n)

    def visit_Str(self, node):
        node.sql = unicode(node.s)

    def visit_unicode(self, node):
        node.sql = node
