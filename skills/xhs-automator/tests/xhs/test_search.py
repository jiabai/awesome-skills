"""搜索模块测试。"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from xhs.errors import NoFeedsError
from xhs.search import (
    _apply_filters,
    _convert_filters,
    _find_internal_option,
    _wait_for_initial_state,
    search_feeds,
)
from xhs.types import FilterOption


class TestFindInternalOption:
    def test_valid_option(self):
        group, tag = _find_internal_option(1, "最新")
        assert group == 1
        assert tag == 2

    def test_invalid_group(self):
        with pytest.raises(ValueError, match="筛选组 99 不存在"):
            _find_internal_option(99, "测试")

    def test_invalid_text(self):
        with pytest.raises(ValueError, match="未找到"):
            _find_internal_option(1, "不存在的选项")


class TestConvertFilters:
    def test_empty_filter(self):
        opt = FilterOption()
        assert _convert_filters(opt) == []

    def test_sort_by(self):
        opt = FilterOption(sort_by="最多点赞")
        result = _convert_filters(opt)
        assert (1, 3) in result

    def test_note_type(self):
        opt = FilterOption(note_type="图文")
        result = _convert_filters(opt)
        assert (2, 3) in result

    def test_multiple_filters(self):
        opt = FilterOption(sort_by="最新", note_type="视频")
        result = _convert_filters(opt)
        assert len(result) == 2


class TestSearchFeeds:
    def test_success(self, mock_page):
        feed_data = [{"id": "f1", "noteCard": {"displayTitle": "测试"}}]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        with patch("xhs.search._wait_for_initial_state"):
            feeds = search_feeds(mock_page, "关键词")
        assert len(feeds) == 1
        assert feeds[0].id == "f1"

    def test_no_feeds_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with patch("xhs.search._wait_for_initial_state"), pytest.raises(NoFeedsError):
            search_feeds(mock_page, "关键词")

    def test_with_filter(self, mock_page):
        feed_data = [{"id": "f1", "noteCard": {"displayTitle": "测试"}}]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        filter_opt = FilterOption(sort_by="最新")
        with (
            patch("xhs.search._wait_for_initial_state"),
            patch("xhs.search._apply_filters"),
        ):
            feeds = search_feeds(mock_page, "关键词", filter_opt)
        assert len(feeds) == 1

    def test_filter_without_internal_matches(self, mock_page):
        """FilterOption with all empty fields should not call _apply_filters."""
        feed_data = [{"id": "f1", "noteCard": {"displayTitle": "测试"}}]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        filter_opt = FilterOption()
        with (
            patch("xhs.search._wait_for_initial_state"),
            patch("xhs.search._apply_filters") as mock_apply,
        ):
            feeds = search_feeds(mock_page, "关键词", filter_opt)
        mock_apply.assert_not_called()
        assert len(feeds) == 1


# ─── _convert_filters additional branches ───────────────────────────────────


class TestConvertFiltersExtended:
    def test_publish_time(self):
        opt = FilterOption(publish_time="一周内")
        result = _convert_filters(opt)
        assert (3, 3) in result

    def test_search_scope(self):
        opt = FilterOption(search_scope="已关注")
        result = _convert_filters(opt)
        assert (4, 4) in result

    def test_location(self):
        opt = FilterOption(location="同城")
        result = _convert_filters(opt)
        assert (5, 2) in result

    def test_all_filters(self):
        opt = FilterOption(
            sort_by="最新",
            note_type="图文",
            publish_time="一周内",
            search_scope="已关注",
            location="同城",
        )
        result = _convert_filters(opt)
        assert len(result) == 5


# ─── _wait_for_initial_state tests ──────────────────────────────────────────


class TestWaitForInitialState:
    def test_immediate_ready(self, mock_page):
        mock_page.evaluate.return_value = True
        _wait_for_initial_state(mock_page, timeout=2.0)
        mock_page.evaluate.assert_called_once_with("window.__INITIAL_STATE__ !== undefined")

    def test_ready_after_polling(self, mock_page):
        mock_page.evaluate.side_effect = [False, False, True]
        _wait_for_initial_state(mock_page, timeout=5.0)
        assert mock_page.evaluate.call_count == 3

    def test_timeout(self, mock_page):
        mock_page.evaluate.return_value = False
        # Use a very short timeout so the test is fast
        _wait_for_initial_state(mock_page, timeout=0.01)
        # Should log warning but not raise


# ─── _apply_filters tests ───────────────────────────────────────────────────


class TestApplyFilters:
    def test_single_filter(self, mock_page):
        mock_page.has_element.return_value = True
        with (
            patch("xhs.search._wait_for_initial_state"),
            patch("xhs.search.sleep_random"),
        ):
            _apply_filters(mock_page, [(1, 2)])
        mock_page.hover_element.assert_called_once()
        mock_page.click_element.assert_called_once()

    def test_multiple_filters(self, mock_page):
        mock_page.has_element.return_value = True
        with (
            patch("xhs.search._wait_for_initial_state"),
            patch("xhs.search.sleep_random"),
        ):
            _apply_filters(mock_page, [(1, 2), (2, 3)])
        assert mock_page.click_element.call_count == 2

    def test_filter_panel_appears_late(self, mock_page):
        """Filter panel not immediately visible, appears after polling."""
        mock_page.has_element.side_effect = [False, False, True]
        with (
            patch("xhs.search._wait_for_initial_state"),
            patch("xhs.search.sleep_random"),
        ):
            _apply_filters(mock_page, [(1, 3)])
        mock_page.click_element.assert_called_once()
