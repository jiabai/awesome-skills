"""Feed 列表测试。"""

from __future__ import annotations

import contextlib
import json

import pytest
from xhs.errors import NoFeedsError
from xhs.feeds import list_feeds


class TestListFeeds:
    def test_success(self, mock_page):
        feed_data = [
            {"id": "f1", "noteCard": {"displayTitle": "标题1"}},
            {"id": "f2", "noteCard": {"displayTitle": "标题2"}},
        ]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        feeds = list_feeds(mock_page)
        assert len(feeds) == 2
        assert feeds[0].id == "f1"
        assert feeds[1].id == "f2"

    def test_no_feeds_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with pytest.raises(NoFeedsError):
            list_feeds(mock_page)

    def test_empty_array(self, mock_page):
        mock_page.evaluate.return_value = json.dumps([])
        feeds = list_feeds(mock_page)
        assert len(feeds) == 0

    def test_navigates_to_home(self, mock_page):
        mock_page.evaluate.return_value = json.dumps([])
        with contextlib.suppress(NoFeedsError):
            list_feeds(mock_page)
        mock_page.navigate.assert_called()
