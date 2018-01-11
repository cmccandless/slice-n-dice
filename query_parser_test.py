import unittest
from ddt import ddt, data, unpack
import re

from query_parser import parse


rgxNames = [
    (re.compile(p), r) for p, r in [
        ('#(\w+)', r'\1 defd'),
        ('"([^"]*)"', r'quo \1 equo'),
        ('\(([^"]*)\)', r'paren \1 eparen'),
    ]
]


def clean_name(name):
    for find, repl in [
        ('>=', ' GTE '),
        ('<=', ' LTE '),
        ('!=', ' NEQ '),
        ('=', ' EQ ',),
        ('>', ' GT '),
        ('<', ' LT '),
        ('&&', ' AND '),
        ('||', ' OR '),
        ('!', 'NOT '),
    ]:
        name = name.replace(find, repl)
    for rgx, repl in rgxNames:
        name = rgx.sub(repl, name)
    return name


class AnnotatedList(list):
    def __init__(self, args):
        list.__init__(self, args)
        name = '{} evaluates to {}'.format(
            *[clean_name(repr(x)) for x in args]
        )
        setattr(self, '__name__', name)

    def __repr__(self):
        return self.__name__


@ddt
class ParserTest(unittest.TestCase):
    def assertTrue(self, query, vars={}):
        self.assertIs(parse(query, vars), True)

    def assertFalse(self, query, vars={}):
        self.assertIs(parse(query, vars), False)

    def assertEqual(self, query, expected, vars={}):
        unittest.TestCase.assertEqual(
            self,
            parse(query, vars),
            expected
        )

    def assertIsNone(self, query, vars={}):
        self.assertIs(parse(query, vars), None)

    @data(*[AnnotatedList(x) for x in [
        ('3', 3),
        ('"test"', 'test'),
        ('[1,2,3]', [1, 2, 3]),
        ('["a", "b", "c"]', ['a', 'b', 'c']),
        ('a', 1, {'a': 1}),
    ]])
    @unpack
    def test_atom(self, query, expected, vars={}):
        self.assertEqual(query, expected, vars)

    def test_atom_true(self):
        self.assertTrue('true')

    def test_atom_false(self):
        self.assertFalse('false')

    def test_atom_null(self):
        self.assertIsNone('null')

    def test_number_cannot_be_float(self):
        with self.assertRaises(ValueError):
            parse('3.2')

    @data(*[AnnotatedList(x) for x in [
        # defined
        ('#a', True, {'a': 1}),
        ('#a', False),

        # eq
        ('3=3', True),
        ('3=4', False),
        ('"a"="a"', True),
        ('"a"="b"', False),
        ('true=true', True),
        ('false=false', True),
        ('null=null', True),
        ('true=false', False),
        ('true=null', False),
        ('false=null', False),
        ('[1,2,3]=[1,2,3]', True),
        ('[1,2,3]=[1,2,3,4]', False),
        ('3="3"', False),
        ('a=2', True, {'a': 2}),
        ('a=2', False, {'a': 3}),
        ('a="str"', True, {'a': "str"}),
        ('a="str"', False, {'a': "str2"}),
        ('a=[1,2,3]', True, {'a': [1, 2, 3]}),
        ('a=[1,2,3]', False, {'a': [1, 2, 3, 4]}),

        # neq
        ('3!=3', False),
        ('3!=4', True),
        ('"a"!="a"', False),
        ('"a"!="b"', True),
        ('true!=true', False),
        ('false!=false', False),
        ('null!=null', False),
        ('true!=false', True),
        ('true!=null', True),
        ('false!=null', True),
        ('[1,2,3]!=[1,2,3]', False),
        ('[1,2,3]!=[1,2,3,4]', True),
        ('3!="3"', True),
        ('a!=2', False, {'a': 2}),
        ('a!=2', True, {'a': 3}),
        ('a!="str"', False, {'a': "str"}),
        ('a!="str"', True, {'a': "str2"}),
        ('a!=[1,2,3]', False, {'a': [1, 2, 3]}),
        ('a!=[1,2,3]', True, {'a': [1, 2, 3, 4]}),

        # gt
        ('3>2', True),
        ('3>3', False),
        ('3>4', False),
        ('"abc">"aaa"', True),
        ('"abc">"abc"', False),
        ('"abc">"bbb"', False),
        ('a>2', True, {'a': 3}),
        ('a>3', False, {'a': 3}),
        ('a>4', False, {'a': 3}),
        ('a>"aaa"', True, {'a': "abc"}),
        ('a>"abc"', False, {'a': "abc"}),
        ('a>"bbb"', False, {'a': "abc"}),
        ('a>b', True, {'a': "abc", 'b': "aaa"}),
        ('a>b', False, {'a': "abc", 'b': "abc"}),
        ('a>b', False, {'a': "abc", 'b': "bbb"}),

        # gte
        ('3>=2', True),
        ('3>=3', True),
        ('3>=4', False),
        ('"abc">="aaa"', True),
        ('"abc">="abc"', True),
        ('"abc">="bbb"', False),
        ('a>=2', True, {'a': 3}),
        ('a>=3', True, {'a': 3}),
        ('a>=4', False, {'a': 3}),
        ('a>="aaa"', True, {'a': "abc"}),
        ('a>="abc"', True, {'a': "abc"}),
        ('a>="bbb"', False, {'a': "abc"}),
        ('a>=b', True, {'a': "abc", 'b': "aaa"}),
        ('a>=b', True, {'a': "abc", 'b': "abc"}),
        ('a>=b', False, {'a': "abc", 'b': "bbb"}),

        # lt
        ('3<4', True),
        ('3<3', False),
        ('3<2', False),
        ('"abc"<"bbb"', True),
        ('"abc"<"abc"', False),
        ('"abc"<"aaa"', False),
        ('a<4', True, {'a': 3}),
        ('a<3', False, {'a': 3}),
        ('a<2', False, {'a': 3}),
        ('a<"bbb"', True, {'a': "abc"}),
        ('a<"abc"', False, {'a': "abc"}),
        ('a<"aaa"', False, {'a': "abc"}),
        ('a<b', True, {'a': "abc", 'b': "bbb"}),
        ('a<b', False, {'a': "abc", 'b': "abc"}),
        ('a<b', False, {'a': "abc", 'b': "aaa"}),

        # lte
        ('3<=4', True),
        ('3<=3', True),
        ('3<=2', False),
        ('"abc"<="bbb"', True),
        ('"abc"<="abc"', True),
        ('"abc"<="aaa"', False),
        ('a<=4', True, {'a': 3}),
        ('a<=3', True, {'a': 3}),
        ('a<=2', False, {'a': 3}),
        ('a<="bbb"', True, {'a': "abc"}),
        ('a<="abc"', True, {'a': "abc"}),
        ('a<="aaa"', False, {'a': "abc"}),
        ('a<=b', True, {'a': "abc", 'b': "bbb"}),
        ('a<=b', True, {'a': "abc", 'b': "abc"}),
        ('a<=b', False, {'a': "abc", 'b': "aaa"}),

        # parenthesis
        ('(3=3)', True),
        ('3=3=true', False),  # control case

        # not
        ('not true', False),
        ('not false', True),
        ('!true', False),
        ('!false', True),
        ('!3', False),

        # and
        ('true and true', True),
        ('true and false', False),
        ('false and true', False),
        ('false and false', False),
        ('a and b', True, {'a': True, 'b': True}),
        ('true&&true', True),

        # or
        ('true or true', True),
        ('true or false', True),
        ('false or true', True),
        ('false or false', False),
        ('a or b', True, {'a': True, 'b': True}),
        ('a or b', True, {'a': False, 'b': True}),
        ('true||true', True),

        # contains
        ('[1, 2, 3] contains 1', True),
        ('[] contains 1', False),
        ('[1, 2, 3] has 1', True),
    ]])
    @unpack
    def test_evaluate(self, query, expected=True, vars={}):
        """{} evaluates to {}"""
        self.assertIs(parse(query, vars), expected)


if __name__ == '__main__':
    unittest.main()
