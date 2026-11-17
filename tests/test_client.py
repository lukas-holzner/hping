import io
import unittest
from unittest.mock import MagicMock, patch

import httpx

from hping.client import hping


class TestClient(unittest.TestCase):
    def setUp(self):
        self.stats = {"transmitted": 0, "received": 0, "rtt_times": []}

    @patch("hping.client.httpx.Client")
    def test_hping_success(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"foo": "bar"}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            hping("http://example.com", 0.1, 1, stats=self.stats)

        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)
        self.assertEqual(len(self.stats["rtt_times"]), 1)
        self.assertGreater(self.stats["rtt_times"][0], 0)
        mock_client.close.assert_called_once()

    @patch("hping.client.httpx.Client")
    def test_hping_failure(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = httpx.RequestError("Connection failed")

        with patch("sys.stdout", new_callable=io.StringIO):
            hping("http://example.com", 0.1, 1, stats=self.stats)

        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)
        self.assertEqual(len(self.stats["rtt_times"]), 0)
        mock_client.close.assert_called_once()

    @patch("hping.client.httpx.Client")
    def test_hping_post_method(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            hping("http://example.com", 0.1, 1, method="POST", stats=self.stats)

        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["method"], "POST")
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    @patch("hping.client.httpx.Client")
    def test_hping_custom_headers(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            hping(
                "http://example.com",
                0.1,
                1,
                headers=[
                    "Authorization: Bearer token",
                    "Content-Type: application/json",
                ],
                stats=self.stats,
            )

        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["headers"]["Authorization"], "Bearer token")
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")

    @patch("hping.client.httpx.Client")
    def test_hping_json_data(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            hping(
                "http://example.com", 0.1, 1, data='{"key": "value"}', stats=self.stats
            )

        mock_client.request.assert_called_once()
        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["content"], '{"key": "value"}')
        self.assertEqual(call_args[1]["headers"]["Content-Type"], "application/json")

    @patch("hping.client.httpx.Client")
    def test_hping_timeout(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = httpx.TimeoutException("Request timeout")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("http://example.com", 0.1, 1, timeout=5.0, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("Request timeout", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)

    @patch("hping.client.httpx.Client")
    def test_hping_too_many_redirects(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = httpx.TooManyRedirects("Too many redirects")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("http://example.com", 0.1, 1, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("Too many redirects", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)

    @patch("hping.client.httpx.Client")
    def test_hping_head_method(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Some content"
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("http://example.com", 0.1, 1, method="HEAD", stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("0 bytes from", output)  # HEAD should show 0 bytes
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    @patch("hping.client.httpx.Client")
    def test_hping_http2(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "2.0"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("http://example.com", 0.1, 1, http2=True, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("protocol=HTTP/2.0", output)

        # Check that client was created with http2=True
        mock_client_class.assert_called_once()
        call_args = mock_client_class.call_args
        self.assertTrue(call_args[1]["http2"])

        mock_client.request.assert_called_once()
        mock_client.close.assert_called_once()
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    @patch("hping.client.httpx.Client")
    def test_hping_redirects_info(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = [MagicMock(), MagicMock()]  # 2 redirects
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("http://example.com", 0.1, 1, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("redirects=2", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 1)

    def test_invalid_http_method(self):
        with self.assertRaises(ValueError) as context:
            hping("http://example.com", 0.1, 1, method="INVALID", stats=self.stats)

        self.assertIn("Unsupported HTTP method", str(context.exception))

    @patch("hping.client.httpx.Client")
    def test_invalid_header_format(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping(
                "http://example.com",
                0.1,
                1,
                headers=["invalid-header"],
                stats=self.stats,
            )

        output = mock_stdout.getvalue()
        self.assertIn("Invalid header format", output)

    @patch("hping.client.httpx.Client")
    def test_hping_default_stats(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"ok"
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("https://example.com", 0.01, 1)

        self.assertIn("2 bytes from https://example.com", mock_stdout.getvalue())
        mock_client.close.assert_called_once()

    @patch("hping.client.httpx.Client")
    def test_hping_non_json_data(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"ok"
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            hping(
                "http://example.com",
                0.01,
                1,
                method="POST",
                data="plain text body",
                stats=self.stats,
            )

        call_args = mock_client.request.call_args
        self.assertEqual(call_args[1]["content"], "plain text body")
        self.assertNotIn("Content-Type", call_args[1]["headers"])

    @patch("hping.client.httpx.Client")
    def test_hping_json_data_preserves_custom_content_type(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"ok"
        mock_response.http_version = "1.1"
        mock_response.history = []
        mock_client.request.return_value = mock_response

        with patch("sys.stdout", new_callable=io.StringIO):
            hping(
                "http://example.com",
                0.01,
                1,
                method="POST",
                headers=["content-type: application/vnd.api+json"],
                data='{"key": "value"}',
                stats=self.stats,
            )

        call_args = mock_client.request.call_args
        self.assertEqual(
            call_args[1]["headers"]["content-type"], "application/vnd.api+json"
        )
        self.assertNotIn("Content-Type", call_args[1]["headers"])

    @patch("hping.client.httpx.Client")
    def test_hping_unexpected_exception(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.request.side_effect = RuntimeError("Unexpected crash")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            hping("http://example.com", 0.01, 1, stats=self.stats)

        output = mock_stdout.getvalue()
        self.assertIn("Unexpected error", output)
        self.assertIn("Unexpected crash", output)
        self.assertEqual(self.stats["transmitted"], 1)
        self.assertEqual(self.stats["received"], 0)

    def test_invalid_url_scheme(self):
        with patch("sys.stdout", new_callable=io.StringIO):
            with self.assertRaises(ValueError) as context:
                hping("file:///etc/passwd", 0.1, 1, stats=self.stats)
            self.assertIn("Invalid URL", str(context.exception))

            with self.assertRaises(ValueError):
                hping("example.com", 0.1, 1, stats=self.stats)

            with self.assertRaises(ValueError):
                hping("http://", 0.1, 1, stats=self.stats)

    def test_invalid_numeric_parameters(self):
        with self.assertRaises(ValueError) as ctx:
            hping("http://example.com", -1.0, 1, stats=self.stats)
        self.assertIn("Interval must be non-negative", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            hping("http://example.com", 0.1, 1, timeout=0, stats=self.stats)
        self.assertIn("Timeout must be positive", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            hping("http://example.com", 0.1, 0, stats=self.stats)
        self.assertIn("Count must be a positive integer", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            hping("http://example.com", 0.1, 1, max_redirects=-1, stats=self.stats)
        self.assertIn("Max redirects must be non-negative", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
