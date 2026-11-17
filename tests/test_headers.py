import io
import unittest
from unittest.mock import patch

from hping.headers import parse_headers


class TestHeaders(unittest.TestCase):
    def test_parse_headers_valid(self):
        headers = [
            "Authorization: Bearer token",
            "Content-Type: application/json",
            "Accept: application/json",
        ]
        result = parse_headers(headers)
        expected = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.assertEqual(result, expected)

    def test_parse_headers_with_spaces(self):
        headers = [
            "  Authorization  :  Bearer token  ",
            "Content-Type:application/json",
        ]
        result = parse_headers(headers)
        expected = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }
        self.assertEqual(result, expected)

    def test_parse_headers_empty(self):
        result = parse_headers(None)
        self.assertEqual(result, {})

    def test_parse_headers_invalid_format(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            headers = ["invalid-header", "valid: header"]
            result = parse_headers(headers)

        output = mock_stdout.getvalue()
        self.assertIn("Invalid header format", output)
        self.assertEqual(result, {"valid": "header"})

    def test_parse_headers_multiple_colons(self):
        headers = ["Authorization: Bearer: token: with: colons"]
        result = parse_headers(headers)
        expected = {"Authorization": "Bearer: token: with: colons"}
        self.assertEqual(result, expected)

    def test_parse_headers_empty_name(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            headers = [": value", "   : another", "Valid-Name: value"]
            result = parse_headers(headers)

        output = mock_stdout.getvalue()
        self.assertIn("Header name cannot be empty", output)
        self.assertEqual(result, {"Valid-Name": "value"})

    def test_parse_headers_crlf_injection(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            headers = [
                "X-Test: val\r\nInjected: bad",
                "X-Newline: val\nInjected: bad",
                "X-Valid: safe",
            ]
            result = parse_headers(headers)

        output = mock_stdout.getvalue()
        self.assertIn("Invalid header format", output)
        self.assertEqual(result, {"X-Valid": "safe"})


if __name__ == "__main__":
    unittest.main()
