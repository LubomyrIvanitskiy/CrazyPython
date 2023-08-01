import json
import os

from domain_map import mapper, read_mapping


def test_handling_literal():
    data = {}

    mapping = {
        "version": "!literal 1.0.0",
        "count": 1
    }

    expected_result = {
        "version": "1.0.0",
        "count": 1
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_handling_optional():
    data = {}

    mapping = {
        "!optional version": "data.version",
        "count": 1
    }

    expected_result = {
        "count": 1
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_handling_path():
    data = {
        "user": {
            "name": "John Doe",
            "age": 30,
        }
    }

    mapping = {
        "name": "user.name",
        "age": "user.age"
    }

    expected_result = {
        "name": "John Doe",
        "age": 30,
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_accessing_list_element():
    data = {
        "users": [
            {
                "name": "John Doe",
                "age": 30,
            },
            {
                "name": "Jane Doe",
                "age": 25,
            }
        ]
    }

    mapping = {
        "user": {
            "name": "users[0].name",
            "age": "users[1].age"
        }
    }

    expected_result = {
        "user": {
            "name": "John Doe",
            "age": 25,
        }
    }
    assert mapper(data, mapping=mapping) == expected_result


def test_defining_list():
    data = {
        "users": [
            {
                "name": "John Doe",
                "age": 30,
            },
            {
                "name": "Jane Doe",
                "age": 25,
            }
        ]
    }

    mapping = {
        "users[i]": {
            "name": "users[i].name",
        }
    }

    expected_result = {
        "users": [
            {
                "name": "John Doe",
            },
            {
                "name": "Jane Doe",
            }
        ]
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_defining_nested_list():
    data = {
        "users": [
            {
                "name": "John Doe",
                "age": 30,
                "addresses": [
                    {
                        "city": "New York",
                        "country": "USA"
                    },
                    {
                        "city": "London",
                        "country": "UK"
                    }
                ]
            },
            {
                "name": "Jane Doe",
                "age": 25,
                "addresses": [
                    {
                        "city": "Paris",
                        "country": "France"
                    },
                    {
                        "city": "Berlin",
                        "country": "Germany"
                    }
                ]
            }
        ]
    }

    mapping = {
        "users[i]": {
            "name": "users[i].name",
            "cities[j]": "users[i].addresses[j].city"
        }
    }

    expected_result = {
        "users": [
            {
                "name": "John Doe",
                "cities": [
                    "New York",
                    "London"
                ]
            },
            {
                "name": "Jane Doe",
                "cities": [
                    "Paris",
                    "Berlin"
                ]
            }
        ]
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_multiindex():
    data = {
        "users": [
            {
                "name": "John Doe",
                "age": 30,
                "addresses": [
                    {
                        "city": "New York",
                        "country": "USA"
                    },
                    {
                        "city": "London",
                        "country": "UK"
                    }
                ]
            },
            {
                "name": "Jane Doe",
                "age": 25,
                "addresses": [
                    {
                        "city": "Paris",
                        "country": "France"
                    },
                    {
                        "city": "Berlin",
                        "country": "Germany"
                    }
                ]
            }
        ]
    }

    mapping = {
        "cities[i*j]": "users[i].addresses[j].city"
    }

    expected_result = {
        "cities": [
            "New York",
            "London",
            "Paris",
            "Berlin"
        ]
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_from_tag():
    data = {
        "user": {
            "name": "John Doe",
            "age": 30,
            "address": {
                "city": "New York",
                "country": "USA"
            }
        }
    }

    mapping = {
        "!from user": {
            "name": "name",
            "age": "age",
            "!from address": {
                "city": "city",
            }
        }
    }

    expected_result = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }

    assert mapper(data, mapping=mapping) == expected_result


def test_loading_from_simple_json():
    from trace_all import trace_on, trace_off
    try:
        trace_on()
        maps = read_mapping('simple_mapping.json')
        print(json.dumps(maps, indent=2))
        assert maps
        data = json.load(open("original_user_info.json"))
        result = mapper(data, mapping=maps, concat=lambda *args: ' '.join(args))
        print(json.dumps(result, indent=2))
        assert result
    finally:
        trace_off()

# def test_loading_from_simple_yaml():
#     maps = read_mapping('simple_mapping.yaml')
#     assert maps
#     data = json.load(open("original_user_info.json"))
#     result = mapper(data, mapping=maps, concat=lambda *args: ' '.join(args))
#     assert result
#
#
# def test_loading_from_advanced_yaml():
#     maps = read_mapping('advanced_mapping.yaml')
#     assert maps
