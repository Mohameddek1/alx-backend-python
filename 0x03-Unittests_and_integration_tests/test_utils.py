#!/usr/bin/env python3
"""
Unittest module for utils.py
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key", {}, ("a",), "a"),
        ("missing_nested_key", {"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path, missing_key):
        """Test access_nested_map raises KeyError when key is missing"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{missing_key}'")


class TestGetJson(unittest.TestCase):
    """Tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected payload and calls requests.get"""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            from utils import get_json
            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
