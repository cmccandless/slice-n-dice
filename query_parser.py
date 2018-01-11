from lark import Lark, InlineTransformer

grammar = """
    ?start: expr

    ?expr: atom
        | "#" NAME              -> defined
        | "not" expr            -> bool_not
        | "!" atom              -> bool_not
        | "!(" expr ")"         -> bool_not
        | expr "=" expr         -> eq
        | expr "!=" expr        -> neq
        | expr ">" expr         -> gt
        | expr ">=" expr        -> gte
        | expr "<" expr         -> lt
        | expr "<=" expr        -> lte
        | expr "and" expr       -> bool_and
        | expr "&&" expr        -> bool_and
        | expr "or" expr        -> bool_or
        | expr "||" expr        -> bool_or
        | expr "contains" expr  -> contains
        | expr "has" expr       -> contains
        | "(" expr ")"

    ?atom: NUMBER               -> number
        | NAME                  -> var
        | "true"                -> true
        | "false"               -> false
        | "null"                -> null
        | string
        | array

    string: ESCAPED_STRING
    array: "[" [atom ("," atom)*] "]"

    %import common.ESCAPED_STRING
    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


class QueryTree(InlineTransformer):
    from operator import eq, lt, gt
    number = int

    def __init__(self, vars=None):
        if vars is None:
            vars = {}
        self.vars = vars

    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    def array(self, *args):
        return list(args)

    def true(self):
        return True

    def false(self):
        return False

    def null(self):
        return None

    def var(self, name):
        return self.vars[name]

    def defined(self, name):
        return name in self.vars

    def bool_not(self, value):
        return not value

    def neq(self, left, right):
        return not self.eq(left, right)

    def lte(self, left, right):
        return self.eq(left, right) or self.lt(left, right)

    def gte(self, left, right):
        return self.eq(left, right) or self.gt(left, right)

    def bool_and(self, left, right):
        return left and right

    def bool_or(self, left, right):
        return left or right

    def contains(self, left, right):
        return right in left


def parse(query_str, vars={}):
    return Lark(
        grammar,
        parser='lalr',
        transformer=QueryTree(vars)
    ).parse(query_str.lower())


def matches(data, query):
    return [e for e in data if parse(query, e) is True]
