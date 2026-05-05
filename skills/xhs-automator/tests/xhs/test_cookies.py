"""Cookie 持久化测试。"""

from __future__ import annotations

import os
from unittest.mock import patch

from xhs.cookies import delete_cookies, get_cookies_file_path, load_cookies, save_cookies


class TestGetCookiesFilePath:
    def test_with_account(self):
        path = get_cookies_file_path("test_account")
        assert "test_account" in path
        assert path.endswith("cookies.json")

    def test_env_variable(self):
        with patch.dict(os.environ, {"COOKIES_PATH": "/tmp/test_cookies.json"}):
            path = get_cookies_file_path()
            assert path == "/tmp/test_cookies.json"

    def test_default_fallback(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("tempfile.gettempdir", return_value="/fake_tmp"),
            patch("os.path.exists", return_value=False),
        ):
            path = get_cookies_file_path()
            assert path == "cookies.json"


class TestCookieFileOperations:
    def test_save_and_load(self, tmp_path):
        cookie_file = str(tmp_path / "test_cookies.json")
        data = b'{"cookies": [{"name": "test"}]}'
        save_cookies(cookie_file, data)
        loaded = load_cookies(cookie_file)
        assert loaded == data

    def test_load_nonexistent(self):
        result = load_cookies("/nonexistent/path/cookies.json")
        assert result is None

    def test_delete_cookies(self, tmp_path):
        cookie_file = str(tmp_path / "test_cookies.json")
        save_cookies(cookie_file, b"test")
        assert os.path.exists(cookie_file)
        delete_cookies(cookie_file)
        assert not os.path.exists(cookie_file)

    def test_delete_nonexistent(self):
        # 不应抛出异常
        delete_cookies("/nonexistent/path/cookies.json")
