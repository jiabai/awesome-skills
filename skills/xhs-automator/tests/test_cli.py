"""CLI 参数解析与子命令测试。"""

from __future__ import annotations

import os
import platform
import subprocess
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from cli import (
    _connect,
    _DummyBrowser,
    _ensure_bridge_ready,
    _open_chrome,
    _open_file_if_display,
    _output,
    _qrcode_fallback,
    build_parser,
    cmd_check_login,
    cmd_click_publish,
    cmd_delete_cookies,
    cmd_favorite_feed,
    cmd_fill_publish,
    cmd_fill_publish_video,
    cmd_get_feed_detail,
    cmd_get_qrcode,
    cmd_like_feed,
    cmd_list_feeds,
    cmd_login,
    cmd_long_article,
    cmd_next_step,
    cmd_phone_login,
    cmd_post_comment,
    cmd_publish,
    cmd_publish_video,
    cmd_reply_comment,
    cmd_save_draft,
    cmd_search_feeds,
    cmd_select_template,
    cmd_send_code,
    cmd_user_profile,
    cmd_verify_code,
    cmd_wait_login,
    main,
)

# ─── build_parser tests ─────────────────────────────────────────────────────


class TestBuildParser:
    def test_parser_creation(self):
        parser = build_parser()
        assert parser is not None

    def test_check_login_command(self):
        parser = build_parser()
        args = parser.parse_args(["check-login"])
        assert args.command == "check-login"

    def test_search_feeds_command(self):
        parser = build_parser()
        args = parser.parse_args(["search-feeds", "--keyword", "测试"])
        assert args.command == "search-feeds"
        assert args.keyword == "测试"

    def test_search_feeds_with_filters(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "search-feeds",
                "--keyword",
                "测试",
                "--sort-by",
                "最多点赞",
                "--note-type",
                "图文",
            ]
        )
        assert args.sort_by == "最多点赞"
        assert args.note_type == "图文"

    def test_publish_command(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "publish",
                "--title-file",
                "title.txt",
                "--content-file",
                "content.txt",
                "--images",
                "img1.jpg",
                "img2.jpg",
                "--tags",
                "标签1",
                "标签2",
            ]
        )
        assert args.command == "publish"
        assert args.images == ["img1.jpg", "img2.jpg"]

    def test_like_feed_command(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "like-feed",
                "--feed-id",
                "f123",
                "--xsec-token",
                "token456",
            ]
        )
        assert args.feed_id == "f123"

    def test_like_feed_unlike(self):
        parser = build_parser()
        args = parser.parse_args(
            [
                "like-feed",
                "--feed-id",
                "f123",
                "--xsec-token",
                "token456",
                "--unlike",
            ]
        )
        assert args.unlike is True


# ─── Helper fixtures ────────────────────────────────────────────────────────


@pytest.fixture
def mock_connect():
    """Mock cli._connect returning (mock_browser, mock_page)."""
    mock_browser = MagicMock()
    mock_page = MagicMock()
    with patch("cli._connect", return_value=(mock_browser, mock_page)):
        yield mock_browser, mock_page


@pytest.fixture
def mock_connect_existing():
    """Mock cli._connect_existing returning (mock_browser, mock_page)."""
    mock_browser = MagicMock()
    mock_page = MagicMock()
    with patch("cli._connect_existing", return_value=(mock_browser, mock_page)):
        yield mock_browser, mock_page


@pytest.fixture
def mock_connect_saved_tab():
    """Mock cli._connect_saved_tab returning (mock_browser, mock_page)."""
    mock_browser = MagicMock()
    mock_page = MagicMock()
    with patch("cli._connect_saved_tab", return_value=(mock_browser, mock_page)):
        yield mock_browser, mock_page


def _make_args(**kwargs):
    """Create a Namespace with given kwargs."""
    return SimpleNamespace(**kwargs)


# ─── _output tests ──────────────────────────────────────────────────────────


class TestOutput:
    def test_output_success(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            _output({"ok": True}, exit_code=0)
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert '"ok"' in captured.out
        assert "true" in captured.out

    def test_output_error_code(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            _output({"error": "fail"}, exit_code=2)
        assert exc_info.value.code == 2

    def test_output_chinese_no_ascii_escape(self, capsys):
        with pytest.raises(SystemExit):
            _output({"message": "你好"})
        captured = capsys.readouterr()
        assert "你好" in captured.out
        assert "\\u" not in captured.out


# ─── _open_file_if_display tests ────────────────────────────────────────────


class TestOpenFileIfDisplay:
    def test_windows(self):
        with (
            patch.object(platform, "system", return_value="Windows"),
            patch.object(os, "startfile") as mock_start,
        ):
            _open_file_if_display("/tmp/test.png")
            mock_start.assert_called_once_with("/tmp/test.png")

    def test_darwin(self):
        with (
            patch.object(platform, "system", return_value="Darwin"),
            patch.object(subprocess, "Popen") as mock_popen,
        ):
            _open_file_if_display("/tmp/test.png")
            mock_popen.assert_called_once_with(["open", "/tmp/test.png"])

    def test_linux(self):
        with (
            patch.object(platform, "system", return_value="Linux"),
            patch.object(subprocess, "Popen") as mock_popen,
        ):
            _open_file_if_display("/tmp/test.png")
            mock_popen.assert_called_once_with(["xdg-open", "/tmp/test.png"])


# ─── cmd_check_login tests ──────────────────────────────────────────────────


class TestCmdCheckLogin:
    def test_already_logged_in(self, mock_connect):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", True)),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_check_login(_make_args())
        assert exc_info.value.code == 0

    def test_not_logged_in(self, mock_connect):
        browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch(
                "xhs.login.make_qrcode_url",
                return_value=("data:img", "https://qr/login"),
            ),
            patch("cli._open_file_if_display"),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_check_login(_make_args())
        assert exc_info.value.code == 1
        browser.close.assert_called_once()


# ─── cmd_login tests ────────────────────────────────────────────────────────


class TestCmdLogin:
    def test_already_logged_in(self, mock_connect):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", True)),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_login(_make_args())
        assert exc_info.value.code == 0

    def test_login_success(self, mock_connect):
        browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch(
                "xhs.login.make_qrcode_url",
                return_value=("data:img", "https://qr/login"),
            ),
            patch("cli._open_file_if_display"),
            patch("xhs.login.wait_for_login", return_value=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_login(_make_args())
        assert exc_info.value.code == 0
        browser.close.assert_called_once()

    def test_login_timeout(self, mock_connect):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch(
                "xhs.login.make_qrcode_url",
                return_value=("data:img", "https://qr/login"),
            ),
            patch("cli._open_file_if_display"),
            patch("xhs.login.wait_for_login", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_login(_make_args())
        assert exc_info.value.code == 2


# ─── cmd_get_qrcode tests ──────────────────────────────────────────────────


class TestCmdGetQrcode:
    def test_already_logged_in(self, mock_connect):
        browser, page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", True)),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_get_qrcode(_make_args())
        assert exc_info.value.code == 0
        browser.close.assert_called_once()
        browser.close_page.assert_called_once_with(page)

    def test_not_logged_in(self, mock_connect, capsys):
        browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch(
                "xhs.login.make_qrcode_url",
                return_value=("data:img", "https://qr/login"),
            ),
            patch("cli._open_file_if_display"),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_get_qrcode(_make_args())
        assert exc_info.value.code == 0
        out = capsys.readouterr().out
        assert "/tmp/qr.png" in out
        browser.close.assert_called_once()

    def test_no_login_url(self, mock_connect, capsys):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch("xhs.login.make_qrcode_url", return_value=("data:img", "")),
            patch("cli._open_file_if_display"),
            pytest.raises(SystemExit),
        ):
            cmd_get_qrcode(_make_args())
        out = capsys.readouterr().out
        assert "qr_login_url" not in out


# ─── cmd_wait_login tests ───────────────────────────────────────────────────


class TestCmdWaitLogin:
    def test_success(self, mock_connect_saved_tab):
        _browser, _page = mock_connect_saved_tab
        with (
            patch("xhs.login.wait_for_login", return_value=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_wait_login(_make_args(timeout=60.0))
        assert exc_info.value.code == 0

    def test_timeout(self, mock_connect_saved_tab):
        browser, _page = mock_connect_saved_tab
        with (
            patch("xhs.login.wait_for_login", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_wait_login(_make_args(timeout=10.0))
        assert exc_info.value.code == 2
        browser.close.assert_called_once()


# ─── cmd_phone_login tests ──────────────────────────────────────────────────


class TestCmdPhoneLogin:
    def test_already_logged_in(self, mock_connect):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.send_phone_code", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_phone_login(_make_args(phone="13800138000", code="1234"))
        assert exc_info.value.code == 0

    def test_success_with_code(self, mock_connect):
        browser, _page = mock_connect
        with (
            patch("xhs.login.send_phone_code", return_value=True),
            patch("xhs.login.submit_phone_code", return_value=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_phone_login(_make_args(phone="13800138000", code="1234"))
        assert exc_info.value.code == 0
        browser.close.assert_called_once()

    def test_wrong_code(self, mock_connect):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.send_phone_code", return_value=True),
            patch("xhs.login.submit_phone_code", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_phone_login(_make_args(phone="13800138000", code="0000"))
        assert exc_info.value.code == 2

    def test_no_code_prompts_input(self, mock_connect):
        """When code is empty, input() is called."""
        _browser, page = mock_connect
        with (
            patch("xhs.login.send_phone_code", return_value=True),
            patch("builtins.input", return_value="5678"),
            patch("xhs.login.submit_phone_code", return_value=True) as mock_submit,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_phone_login(_make_args(phone="13800138000", code=""))
        mock_submit.assert_called_once_with(page, "5678")
        assert exc_info.value.code == 0


# ─── cmd_send_code tests ────────────────────────────────────────────────────


class TestCmdSendCode:
    def test_already_logged_in(self, mock_connect):
        _browser, _page = mock_connect
        with (
            patch("xhs.login.send_phone_code", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_send_code(_make_args(phone="13800138000"))
        assert exc_info.value.code == 0

    def test_code_sent(self, mock_connect, capsys):
        browser, _page = mock_connect
        with (
            patch("xhs.login.send_phone_code", return_value=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_send_code(_make_args(phone="13800138000"))
        assert exc_info.value.code == 0
        out = capsys.readouterr().out
        assert "138****8000" in out
        browser.close.assert_called_once()


# ─── cmd_verify_code tests ──────────────────────────────────────────────────


class TestCmdVerifyCode:
    def test_success(self, mock_connect_saved_tab):
        _browser, _page = mock_connect_saved_tab
        with (
            patch("xhs.login.submit_phone_code", return_value=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_verify_code(_make_args(code="1234"))
        assert exc_info.value.code == 0

    def test_failure(self, mock_connect_saved_tab):
        _browser, _page = mock_connect_saved_tab
        with (
            patch("xhs.login.submit_phone_code", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_verify_code(_make_args(code="0000"))
        assert exc_info.value.code == 2


# ─── cmd_delete_cookies tests ───────────────────────────────────────────────


class TestCmdDeleteCookies:
    def test_logout_success(self, mock_connect, capsys):
        browser, _page = mock_connect
        with patch("xhs.login.logout", return_value=True), pytest.raises(SystemExit) as exc_info:
            cmd_delete_cookies(_make_args())
        assert exc_info.value.code == 0
        out = capsys.readouterr().out
        assert "已退出登录" in out
        browser.close.assert_called_once()

    def test_not_logged_in(self, mock_connect, capsys):
        _browser, _page = mock_connect
        with patch("xhs.login.logout", return_value=False), pytest.raises(SystemExit) as exc_info:
            cmd_delete_cookies(_make_args())
        assert exc_info.value.code == 0
        out = capsys.readouterr().out
        assert "未登录" in out


# ─── cmd_list_feeds tests ───────────────────────────────────────────────────


class TestCmdListFeeds:
    def test_list_feeds(self, mock_connect):
        browser, _page = mock_connect
        mock_feed = MagicMock()
        mock_feed.to_dict.return_value = {"id": "f1", "title": "hello"}
        with (
            patch("xhs.feeds.list_feeds", return_value=[mock_feed]),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_list_feeds(_make_args())
        assert exc_info.value.code == 0
        browser.close.assert_called_once()


# ─── cmd_search_feeds tests ─────────────────────────────────────────────────


class TestCmdSearchFeeds:
    def test_search_feeds(self, mock_connect, capsys):
        browser, _page = mock_connect
        mock_feed = MagicMock()
        mock_feed.to_dict.return_value = {"id": "f1"}
        args = _make_args(
            keyword="python",
            sort_by="最新",
            note_type="图文",
            publish_time="",
            search_scope="",
            location="",
        )
        with (
            patch("xhs.search.search_feeds", return_value=[mock_feed]) as mock_search,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_search_feeds(args)
        assert exc_info.value.code == 0
        call_args = mock_search.call_args
        assert call_args[0][1] == "python"
        filter_opt = call_args[0][2]
        assert filter_opt.sort_by == "最新"
        assert filter_opt.note_type == "图文"
        browser.close.assert_called_once()


# ─── cmd_get_feed_detail tests ──────────────────────────────────────────────


class TestCmdGetFeedDetail:
    def test_get_feed_detail(self, mock_connect):
        browser, _page = mock_connect
        mock_detail = MagicMock()
        mock_detail.to_dict.return_value = {"id": "f1", "title": "test"}
        args = _make_args(
            feed_id="f1",
            xsec_token="tok",
            load_all_comments=False,
            click_more_replies=False,
            max_replies_threshold=10,
            max_comment_items=0,
            scroll_speed="normal",
        )
        with (
            patch("xhs.feed_detail.get_feed_detail", return_value=mock_detail) as mock_fn,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_get_feed_detail(args)
        assert exc_info.value.code == 0
        mock_fn.assert_called_once()
        browser.close.assert_called_once()


# ─── cmd_user_profile tests ─────────────────────────────────────────────────


class TestCmdUserProfile:
    def test_user_profile(self, mock_connect):
        browser, _page = mock_connect
        mock_profile = MagicMock()
        mock_profile.to_dict.return_value = {"user_id": "u1"}
        args = _make_args(user_id="u1", xsec_token="tok")
        with (
            patch("xhs.user_profile.get_user_profile", return_value=mock_profile),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_user_profile(args)
        assert exc_info.value.code == 0
        browser.close.assert_called_once()


# ─── cmd_post_comment tests ─────────────────────────────────────────────────


class TestCmdPostComment:
    def test_post_comment(self, mock_connect):
        browser, page = mock_connect
        args = _make_args(feed_id="f1", xsec_token="tok", content="好文")
        with patch("xhs.comment.post_comment") as mock_fn, pytest.raises(SystemExit) as exc_info:
            cmd_post_comment(args)
        assert exc_info.value.code == 0
        mock_fn.assert_called_once_with(page, "f1", "tok", "好文")
        browser.close.assert_called_once()


# ─── cmd_reply_comment tests ────────────────────────────────────────────────


class TestCmdReplyComment:
    def test_reply_comment(self, mock_connect):
        browser, page = mock_connect
        args = _make_args(
            feed_id="f1",
            xsec_token="tok",
            content="回复",
            comment_id="c1",
            user_id="u1",
        )
        with patch("xhs.comment.reply_comment") as mock_fn, pytest.raises(SystemExit) as exc_info:
            cmd_reply_comment(args)
        assert exc_info.value.code == 0
        mock_fn.assert_called_once_with(
            page,
            "f1",
            "tok",
            "回复",
            comment_id="c1",
            user_id="u1",
        )
        browser.close.assert_called_once()

    def test_reply_comment_no_ids(self, mock_connect):
        _browser, page = mock_connect
        args = _make_args(
            feed_id="f1",
            xsec_token="tok",
            content="回复",
            comment_id=None,
            user_id=None,
        )
        with patch("xhs.comment.reply_comment") as mock_fn, pytest.raises(SystemExit) as exc_info:
            cmd_reply_comment(args)
        assert exc_info.value.code == 0
        mock_fn.assert_called_once_with(
            page,
            "f1",
            "tok",
            "回复",
            comment_id="",
            user_id="",
        )


# ─── cmd_like_feed tests ────────────────────────────────────────────────────


class TestCmdLikeFeed:
    def test_like_feed(self, mock_connect):
        _browser, page = mock_connect
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"success": True}
        args = _make_args(feed_id="f1", xsec_token="tok", unlike=False)
        with (
            patch("xhs.like_favorite.like_feed", return_value=mock_result) as mock_like,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_like_feed(args)
        assert exc_info.value.code == 0
        mock_like.assert_called_once_with(page, "f1", "tok")

    def test_unlike_feed(self, mock_connect):
        browser, page = mock_connect
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"success": True}
        args = _make_args(feed_id="f1", xsec_token="tok", unlike=True)
        with (
            patch("xhs.like_favorite.unlike_feed", return_value=mock_result) as mock_unlike,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_like_feed(args)
        assert exc_info.value.code == 0
        mock_unlike.assert_called_once_with(page, "f1", "tok")
        browser.close.assert_called_once()


# ─── cmd_favorite_feed tests ────────────────────────────────────────────────


class TestCmdFavoriteFeed:
    def test_favorite_feed(self, mock_connect):
        _browser, page = mock_connect
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"success": True}
        args = _make_args(feed_id="f1", xsec_token="tok", unfavorite=False)
        with (
            patch("xhs.like_favorite.favorite_feed", return_value=mock_result) as mock_fav,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_favorite_feed(args)
        assert exc_info.value.code == 0
        mock_fav.assert_called_once_with(page, "f1", "tok")

    def test_unfavorite_feed(self, mock_connect):
        browser, page = mock_connect
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"success": True}
        args = _make_args(feed_id="f1", xsec_token="tok", unfavorite=True)
        with (
            patch("xhs.like_favorite.unfavorite_feed", return_value=mock_result) as mock_unfav,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_favorite_feed(args)
        assert exc_info.value.code == 0
        mock_unfav.assert_called_once_with(page, "f1", "tok")
        browser.close.assert_called_once()


# ─── cmd_publish tests ──────────────────────────────────────────────────────


class TestCmdPublish:
    def test_publish_success(self, mock_connect, tmp_path):
        browser, _page = mock_connect
        title_file = tmp_path / "title.txt"
        title_file.write_text("My Title", encoding="utf-8")
        content_file = tmp_path / "content.txt"
        content_file.write_text("My Content", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            images=["/tmp/a.jpg"],
            tags=["tag1"],
            schedule_at=None,
            original=False,
            visibility="",
        )
        with (
            patch("image_downloader.process_images", return_value=["/tmp/a.jpg"]),
            patch("xhs.publish.publish_image_content") as mock_pub,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_publish(args)
        assert exc_info.value.code == 0
        mock_pub.assert_called_once()
        browser.close.assert_called_once()

    def test_publish_no_images(self, mock_connect, tmp_path):
        _browser, _page = mock_connect
        title_file = tmp_path / "title.txt"
        title_file.write_text("T", encoding="utf-8")
        content_file = tmp_path / "content.txt"
        content_file.write_text("C", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            images=[],
            tags=None,
            schedule_at=None,
            original=False,
            visibility=None,
        )
        with (
            patch("image_downloader.process_images", return_value=[]),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_publish(args)
        assert exc_info.value.code == 2


# ─── cmd_fill_publish tests ─────────────────────────────────────────────────


class TestCmdFillPublish:
    def test_fill_publish_success(self, mock_connect, tmp_path):
        browser, _page = mock_connect
        title_file = tmp_path / "t.txt"
        title_file.write_text("Title", encoding="utf-8")
        content_file = tmp_path / "c.txt"
        content_file.write_text("Content", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            images=["/tmp/a.jpg"],
            tags=[],
            schedule_at=None,
            original=True,
            visibility="public",
        )
        with (
            patch("image_downloader.process_images", return_value=["/tmp/a.jpg"]),
            patch("xhs.publish.fill_publish_form") as mock_fill,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_fill_publish(args)
        assert exc_info.value.code == 0
        mock_fill.assert_called_once()
        call_data = mock_fill.call_args[0][1]
        assert call_data.title == "Title"
        assert call_data.is_original is True
        browser.close.assert_called_once()


# ─── cmd_fill_publish_video tests ───────────────────────────────────────────


class TestCmdFillPublishVideo:
    def test_fill_publish_video(self, mock_connect, tmp_path):
        browser, _page = mock_connect
        title_file = tmp_path / "t.txt"
        title_file.write_text("VTitle", encoding="utf-8")
        content_file = tmp_path / "c.txt"
        content_file.write_text("VContent", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            video="/tmp/vid.mp4",
            tags=["tag1"],
            schedule_at=None,
            visibility="",
        )
        with (
            patch("xhs.publish_video.fill_publish_video_form") as mock_fill,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_fill_publish_video(args)
        assert exc_info.value.code == 0
        call_data = mock_fill.call_args[0][1]
        assert call_data.title == "VTitle"
        assert call_data.video_path == "/tmp/vid.mp4"
        browser.close.assert_called_once()


# ─── cmd_click_publish tests ────────────────────────────────────────────────


class TestCmdClickPublish:
    def test_click_publish(self, mock_connect_existing):
        browser, page = mock_connect_existing
        with (
            patch("xhs.publish.click_publish_button") as mock_click,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_click_publish(_make_args())
        assert exc_info.value.code == 0
        mock_click.assert_called_once_with(page)
        browser.close.assert_called_once()


# ─── cmd_save_draft tests ───────────────────────────────────────────────────


class TestCmdSaveDraft:
    def test_save_draft(self, mock_connect_existing):
        browser, page = mock_connect_existing
        with patch("xhs.publish.save_as_draft") as mock_save, pytest.raises(SystemExit) as exc_info:
            cmd_save_draft(_make_args())
        assert exc_info.value.code == 0
        mock_save.assert_called_once_with(page)
        browser.close.assert_called_once()


# ─── cmd_long_article tests ─────────────────────────────────────────────────


class TestCmdLongArticle:
    def test_long_article(self, mock_connect, tmp_path):
        browser, page = mock_connect
        title_file = tmp_path / "t.txt"
        title_file.write_text("Long Title", encoding="utf-8")
        content_file = tmp_path / "c.txt"
        content_file.write_text("Long Content", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            images=["/tmp/img.jpg"],
        )
        with (
            patch(
                "xhs.publish_long_article.publish_long_article",
                return_value=["模板A", "模板B"],
            ) as mock_fn,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_long_article(args)
        assert exc_info.value.code == 0
        mock_fn.assert_called_once_with(
            page,
            title="Long Title",
            content="Long Content",
            image_paths=["/tmp/img.jpg"],
        )
        browser.close.assert_called_once()


# ─── cmd_select_template tests ──────────────────────────────────────────────


class TestCmdSelectTemplate:
    def test_success(self, mock_connect_existing):
        _browser, _page = mock_connect_existing
        with (
            patch("xhs.publish_long_article.select_template", return_value=True),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_select_template(_make_args(name="模板A"))
        assert exc_info.value.code == 0

    def test_not_found(self, mock_connect_existing, capsys):
        browser, _page = mock_connect_existing
        with (
            patch("xhs.publish_long_article.select_template", return_value=False),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_select_template(_make_args(name="不存在"))
        assert exc_info.value.code == 2
        out = capsys.readouterr().out
        assert "不存在" in out
        browser.close.assert_called_once()


# ─── cmd_next_step tests ────────────────────────────────────────────────────


class TestCmdNextStep:
    def test_next_step(self, mock_connect_existing, tmp_path):
        browser, page = mock_connect_existing
        content_file = tmp_path / "desc.txt"
        content_file.write_text("描述内容", encoding="utf-8")
        args = _make_args(content_file=str(content_file))
        with (
            patch("xhs.publish_long_article.click_next_and_fill_description") as mock_fn,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_next_step(args)
        assert exc_info.value.code == 0
        mock_fn.assert_called_once_with(page, "描述内容")
        browser.close.assert_called_once()


# ─── cmd_publish_video tests ────────────────────────────────────────────────


class TestCmdPublishVideo:
    def test_publish_video(self, mock_connect, tmp_path):
        browser, _page = mock_connect
        title_file = tmp_path / "t.txt"
        title_file.write_text("Video Title", encoding="utf-8")
        content_file = tmp_path / "c.txt"
        content_file.write_text("Video Desc", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            video="/tmp/vid.mp4",
            tags=["vtag"],
            schedule_at=None,
            visibility="",
        )
        with (
            patch("xhs.publish_video.publish_video_content") as mock_pub,
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_publish_video(args)
        assert exc_info.value.code == 0
        call_data = mock_pub.call_args[0][1]
        assert call_data.title == "Video Title"
        assert call_data.video_path == "/tmp/vid.mp4"
        browser.close.assert_called_once()


# ─── main() tests ───────────────────────────────────────────────────────────


class TestMain:
    def test_main_success(self):
        mock_args = MagicMock()
        mock_args.func = MagicMock()
        with patch("cli.build_parser") as mock_bp:
            mock_bp.return_value.parse_args.return_value = mock_args
            main()
        mock_args.func.assert_called_once_with(mock_args)

    def test_main_exception(self, capsys):
        mock_args = MagicMock()
        mock_args.func = MagicMock(side_effect=RuntimeError("boom"))
        with patch("cli.build_parser") as mock_bp:
            mock_bp.return_value.parse_args.return_value = mock_args
            with pytest.raises(SystemExit) as exc_info:
                main()
        assert exc_info.value.code == 2
        out = capsys.readouterr().out
        assert "boom" in out


# ─── _DummyBrowser tests ────────────────────────────────────────────────────


class TestDummyBrowser:
    def test_close(self):
        browser = _DummyBrowser()
        browser.close()  # should not raise

    def test_close_page(self):
        browser = _DummyBrowser()
        browser.close_page(MagicMock())  # should not raise


# ─── _open_file_if_display exception test ───────────────────────────────────


class TestOpenFileIfDisplayException:
    def test_exception_is_swallowed(self):
        """When the OS call fails, the exception is caught and logged."""
        with (
            patch.object(platform, "system", return_value="Windows"),
            patch.object(os, "startfile", side_effect=OSError("no display")),
        ):
            _open_file_if_display("/tmp/test.png")  # should not raise


# ─── _ensure_bridge_ready tests ─────────────────────────────────────────────


class TestEnsureBridgeReady:
    def test_server_running_extension_connected(self):
        """Happy path: server running, extension connected -> returns immediately."""
        mock_page = MagicMock()
        mock_page.is_server_running.return_value = True
        mock_page.is_extension_connected.return_value = True
        with patch("xhs.bridge.BridgePage", return_value=mock_page):
            _ensure_bridge_ready("ws://localhost:9333")
        mock_page.is_server_running.assert_called_once()
        mock_page.is_extension_connected.assert_called_once()

    def test_server_not_running_starts_it(self):
        """Server not running -> launches subprocess, polls until running."""
        mock_page = MagicMock()
        mock_page.is_server_running.side_effect = [False, True, True]
        mock_page.is_extension_connected.return_value = True
        with (
            patch("xhs.bridge.BridgePage", return_value=mock_page),
            patch("subprocess.Popen") as mock_popen,
        ):
            _ensure_bridge_ready("ws://localhost:9333")
        mock_popen.assert_called_once()

    def test_server_start_timeout(self):
        """Server never starts -> returns after timeout."""
        mock_page = MagicMock()
        mock_page.is_server_running.side_effect = [False] + [False] * 10
        with (
            patch("xhs.bridge.BridgePage", return_value=mock_page),
            patch("subprocess.Popen"),
        ):
            _ensure_bridge_ready("ws://localhost:9333")
        # Should have logged warning and returned, not raised

    def test_extension_not_connected_opens_chrome(self):
        """Extension not connected -> opens Chrome and polls."""
        mock_page = MagicMock()
        mock_page.is_server_running.return_value = True
        mock_page.is_extension_connected.side_effect = [False, True]
        with (
            patch("xhs.bridge.BridgePage", return_value=mock_page),
            patch("cli._open_chrome") as mock_open,
        ):
            _ensure_bridge_ready("ws://localhost:9333")
        mock_open.assert_called_once()

    def test_extension_connect_timeout(self):
        """Extension never connects -> logs warning."""
        mock_page = MagicMock()
        mock_page.is_server_running.return_value = True
        mock_page.is_extension_connected.return_value = False
        with (
            patch("xhs.bridge.BridgePage", return_value=mock_page),
            patch("cli._open_chrome"),
        ):
            _ensure_bridge_ready("ws://localhost:9333")
        # Should have logged warning, not raised


# ─── _open_chrome tests ─────────────────────────────────────────────────────


class TestOpenChrome:
    def test_windows_chrome_found(self):
        """Windows path found -> launches it."""
        with (
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen") as mock_popen,
        ):
            _open_chrome()
        mock_popen.assert_called_once()
        cmd = mock_popen.call_args[0][0]
        assert "chrome.exe" in cmd[0]

    def test_no_chrome_found_linux_fallback(self):
        """No Windows path found, linux fallback succeeds."""
        with (
            patch("os.path.exists", return_value=False),
            patch("subprocess.Popen", side_effect=[FileNotFoundError, MagicMock()]),
        ):
            _open_chrome()

    def test_no_chrome_at_all(self):
        """All launch attempts fail -> logs warning."""
        with (
            patch("os.path.exists", return_value=False),
            patch("subprocess.Popen", side_effect=FileNotFoundError),
        ):
            _open_chrome()  # should log warning, not raise


# ─── _connect tests ─────────────────────────────────────────────────────────


class TestConnect:
    def test_connect_returns_dummy_browser_and_bridge_page(self):
        mock_bp = MagicMock()
        args = _make_args(bridge_url="ws://localhost:1234")
        with (
            patch("cli._ensure_bridge_ready") as mock_ensure,
            patch("xhs.bridge.BridgePage", return_value=mock_bp),
        ):
            browser, page = _connect(args)
        assert isinstance(browser, _DummyBrowser)
        assert page is mock_bp
        mock_ensure.assert_called_once_with("ws://localhost:1234")

    def test_connect_default_bridge_url(self):
        args = SimpleNamespace()  # no bridge_url attr
        with (
            patch("cli._ensure_bridge_ready"),
            patch("xhs.bridge.BridgePage") as mock_bp_cls,
        ):
            _browser, _page = _connect(args)
        mock_bp_cls.assert_called_once_with("ws://localhost:9333")


# ─── _qrcode_fallback tests ─────────────────────────────────────────────────


class TestQrcodeFallback:
    def test_already_logged_in(self):
        browser, page = MagicMock(), MagicMock()
        args = _make_args()
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", True)),
            pytest.raises(SystemExit) as exc_info,
        ):
            _qrcode_fallback(browser, page, args)
        assert exc_info.value.code == 0

    def test_not_logged_in_with_login_url(self, capsys):
        browser, page = MagicMock(), MagicMock()
        args = _make_args()
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch(
                "xhs.login.make_qrcode_url",
                return_value=("data:img", "https://qr/login"),
            ),
            patch("cli._open_file_if_display"),
            pytest.raises(SystemExit) as exc_info,
        ):
            _qrcode_fallback(browser, page, args)
        assert exc_info.value.code == 1
        out = capsys.readouterr().out
        assert "qr_login_url" in out
        assert "验证码发送受限" in out

    def test_not_logged_in_no_login_url(self, capsys):
        browser, page = MagicMock(), MagicMock()
        args = _make_args()
        with (
            patch("xhs.login.fetch_qrcode", return_value=(b"png", "b64", False)),
            patch("xhs.login.save_qrcode_to_file", return_value="/tmp/qr.png"),
            patch("xhs.login.make_qrcode_url", return_value=("data:img", "")),
            patch("cli._open_file_if_display"),
            pytest.raises(SystemExit) as exc_info,
        ):
            _qrcode_fallback(browser, page, args)
        assert exc_info.value.code == 1
        out = capsys.readouterr().out
        assert "qr_login_url" not in out


# ─── cmd_phone_login RateLimitError test ────────────────────────────────────


class TestCmdPhoneLoginRateLimit:
    def test_rate_limit_falls_back_to_qrcode(self):
        from xhs.errors import RateLimitError

        browser, page = MagicMock(), MagicMock()
        args = _make_args(phone="13800138000", code="1234")
        with (
            patch("cli._connect", return_value=(browser, page)),
            patch("xhs.login.send_phone_code", side_effect=RateLimitError()),
            patch("cli._qrcode_fallback") as mock_fb,
        ):
            cmd_phone_login(args)
        mock_fb.assert_called_once_with(browser, page, args)
        browser.close.assert_called_once()


# ─── cmd_send_code RateLimitError test ──────────────────────────────────────


class TestCmdSendCodeRateLimit:
    def test_rate_limit_falls_back_to_qrcode(self):
        from xhs.errors import RateLimitError

        browser, page = MagicMock(), MagicMock()
        args = _make_args(phone="13800138000")
        with (
            patch("cli._connect", return_value=(browser, page)),
            patch("xhs.login.send_phone_code", side_effect=RateLimitError()),
            patch("cli._qrcode_fallback") as mock_fb,
        ):
            cmd_send_code(args)
        mock_fb.assert_called_once_with(browser, page, args)
        browser.close.assert_called_once()


# ─── cmd_fill_publish no images test ────────────────────────────────────────


class TestCmdFillPublishNoImages:
    def test_fill_publish_no_images(self, mock_connect, tmp_path):
        _browser, _page = mock_connect
        title_file = tmp_path / "t.txt"
        title_file.write_text("T", encoding="utf-8")
        content_file = tmp_path / "c.txt"
        content_file.write_text("C", encoding="utf-8")
        args = _make_args(
            title_file=str(title_file),
            content_file=str(content_file),
            images=[],
            tags=None,
            schedule_at=None,
            original=False,
            visibility=None,
        )
        with (
            patch("image_downloader.process_images", return_value=[]),
            pytest.raises(SystemExit) as exc_info,
        ):
            cmd_fill_publish(args)
        assert exc_info.value.code == 2
