"""Feed 详情测试。"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from xhs.errors import NoFeedDetailError, PageNotAccessibleError
from xhs.feed_detail import (
    _check_end_container,
    _check_no_comments,
    _check_page_accessible,
    _click_show_more_buttons,
    _extract_feed_detail,
    _get_comment_count,
    _get_total_comment_count,
    _human_scroll,
    _is_scan_qrcode_verification,
    _load_all_comments,
    _scroll_to_comments_area,
    _scroll_to_last_comment,
    get_feed_detail,
)
from xhs.types import CommentLoadConfig, FeedDetailResponse


class TestCheckPageAccessible:
    def test_accessible(self, mock_page):
        mock_page.get_element_text.return_value = None
        _check_page_accessible(mock_page)

    def test_inaccessible_keyword(self, mock_page):
        mock_page.get_element_text.return_value = "该笔记已被删除"
        with pytest.raises(PageNotAccessibleError, match="该笔记已被删除"):
            _check_page_accessible(mock_page)

    def test_scan_qrcode_retry(self, mock_page):
        mock_page.get_element_text.side_effect = ["扫码查看", ""]
        _check_page_accessible(mock_page, url="https://example.com")


class TestIsScanQrcodeVerification:
    def test_positive(self):
        assert _is_scan_qrcode_verification("请使用小红书App扫码") is True

    def test_negative(self):
        assert _is_scan_qrcode_verification("该笔记已被删除") is False


class TestExtractFeedDetail:
    def test_success(self, mock_page):
        detail = {"note": {"title": "测试"}, "comments": {"list": [], "hasMore": False}}
        mock_page.evaluate.return_value = json.dumps({"feed123": detail})
        result = _extract_feed_detail(mock_page, "feed123")
        assert isinstance(result, FeedDetailResponse)

    def test_empty_result_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with pytest.raises(NoFeedDetailError):
            _extract_feed_detail(mock_page, "feed123")

    def test_missing_feed_id_raises(self, mock_page):
        mock_page.evaluate.return_value = json.dumps({"other_feed": {}})
        with pytest.raises(NoFeedDetailError):
            _extract_feed_detail(mock_page, "feed123")


class TestCheckNoComments:
    def test_no_comments(self, mock_page):
        mock_page.get_element_text.return_value = "这是一片荒地"
        assert _check_no_comments(mock_page) is True

    def test_has_comments(self, mock_page):
        mock_page.get_element_text.return_value = "精彩评论"
        assert _check_no_comments(mock_page) is False

    def test_none_text(self, mock_page):
        mock_page.get_element_text.return_value = None
        assert _check_no_comments(mock_page) is False


class TestCheckEndContainer:
    def test_the_end(self, mock_page):
        mock_page.get_element_text.return_value = "THE END"
        assert _check_end_container(mock_page) is True

    def test_not_end(self, mock_page):
        mock_page.get_element_text.return_value = "加载更多"
        assert _check_end_container(mock_page) is False

    def test_none_text(self, mock_page):
        mock_page.get_element_text.return_value = None
        assert _check_end_container(mock_page) is False


class TestGetCommentCount:
    def test_returns_count(self, mock_page):
        mock_page.get_elements_count.return_value = 15
        assert _get_comment_count(mock_page) == 15


class TestGetFeedDetail:
    def test_success(self, mock_page):
        detail_data = {
            "feed123": {
                "note": {"title": "测试笔记", "interactInfo": {}},
                "comments": {"list": [], "hasMore": False},
            }
        }
        mock_page.evaluate.return_value = json.dumps(detail_data)
        with patch("xhs.feed_detail._check_page_accessible"), patch("xhs.feed_detail.sleep_random"):
            result = get_feed_detail(mock_page, "feed123", "token456")
        assert isinstance(result, FeedDetailResponse)


class TestGetTotalCommentCount:
    def test_matches_count(self, mock_page):
        mock_page.get_element_text.return_value = "共42条评论"
        assert _get_total_comment_count(mock_page) == 42

    def test_no_match(self, mock_page):
        mock_page.get_element_text.return_value = "暂无评论"
        assert _get_total_comment_count(mock_page) == 0

    def test_none_text(self, mock_page):
        mock_page.get_element_text.return_value = None
        assert _get_total_comment_count(mock_page) == 0


class TestScrollToCommentsArea:
    def test_scrolls_and_dispatches(self, mock_page):
        _scroll_to_comments_area(mock_page)
        mock_page.scroll_element_into_view.assert_called_once_with(".comments-container")
        mock_page.dispatch_wheel_event.assert_called_once_with(100)


class TestScrollToLastComment:
    def test_has_comments(self, mock_page):
        mock_page.get_elements_count.return_value = 5
        _scroll_to_last_comment(mock_page)
        mock_page.scroll_nth_element_into_view.assert_called_once_with(".parent-comment", 4)

    def test_no_comments(self, mock_page):
        mock_page.get_elements_count.return_value = 0
        _scroll_to_last_comment(mock_page)
        mock_page.scroll_nth_element_into_view.assert_not_called()


class TestClickShowMoreButtons:
    def test_no_buttons(self, mock_page):
        mock_page.get_elements_count.return_value = 0
        clicked, skipped = _click_show_more_buttons(mock_page, 0)
        assert clicked == 0
        assert skipped == 0

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.random.randint", return_value=0)
    def test_skips_over_threshold(self, mock_randint, mock_sleep, mock_page):
        mock_page.get_elements_count.return_value = 1
        mock_page.evaluate.return_value = "展开 200 条回复"
        clicked, skipped = _click_show_more_buttons(mock_page, 100)
        assert clicked == 0
        assert skipped == 1

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.random.randint", return_value=0)
    def test_clicks_under_threshold(self, mock_randint, mock_sleep, mock_page):
        mock_page.get_elements_count.return_value = 1
        mock_page.evaluate.side_effect = ["展开 10 条回复", ""]
        clicked, skipped = _click_show_more_buttons(mock_page, 100)
        assert clicked == 1
        assert skipped == 0
        mock_page.scroll_nth_element_into_view.assert_called_once()
        assert mock_page.evaluate.call_count == 2

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.random.randint", return_value=0)
    def test_mixed_buttons(self, mock_randint, mock_sleep, mock_page):
        mock_page.get_elements_count.return_value = 2
        mock_page.evaluate.side_effect = [
            "展开 200 条回复",
            "展开 10 条回复",
            "",
        ]
        clicked, skipped = _click_show_more_buttons(mock_page, 50)
        assert clicked == 1
        assert skipped == 1


class TestHumanScroll:
    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.calculate_scroll_delta", return_value=300)
    def test_simple_scroll(self, mock_calc_delta, mock_sleep, mock_page):
        mock_page.get_scroll_top.side_effect = [0, 300]
        mock_page.get_viewport_height.return_value = 800
        delta, top = _human_scroll(mock_page, "medium", False, 1)
        assert delta == 300
        assert top == 300
        mock_page.scroll_by.assert_called_once_with(0, 300)

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.get_scroll_ratio", return_value=0.3)
    @patch("xhs.feed_detail.calculate_scroll_delta", return_value=300)
    def test_large_mode_doubles_ratio(self, mock_calc_delta, mock_ratio, mock_sleep, mock_page):
        mock_page.get_scroll_top.side_effect = [0, 600]
        mock_page.get_viewport_height.return_value = 800
        delta, top = _human_scroll(mock_page, "medium", True, 1)
        mock_calc_delta.assert_called_once_with(800, pytest.approx(0.6))
        assert delta == 600
        assert top == 600

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.calculate_scroll_delta", return_value=5)
    def test_fallback_scroll_to_bottom(self, mock_calc_delta, mock_sleep, mock_page):
        mock_page.get_scroll_top.side_effect = [0, 5, 1000]
        mock_page.get_viewport_height.return_value = 800
        delta, top = _human_scroll(mock_page, "medium", False, 1)
        mock_page.scroll_to_bottom.assert_called_once()
        assert delta == 1000
        assert top == 1000

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.calculate_scroll_delta", return_value=300)
    def test_zero_push_count(self, mock_calc_delta, mock_sleep, mock_page):
        mock_page.get_scroll_top.return_value = 0
        mock_page.get_viewport_height.return_value = 800
        delta, top = _human_scroll(mock_page, "medium", False, 0)
        assert delta == 0
        assert top == 0

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.calculate_scroll_delta", return_value=300)
    def test_multiple_pushes(self, mock_calc_delta, mock_sleep, mock_page):
        mock_page.get_scroll_top.side_effect = [0, 300, 600]
        mock_page.get_viewport_height.return_value = 800
        delta, top = _human_scroll(mock_page, "medium", False, 2)
        assert delta == 600
        assert top == 600
        assert mock_page.scroll_by.call_count == 2


class TestCheckPageAccessibleExtended:
    """覆盖 _check_page_accessible 中扫码验证后仍然失败的路径。"""

    def test_scan_qrcode_still_qrcode_after_retry(self, mock_page):
        """扫码验证后重试仍然是扫码验证 → 抛出 PageNotAccessibleError。"""
        mock_page.get_element_text.side_effect = ["扫码查看", "打开小红书App扫码"]
        with pytest.raises(PageNotAccessibleError, match="需要在浏览器中扫码完成验证"):
            _check_page_accessible(mock_page, url="https://example.com")

    def test_scan_qrcode_then_inaccessible_keyword(self, mock_page):
        """扫码验证后重试文本匹配不可访问关键词。"""
        mock_page.get_element_text.side_effect = [
            "请使用小红书App扫码",
            "该笔记已被删除",
        ]
        with pytest.raises(PageNotAccessibleError, match="该笔记已被删除"):
            _check_page_accessible(mock_page, url="https://example.com")

    def test_unknown_text_raises(self, mock_page):
        """页面文本不匹配任何已知关键词，但非空 → 仍报错。"""
        mock_page.get_element_text.return_value = "未知的错误提示内容"
        with pytest.raises(PageNotAccessibleError, match="未知的错误提示内容"):
            _check_page_accessible(mock_page)

    def test_scan_qrcode_with_empty_url_skips_retry(self, mock_page):
        """扫码验证但 url 为空 → 走关键词检测路径，匹配则报错。"""
        mock_page.get_element_text.return_value = "扫码查看"
        # _is_scan_qrcode_verification returns True but url is falsy,
        # so it falls through to keyword check; "扫码查看" not in _INACCESSIBLE_KEYWORDS
        # and text is truthy → raises with raw text
        with pytest.raises(PageNotAccessibleError):
            _check_page_accessible(mock_page, url="")


class TestGetFeedDetailExtended:
    """覆盖 get_feed_detail 中评论加载和导航重试路径。"""

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail._check_page_accessible")
    @patch("xhs.feed_detail._load_all_comments")
    def test_load_all_comments_enabled(self, mock_load, mock_check, mock_sleep, mock_page):
        """load_all_comments=True 时调用 _load_all_comments。"""
        detail_data = {
            "f1": {
                "note": {"title": "t", "interactInfo": {}},
                "comments": {"list": [], "hasMore": False},
            }
        }
        mock_page.evaluate.return_value = json.dumps(detail_data)
        result = get_feed_detail(mock_page, "f1", "tok", load_all_comments=True)
        assert isinstance(result, FeedDetailResponse)
        mock_load.assert_called_once()

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail._check_page_accessible")
    @patch("xhs.feed_detail._load_all_comments")
    def test_load_all_comments_with_custom_config(
        self, mock_load, mock_check, mock_sleep, mock_page
    ):
        """自定义 CommentLoadConfig 传给 _load_all_comments。"""
        detail_data = {
            "f1": {
                "note": {"title": "t", "interactInfo": {}},
                "comments": {"list": [], "hasMore": False},
            }
        }
        mock_page.evaluate.return_value = json.dumps(detail_data)
        cfg = CommentLoadConfig(click_more_replies=True, max_comment_items=50)
        get_feed_detail(mock_page, "f1", "tok", load_all_comments=True, config=cfg)
        mock_load.assert_called_once_with(mock_page, cfg)

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail._check_page_accessible")
    @patch("xhs.feed_detail._load_all_comments", side_effect=RuntimeError("boom"))
    def test_load_all_comments_failure_is_caught(
        self, mock_load, mock_check, mock_sleep, mock_page
    ):
        """_load_all_comments 异常被吞掉，不影响返回结果。"""
        detail_data = {
            "f1": {
                "note": {"title": "t", "interactInfo": {}},
                "comments": {"list": [], "hasMore": False},
            }
        }
        mock_page.evaluate.return_value = json.dumps(detail_data)
        result = get_feed_detail(mock_page, "f1", "tok", load_all_comments=True)
        assert isinstance(result, FeedDetailResponse)

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail._check_page_accessible")
    def test_navigation_retry_then_success(self, mock_check, mock_sleep, mock_page):
        """导航第一次失败，第二次成功。"""
        mock_page.navigate.side_effect = [RuntimeError("timeout"), None]
        detail_data = {
            "f1": {
                "note": {"title": "t", "interactInfo": {}},
                "comments": {"list": [], "hasMore": False},
            }
        }
        mock_page.evaluate.return_value = json.dumps(detail_data)
        result = get_feed_detail(mock_page, "f1", "tok")
        assert isinstance(result, FeedDetailResponse)
        assert mock_page.navigate.call_count == 2

    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail._check_page_accessible")
    def test_navigation_all_retries_fail(self, mock_check, mock_sleep, mock_time_sleep, mock_page):
        """导航连续 3 次失败 → RuntimeError。"""
        mock_page.navigate.side_effect = RuntimeError("fail")
        with pytest.raises(RuntimeError, match="页面导航失败"):
            get_feed_detail(mock_page, "f1", "tok")


class TestLoadAllComments:
    """覆盖 _load_all_comments 状态机的各个分支。"""

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._scroll_to_comments_area")
    @patch("xhs.feed_detail._check_no_comments", return_value=True)
    def test_no_comments_returns_immediately(
        self, mock_no_comments, mock_scroll_area, mock_sleep, mock_sleep_r, mock_page
    ):
        """页面无评论 → 直接返回，不进入滚动循环。"""
        config = CommentLoadConfig()
        _load_all_comments(mock_page, config)
        mock_scroll_area.assert_called_once()
        mock_no_comments.assert_called_once()

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._get_comment_count", return_value=0)
    @patch("xhs.feed_detail._check_end_container", return_value=True)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_end_container_reached_immediately(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """一开始就检测到 THE END → 立即返回。"""
        config = CommentLoadConfig()
        _load_all_comments(mock_page, config)
        mock_end.assert_called_once()
        mock_count.assert_called()

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._human_scroll", return_value=(300, 600))
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count", side_effect=[10, 20])
    @patch("xhs.feed_detail._check_end_container", side_effect=[False, True])
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_normal_scroll_comment_increase(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """正常滚动：评论数增长后到达底部。"""
        config = CommentLoadConfig()
        _load_all_comments(mock_page, config)
        assert mock_end.call_count == 2

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._human_scroll", return_value=(300, 600))
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count", return_value=0)
    @patch("xhs.feed_detail._check_end_container", return_value=False)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_max_attempts_reached(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """达到最大尝试次数 → 走到最后冲刺逻辑。"""
        # max_comment_items=1 → max_attempts=3, count=0 so 0<1 → no early return
        config = CommentLoadConfig(max_comment_items=1)
        _load_all_comments(mock_page, config)
        assert mock_end.call_count == 3
        assert mock_count.call_count >= 3

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._click_show_more_buttons", return_value=(0, 0))
    @patch("xhs.feed_detail._human_scroll", return_value=(300, 600))
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count", return_value=10)
    @patch("xhs.feed_detail._check_end_container", return_value=False)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_click_more_replies_enabled(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_click_more,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """click_more_replies=True 时会调用 _click_show_more_buttons。"""
        config = CommentLoadConfig(click_more_replies=True, max_comment_items=1)  # max_attempts=3
        _load_all_comments(mock_page, config)
        # BUTTON_CLICK_INTERVAL=3, attempt 0 triggers click
        assert mock_click_more.call_count >= 1

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._click_show_more_buttons")
    @patch("xhs.feed_detail._human_scroll", return_value=(300, 600))
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count", return_value=10)
    @patch("xhs.feed_detail._check_end_container", return_value=False)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_click_more_replies_with_second_round(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_click_more,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """click_more 第一轮有结果 → 触发第二轮。"""
        mock_click_more.side_effect = [(1, 0), (0, 0)]
        config = CommentLoadConfig(click_more_replies=True, max_comment_items=1)
        _load_all_comments(mock_page, config)
        assert mock_click_more.call_count >= 2

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._human_scroll", return_value=(300, 600))
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count")
    @patch("xhs.feed_detail._check_end_container", return_value=False)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_max_comment_items_target_reached(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """达到目标评论数后返回。"""
        mock_count.side_effect = [0, 3, 5]
        config = CommentLoadConfig(max_comment_items=5)
        _load_all_comments(mock_page, config)

    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._human_scroll")
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count", return_value=0)
    @patch("xhs.feed_detail._check_end_container", return_value=False)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_stagnation_large_scroll_push(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """停滞超过 LARGE_SCROLL_TRIGGER → large_mode=True。"""
        # scroll_delta=5 < MIN_SCROLL_DELTA(10) → stagnant_checks 每轮+2
        # (count check +1, scroll delta check +1)
        # 第 3 轮 (index 2) 时 stagnant_checks=4+1=5 >= LARGE_SCROLL_TRIGGER(5)
        mock_human_scroll.return_value = (5, 10)
        config = CommentLoadConfig(max_comment_items=1)  # max_attempts=3
        _load_all_comments(mock_page, config)
        # 3 次循环 + 1 次最终冲刺 = 4
        assert mock_human_scroll.call_count == 4
        # 第 3 次调用 (index 2) 时 large_mode=True
        assert mock_human_scroll.call_args_list[2][0][2] is True

    @patch("xhs.feed_detail.STAGNANT_LIMIT", 2)
    @patch("xhs.feed_detail.DEFAULT_MAX_ATTEMPTS", 10)
    @patch("xhs.feed_detail.sleep_random")
    @patch("xhs.feed_detail.time.sleep")
    @patch("xhs.feed_detail._human_scroll")
    @patch("xhs.feed_detail._scroll_to_last_comment")
    @patch("xhs.feed_detail._get_comment_count", return_value=5)
    @patch("xhs.feed_detail._check_end_container", return_value=False)
    @patch("xhs.feed_detail._check_no_comments", return_value=False)
    @patch("xhs.feed_detail._scroll_to_comments_area")
    def test_stagnation_triggers_sprint(
        self,
        mock_scroll_area,
        mock_no_comments,
        mock_end,
        mock_count,
        mock_scroll_last,
        mock_human_scroll,
        mock_sleep,
        mock_sleep_r,
        mock_page,
    ):
        """停滞检查达到 STAGNANT_LIMIT → 触发大冲刺并重置。"""
        # 始终返回小 delta → stagnant_checks 持续累加
        mock_human_scroll.return_value = (5, 10)
        config = CommentLoadConfig(max_comment_items=0)  # uses DEFAULT_MAX_ATTEMPTS(10)
        _load_all_comments(mock_page, config)
        # 至少调用了 human_scroll
        assert mock_human_scroll.call_count >= 1
