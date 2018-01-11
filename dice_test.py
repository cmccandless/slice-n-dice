import unittest

from dice import dice


# Data adapted from https://github.com/exercism/python/blob/master/config.json
data = [
    {
        "uuid": "f458c48a-4a05-4809-9168-8edd55179349",
        "slug": "hello-world",
        "core": False,
        "unlocked_by": None,
        "difficulty": 2,
        "topics": [
            "conditionals",
            "optional_values",
            "text_formatting"
        ]
    },
    {
        "uuid": "b6acda85-5f62-4d9c-bb4f-42b7a360355a",
        "slug": "leap",
        "core": False,
        "unlocked_by": None,
        "difficulty": 1,
        "topics": [
            "conditionals",
            "booleans",
            "logic"
        ]
    },
    {
        "uuid": "d39f86fe-db56-461c-8a93-d87058af8366",
        "slug": "reverse-string",
        "core": False,
        "unlocked_by": None,
        "difficulty": 8,
        "topics": [
            "strings"
        ]
    },
    {
        "uuid": "d1a98c79-d3cc-4035-baab-0e334d2b6a57",
        "slug": "isogram",
        "core": False,
        "unlocked_by": None,
        "difficulty": 4,
        "topics": [
            "conditionals",
            "loops",
            "strings",
            "algorithms"
        ]
    },
    {
        "uuid": "bebf7ae6-1c35-48bc-926b-e053a975eb10",
        "slug": "pangram",
        "core": False,
        "unlocked_by": None,
        "difficulty": 4,
        "topics": [
            "loops",
            "conditionals",
            "strings",
            "algorithms",
            "filtering",
            "logic"
        ]
    },
    {
        "uuid": "dc2917d5-aaa9-43d9-b9f4-a32919fdbe18",
        "slug": "word-search",
        "core": False,
        "unlocked_by": None,
        "difficulty": 6,
        "topics": [
            "strings",
            "searching"
        ]
    },
    {
        "uuid": "af50bb9a-e400-49ce-966f-016c31720be1",
        "slug": "wordy",
        "core": False,
        "unlocked_by": None,
        "difficulty": 8,
        "topics": [
            "logic",
            "pattern_matching",
            "mathematics",
        ]
    },
]

select_data = {
    'title': 'My title',
    'author': 'jdoe',
    'comments': [
        {
            'author': 'jqpublic',
            'body': 'Good stuff!',
            'votes': 10,
            'month': 10
        },
        {
            'author': 'jqpublic',
            'body': 'More good stuff!',
            'votes': 90,
            'month': 8
        },
        {
            'author': 'tjones',
            'body': 'Not again.',
            'votes': 90,
            'month': 7
        },
    ]
}


class TestDice(unittest.TestCase):
    # def setUp(self):
    #     self.maxDiff = 1300

    def test_single_key(self):
        schema = {
            "keys": ["slug"]
        }
        expected = [
            'hello-world',
            'leap',
            'reverse-string',
            'isogram',
            'pangram',
            'word-search',
            'wordy'
        ]
        self.assertEqual(dice(data, schema), expected)

    def test_multiple_keys(self):
        schema = {
            "keys": ['slug', 'difficulty']
        }
        expected = [
            {'slug': 'hello-world', 'difficulty': 2},
            {'slug': 'leap', 'difficulty': 1},
            {'slug': 'reverse-string', 'difficulty': 8},
            {'slug': 'isogram', 'difficulty': 4},
            {'slug': 'pangram', 'difficulty': 4},
            {'slug': 'word-search', 'difficulty': 6},
            {'slug': 'wordy', 'difficulty': 8}
        ]
        self.assertEqual(dice(data, schema), expected)

    def test_single_sort_key(self):
        schema = {
            "keys": ['slug'],
            "sort": ["difficulty"]
        }
        expected = [
            'leap',
            'hello-world',
            'isogram',
            'pangram',
            'word-search',
            'reverse-string',
            'wordy'
        ]
        self.assertEqual(dice(data, schema), expected)

    def test_reverse_sort(self):
        schema = {
            "keys": ['slug'],
            "sort": ["-difficulty"]
        }
        expected = [
            'reverse-string',
            'wordy',
            'word-search',
            'isogram',
            'pangram',
            'hello-world',
            'leap',
        ]
        self.assertEqual(dice(data, schema), expected)

    def test_multiple_sort_keys(self):
        schema = {
            "keys": ['slug'],
            "sort": ["difficulty", '-slug']
        }
        expected = [
            'leap',
            'hello-world',
            'pangram',
            'isogram',
            'word-search',
            'wordy',
            'reverse-string',
        ]
        self.assertEqual(dice(data, schema), expected)

    def test_simple_groupby(self):
        schema = {
            "groupby": {
                "gkey": "difficulty",
                "keys": ['slug']
            }
        }
        expected = {
            1: ["leap"],
            2: ['hello-world'],
            4: ['isogram', 'pangram'],
            6: ['word-search'],
            8: ['reverse-string', 'wordy']
        }
        self.assertEqual(dice(data, schema), expected)

    def test_groupby_list_key(self):
        schema = {
            "groupby": {
                "gkey": "topics",
                "list_key": True,
                'keys': ['slug']
            }
        }
        expected = {
            "algorithms": [
                'isogram',
                'pangram',
            ],
            "booleans": [
                'leap',
            ],
            "conditionals": [
                'hello-world',
                'leap',
                'isogram',
                'pangram',
            ],
            "filtering": [
                'pangram',
            ],
            "logic": [
                'leap',
                'pangram',
                'wordy',
            ],
            "loops": [
                'isogram',
                'pangram',
            ],
            "mathematics": [
                'wordy',
            ],
            "optional_values": [
                'hello-world',
            ],
            "pattern_matching": [
                'wordy',
            ],
            "searching": [
                'word-search',
            ],
            "strings": [
                'reverse-string',
                'isogram',
                'pangram',
                'word-search',
            ],
            "text_formatting": [
                'hello-world',
            ],
        }
        self.assertEqual(dice(data, schema), expected)

    def test_sort_in_groupby(self):
        schema = {
            "groupby": {
                "gkey": 'difficulty',
                'keys': ['slug'],
                'sort': ['-slug']
            }
        }
        expected = {
            1: ["leap"],
            2: ['hello-world'],
            4: ['pangram', 'isogram'],
            6: ['word-search'],
            8: ['wordy', 'reverse-string']
        }
        self.assertEqual(dice(data, schema), expected)

    def test_nested_groupby(self):
        schema = {
            'groupby': {
                'gkey': 'difficulty',
                'groupby': {
                    'gkey': 'topics',
                    'list_key': True,
                    'keys': ['slug']
                }
            }
        }
        expected = {
            1: {

                "conditionals": ['leap'],
                "booleans": ['leap'],
                "logic": ['leap'],
            },
            2: {
                "conditionals": ['hello-world'],
                "optional_values": ['hello-world'],
                "text_formatting": ['hello-world'],
            },
            4: {
                "algorithms": ['isogram', 'pangram'],
                "conditionals": ['isogram', 'pangram'],
                "filtering": ['pangram'],
                "logic": ['pangram'],
                "loops": ['isogram', 'pangram'],
                "strings": ['isogram', 'pangram'],
            },
            6: {
                "strings": ['word-search'],
                "searching": ['word-search'],
            },
            8: {
                "logic": ['wordy'],
                "mathematics": ['wordy'],
                "pattern_matching": ['wordy'],
                "strings": ['reverse-string'],
            },
        }
        self.assertEqual(dice(data, schema), expected)

    def test_unknown_gkey(self):
        schema = {
            'groupby': {
                'gkey': 'submissions'
            }
        }
        with self.assertRaises(KeyError):
            dice(data, schema)

    def test_select(self):
        schema = {
            'select': {
                'skey': 'comments'
            }
        }
        expected = [
            {
                'author': 'jqpublic',
                'body': 'Good stuff!',
                'votes': 10,
                'month': 10
            },
            {
                'author': 'jqpublic',
                'body': 'More good stuff!',
                'votes': 90,
                'month': 8
            },
            {
                'author': 'tjones',
                'body': 'Not again.',
                'votes': 90,
                'month': 7
            },
        ]
        self.assertEqual(dice(select_data, schema), expected)

    def test_select_sort(self):
        schema = {
            'select': {
                'skey': 'comments',
                'sort': ['-votes', 'month'],
            }
        }
        expected = [
            {
                'author': 'tjones',
                'body': 'Not again.',
                'votes': 90,
                'month': 7
            },
            {
                'author': 'jqpublic',
                'body': 'More good stuff!',
                'votes': 90,
                'month': 8
            },
            {
                'author': 'jqpublic',
                'body': 'Good stuff!',
                'votes': 10,
                'month': 10
            },
        ]
        self.assertEqual(dice(select_data, schema), expected)

    def test_select_groupby(self):
        schema = {
            'select': {
                'skey': 'comments',
                'groupby': {
                    'gkey': 'votes',
                    'groupby': {
                        'gkey': 'author',
                    }
                }
            }
        }
        expected = {
            10: {
                'jqpublic': [
                    {
                        'author': 'jqpublic',
                        'body': 'Good stuff!',
                        'votes': 10,
                        'month': 10
                    },
                ]
            },
            90: {
                'tjones': [
                    {
                        'author': 'tjones',
                        'body': 'Not again.',
                        'votes': 90,
                        'month': 7
                    },
                ],
                'jqpublic': [
                    {
                        'author': 'jqpublic',
                        'body': 'More good stuff!',
                        'votes': 90,
                        'month': 8
                    },
                ]
            }
        }
        self.assertEqual(dice(select_data, schema), expected)

    def test_nested_select(self):
        schema = {
            'select': {
                'skey': 'article',
                'select': {
                    'skey': 'comments'
                }
            }
        }
        article = {
            'article': select_data
        }
        expected = [
            {
                'author': 'jqpublic',
                'body': 'Good stuff!',
                'votes': 10,
                'month': 10
            },
            {
                'author': 'jqpublic',
                'body': 'More good stuff!',
                'votes': 90,
                'month': 8
            },
            {
                'author': 'tjones',
                'body': 'Not again.',
                'votes': 90,
                'month': 7
            },
        ]
        self.assertEqual(dice(article, schema), expected)

    def test_error_select_on_list(self):
        schema = {
            'select': 'slug'
        }
        with self.assertRaises(TypeError):
            dice(data, schema)

    def test_error_non_select_on_dictionary(self):
        schema = {
            'keys': ['title', 'author']
        }
        with self.assertRaises(TypeError):
            dice(select_data, schema)

    def test_where_defined(self):
        schema = {
            'where': '#difficulty',
            'keys': ['slug']
        }
        filter_data = list(data)
        filter_data.append({
            'slug': 'no_difficulty'
        })
        expected = [
            'hello-world',
            'leap',
            'reverse-string',
            'isogram',
            'pangram',
            'word-search',
            'wordy'
        ]
        self.assertEqual(dice(filter_data, schema), expected)

    def test_where_gt(self):
        schema = {
            'where': 'difficulty>5',
            'keys': ['slug']
        }
        expected = [
            'reverse-string',
            'word-search',
            'wordy'
        ]
        self.assertEqual(dice(data, schema), expected)

    def test_where_contains(self):
        schema = {
            'where': 'topics has "strings"',
            'keys': ['slug']
        }
        expected = [
            'reverse-string',
            'isogram',
            'pangram',
            'word-search',
        ]
        self.assertEqual(dice(data, schema), expected)


if __name__ == '__main__':
    unittest.main()
