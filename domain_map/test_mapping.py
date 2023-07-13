from domain_map import mapper


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

    assert mapper(data, mapping) == expected_result


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

    assert mapper(data, mapping) == expected_result


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
    assert mapper(data, mapping) == expected_result


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

    assert mapper(data, mapping) == expected_result


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

    assert mapper(data, mapping) == expected_result


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

    assert mapper(data, mapping) == expected_result
