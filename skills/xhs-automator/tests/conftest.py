"""共享测试 fixtures。"""

from __future__ import annotations

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_sleep():
    """自动 mock time.sleep，加速测试。"""
    with patch("time.sleep"):
        yield


@pytest.fixture
def sample_feed_data():
    """示例 Feed 数据。"""
    return {
        "id": "test_feed_id",
        "noteCard": {
            "displayTitle": "测试标题",
            "user": {"userId": "user123", "nickname": "测试用户"},
            "interactInfo": {"likedCount": "100", "commentCount": "50"},
        },
    }


@pytest.fixture
def tmp_cookies(tmp_path):
    """临时 Cookie 文件。"""
    cookie_file = tmp_path / "cookies.json"
    cookie_file.write_bytes(b'{"cookies": []}')
    return str(cookie_file)
