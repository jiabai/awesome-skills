"""点赞/收藏测试。"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from xhs.errors import NoFeedDetailError
from xhs.like_favorite import (
    _get_interact_state,
    _prepare_page,
    _toggle_favorite,
    _toggle_like,
    _wait_collect_button,
    _wait_collected_state,
    favorite_feed,
    like_feed,
    unfavorite_feed,
    unlike_feed,
)


class TestGetInteractState:
    def test_success(self, mock_page):
        data = {"feed123": {"note": {"interactInfo": {"liked": True, "collected": False}}}}
        mock_page.evaluate.return_value = json.dumps(data)
        liked, collected = _get_interact_state(mock_page, "feed123")
        assert liked is True
        assert collected is False

    def test_empty_result_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with pytest.raises(NoFeedDetailError):
            _get_interact_state(mock_page, "feed123")

    def test_missing_feed_single_entry(self, mock_page):
        data = {"other": {"note": {"interactInfo": {"liked": True, "collected": True}}}}
        mock_page.evaluate.return_value = json.dumps(data)
        liked, collected = _get_interact_state(mock_page, "feed123")
        assert liked is True
        assert collected is True

    def test_missing_feed_multiple_entries_raises(self, mock_page):
        data = {
            "a": {"note": {"interactInfo": {"liked": True}}},
            "b": {"note": {"interactInfo": {"liked": False}}},
        }
        mock_page.evaluate.return_value = json.dumps(data)
        with pytest.raises(NoFeedDetailError):
            _get_interact_state(mock_page, "feed123")


class TestToggleLike:
    def test_already_liked_skip(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", return_value=(True, False)):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        assert result.success is True
        assert "已点赞" in result.message

    def test_already_unliked_skip(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", return_value=(False, False)):
            result = _toggle_like(mock_page, "feed123", target_liked=False)
        assert result.success is True
        assert "已取消点赞" in result.message

    def test_like_success(self, mock_page):
        with patch(
            "xhs.like_favorite._get_interact_state",
            side_effect=[(False, False), (True, False)],
        ):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        assert result.success is True
        assert "点赞成功" in result.message
        mock_page.click_element.assert_called_once()

    def test_like_retry(self, mock_page):
        with patch(
            "xhs.like_favorite._get_interact_state",
            side_effect=[(False, False), (False, False)],
        ):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        assert result.success is True
        assert "已执行" in result.message
        assert mock_page.click_element.call_count == 2

    def test_like_on_read_error(self, mock_page):
        """无法读取状态时强制点击。"""
        with patch(
            "xhs.like_favorite._get_interact_state",
            side_effect=[NoFeedDetailError(), (True, False)],
        ):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        assert result.success is True
        mock_page.click_element.assert_called_once()


class TestToggleFavorite:
    def test_already_collected_skip(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", return_value=(False, True)):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is True
        assert "已收藏" in result.message

    def test_collect_success(self, mock_page):
        with (
            patch(
                "xhs.like_favorite._get_interact_state",
                return_value=(False, False),
            ),
            patch("xhs.like_favorite._wait_collect_button", return_value=True),
            patch("xhs.like_favorite._wait_collected_state", return_value=True),
        ):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is True
        assert "收藏成功" in result.message

    def test_collect_button_not_found(self, mock_page):
        with (
            patch("xhs.like_favorite._get_interact_state", return_value=(False, False)),
            patch("xhs.like_favorite._wait_collect_button", return_value=False),
        ):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is False
        assert "未找到收藏按钮" in result.message

    def test_uncollect_success(self, mock_page):
        with (
            patch(
                "xhs.like_favorite._get_interact_state",
                return_value=(False, True),
            ),
            patch("xhs.like_favorite._wait_collect_button", return_value=True),
            patch("xhs.like_favorite._wait_collected_state", return_value=True),
        ):
            result = _toggle_favorite(mock_page, "feed123", target_collected=False)
        assert result.success is True
        assert "取消收藏成功" in result.message

    def test_collect_retry_failure(self, mock_page):
        """两次点击均未确认成功，返回失败。"""
        with (
            patch(
                "xhs.like_favorite._get_interact_state",
                return_value=(False, False),
            ),
            patch("xhs.like_favorite._wait_collect_button", return_value=True),
            patch("xhs.like_favorite._wait_collected_state", return_value=False),
        ):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is False
        assert "失败" in result.message


class TestLikeFeed:
    @patch("xhs.like_favorite._toggle_like")
    @patch("xhs.like_favorite._prepare_page")
    def test_delegates(self, mock_prepare, mock_toggle, mock_page):
        mock_toggle.return_value = None
        like_feed(mock_page, "feed123", "token")
        mock_prepare.assert_called_once_with(mock_page, "feed123", "token")
        mock_toggle.assert_called_once_with(mock_page, "feed123", target_liked=True)


class TestUnlikeFeed:
    @patch("xhs.like_favorite._toggle_like")
    @patch("xhs.like_favorite._prepare_page")
    def test_delegates(self, mock_prepare, mock_toggle, mock_page):
        mock_toggle.return_value = None
        unlike_feed(mock_page, "feed123", "token")
        mock_prepare.assert_called_once_with(mock_page, "feed123", "token")
        mock_toggle.assert_called_once_with(mock_page, "feed123", target_liked=False)


class TestFavoriteFeed:
    @patch("xhs.like_favorite._toggle_favorite")
    @patch("xhs.like_favorite._prepare_page")
    def test_delegates(self, mock_prepare, mock_toggle, mock_page):
        mock_toggle.return_value = None
        favorite_feed(mock_page, "feed123", "token")
        mock_prepare.assert_called_once_with(mock_page, "feed123", "token")
        mock_toggle.assert_called_once_with(mock_page, "feed123", target_collected=True)


class TestUnfavoriteFeed:
    @patch("xhs.like_favorite._toggle_favorite")
    @patch("xhs.like_favorite._prepare_page")
    def test_delegates(self, mock_prepare, mock_toggle, mock_page):
        mock_toggle.return_value = None
        unfavorite_feed(mock_page, "feed123", "token")
        mock_prepare.assert_called_once_with(mock_page, "feed123", "token")
        mock_toggle.assert_called_once_with(mock_page, "feed123", target_collected=False)


# ─── _prepare_page tests ────────────────────────────────────────────────────


class TestPreparePage:
    def test_calls_navigate_and_wait(self, mock_page):
        with patch("xhs.like_favorite.make_feed_detail_url", return_value="https://xhs.com/f1"):
            _prepare_page(mock_page, "feed123", "token")
        mock_page.navigate.assert_called_once_with("https://xhs.com/f1")
        mock_page.wait_for_load.assert_called_once()
        mock_page.wait_dom_stable.assert_called_once()


# ─── _toggle_like verification failure path ─────────────────────────────────


class TestToggleLikeVerification:
    def test_like_verification_raises_no_feed_detail(self, mock_page):
        """After clicking, verification raises NoFeedDetailError -> falls through to retry."""
        with patch(
            "xhs.like_favorite._get_interact_state",
            side_effect=[(False, False), NoFeedDetailError()],
        ):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        # Should click twice (initial + retry)
        assert mock_page.click_element.call_count == 2
        assert result.success is True
        assert "已执行" in result.message


# ─── _toggle_favorite click exception path ──────────────────────────────────


class TestToggleFavoriteClickException:
    def test_click_raises_exception_then_success(self, mock_page):
        """First click raises, second click succeeds."""
        with (
            patch(
                "xhs.like_favorite._get_interact_state",
                return_value=(False, False),
            ),
            patch("xhs.like_favorite._wait_collect_button", return_value=True),
            patch(
                "xhs.like_favorite._wait_collected_state",
                return_value=True,
            ),
        ):
            mock_page.click_element.side_effect = [Exception("click failed"), None]
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is True
        assert "收藏成功" in result.message

    def test_all_clicks_raise(self, mock_page):
        """All clicks raise exception -> failure after retry."""
        with (
            patch(
                "xhs.like_favorite._get_interact_state",
                return_value=(False, False),
            ),
            patch("xhs.like_favorite._wait_collect_button", return_value=True),
            patch(
                "xhs.like_favorite._wait_collected_state",
                return_value=False,
            ),
        ):
            mock_page.click_element.side_effect = Exception("click failed")
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is False
        assert "失败" in result.message


# ─── _toggle_favorite NoFeedDetailError path ────────────────────────────────


class TestToggleFavoriteReadError:
    def test_read_error_forces_click(self, mock_page):
        """NoFeedDetailError on initial read -> sets collected = not target_collected."""
        with (
            patch(
                "xhs.like_favorite._get_interact_state",
                side_effect=NoFeedDetailError(),
            ),
            patch("xhs.like_favorite._wait_collect_button", return_value=True),
            patch(
                "xhs.like_favorite._wait_collected_state",
                return_value=True,
            ),
        ):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is True
        mock_page.click_element.assert_called_once()


# ─── _wait_collect_button tests ─────────────────────────────────────────────


class TestWaitCollectButton:
    def test_immediate_found(self, mock_page):
        mock_page.has_element.return_value = True
        result = _wait_collect_button(mock_page, timeout=1.0)
        assert result is True

    def test_found_after_polling(self, mock_page):
        mock_page.has_element.side_effect = [False, False, True]
        result = _wait_collect_button(mock_page, timeout=5.0, interval=0.01)
        assert result is True

    def test_timeout(self, mock_page):
        mock_page.has_element.return_value = False
        result = _wait_collect_button(mock_page, timeout=0.01)
        assert result is False


# ─── _wait_collected_state tests ────────────────────────────────────────────


class TestWaitCollectedState:
    def test_immediate_match(self, mock_page):
        with patch(
            "xhs.like_favorite._get_interact_state",
            return_value=(False, True),
        ):
            result = _wait_collected_state(mock_page, "feed123", True, timeout=1.0)
        assert result is True

    def test_match_after_polling(self, mock_page):
        with patch(
            "xhs.like_favorite._get_interact_state",
            side_effect=[
                (False, False),
                NoFeedDetailError(),
                (False, True),
            ],
        ):
            result = _wait_collected_state(mock_page, "feed123", True, timeout=5.0, interval=0.01)
        assert result is True

    def test_timeout_no_match(self, mock_page):
        with patch(
            "xhs.like_favorite._get_interact_state",
            return_value=(False, False),
        ):
            result = _wait_collected_state(mock_page, "feed123", True, timeout=0.01)
        assert result is False
