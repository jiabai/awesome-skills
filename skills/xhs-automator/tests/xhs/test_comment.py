"""评论模块测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from xhs.comment import _find_and_scroll_to_comment, _js_str, post_comment, reply_comment


class TestPostComment:
    def test_success(self, mock_page):
        mock_page.has_element.return_value = True
        with patch("xhs.comment._check_page_accessible"), patch("xhs.comment.sleep_random"):
            post_comment(mock_page, "feed123", "token456", "好文章！")
        mock_page.click_element.assert_called()
        mock_page.input_content_editable.assert_called()

    def test_no_input_trigger_raises(self, mock_page):
        mock_page.has_element.return_value = False
        with (
            patch("xhs.comment._check_page_accessible"),
            patch("xhs.comment.sleep_random"),
            pytest.raises(RuntimeError, match="未找到评论输入框"),
        ):
            post_comment(mock_page, "feed123", "token456", "评论")


class TestReplyComment:
    def test_no_ids_raises(self, mock_page):
        with pytest.raises(ValueError, match="至少提供一个"):
            reply_comment(mock_page, "feed123", "token456", "回复", comment_id="", user_id="")

    @patch("xhs.comment._find_and_scroll_to_comment")
    def test_reply_by_comment_id(self, mock_find, mock_page):
        mock_find.return_value = True
        mock_page.has_element.return_value = True
        with patch("xhs.comment._check_page_accessible"), patch("xhs.comment.sleep_random"):
            reply_comment(
                mock_page,
                "feed123",
                "token456",
                "回复",
                comment_id="c123",
            )
        mock_find.assert_called_once()

    @patch("xhs.comment._find_and_scroll_to_comment")
    def test_comment_not_found_raises(self, mock_find, mock_page):
        mock_find.return_value = False
        with (
            patch("xhs.comment._check_page_accessible"),
            patch("xhs.comment.sleep_random"),
            pytest.raises(RuntimeError, match="未找到评论"),
        ):
            reply_comment(
                mock_page,
                "feed123",
                "token456",
                "回复",
                comment_id="c999",
            )

    @patch("xhs.comment._find_and_scroll_to_comment")
    def test_reply_by_user_id(self, mock_find, mock_page):
        """只传 user_id（不传 comment_id）应走 user_id 分支。"""
        mock_find.return_value = True
        mock_page.has_element.return_value = True
        with patch("xhs.comment._check_page_accessible"), patch("xhs.comment.sleep_random"):
            reply_comment(
                mock_page,
                "feed123",
                "token456",
                "回复",
                user_id="u456",
            )
        mock_find.assert_called_once_with(mock_page, "", "u456")
        # user_id 分支使用 REPLY_BUTTON 而非 #comment-{id} REPLY_BUTTON
        mock_page.click_element.assert_any_call(".right .interactions .reply")


class TestJsStr:
    def test_simple_string(self):
        assert _js_str("hello") == '"hello"'

    def test_string_with_quotes(self):
        assert _js_str('say "hi"') == '"say \\"hi\\""'

    def test_empty_string(self):
        assert _js_str("") == '""'

    def test_unicode(self):
        # json.dumps escapes non-ASCII by default
        assert _js_str("评论") == '"\\u8bc4\\u8bba"'


class TestFindAndScrollToComment:
    @patch("xhs.comment.sleep_random")
    @patch("xhs.comment._get_comment_count", return_value=5)
    @patch("xhs.comment._check_end_container", return_value=False)
    def test_found_by_comment_id(self, mock_end, mock_count, mock_sleep, mock_page):
        """通过 comment_id 在第一次循环中找到评论。"""
        mock_page.has_element.side_effect = lambda sel: sel == "#comment-c789"
        result = _find_and_scroll_to_comment(mock_page, "c789", "", max_attempts=3)
        assert result is True
        mock_page.scroll_element_into_view.assert_any_call("#comment-c789")

    @patch("xhs.comment.sleep_random")
    @patch("xhs.comment._get_comment_count", return_value=3)
    @patch("xhs.comment._check_end_container", return_value=False)
    def test_found_by_user_id(self, mock_end, mock_count, mock_sleep, mock_page):
        """通过 user_id 找到评论。"""
        mock_page.has_element.return_value = False
        mock_page.evaluate.return_value = True
        result = _find_and_scroll_to_comment(mock_page, "", "u456", max_attempts=2)
        assert result is True

    @patch("xhs.comment.sleep_random")
    @patch("xhs.comment._get_comment_count", return_value=2)
    @patch("xhs.comment._check_end_container", return_value=True)
    def test_not_found_end_reached(self, mock_end, mock_count, mock_sleep, mock_page):
        """到达评论底部时返回 False。"""
        mock_page.has_element.return_value = False
        result = _find_and_scroll_to_comment(mock_page, "c999", "", max_attempts=5)
        assert result is False

    @patch("xhs.comment.sleep_random")
    @patch("xhs.comment._get_comment_count", return_value=1)
    @patch("xhs.comment._check_end_container", return_value=False)
    def test_stagnant_breaks(self, mock_end, mock_count, mock_sleep, mock_page):
        """评论数量停滞超过 10 次时退出。"""
        mock_page.has_element.return_value = False
        result = _find_and_scroll_to_comment(mock_page, "c000", "", max_attempts=100)
        assert result is False
        # 应该至少滚动了 10 次（stagnant 阈值）
        assert mock_page.evaluate.call_count >= 10
