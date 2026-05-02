"""登录模块测试。"""

from __future__ import annotations

import base64
from unittest.mock import patch

import pytest
from xhs.errors import RateLimitError
from xhs.login import (
    _wait_for_countdown,
    check_login_status,
    fetch_qrcode,
    get_current_user_nickname,
    logout,
    make_qrcode_url,
    save_qrcode_to_file,
    send_phone_code,
    submit_phone_code,
    wait_for_login,
)


class TestCheckLoginStatus:
    def test_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: (
            sel == ".main-container .user .link-wrapper .channel"
        )
        assert check_login_status(mock_page) is True

    def test_not_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: sel == ".login-container"
        assert check_login_status(mock_page) is False

    def test_navigates_when_not_explore(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/other"
        mock_page.has_element.side_effect = lambda sel: (
            sel == ".main-container .user .link-wrapper .channel"
        )
        check_login_status(mock_page)
        mock_page.navigate.assert_called()


class TestFetchQrcode:
    def test_already_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.return_value = True
        png_bytes, _b64_str, already = fetch_qrcode(mock_page)
        assert already is True
        assert png_bytes == b""

    def test_success(self, mock_page):
        fake_b64 = base64.b64encode(b"fake-png-data").decode()
        mock_page.evaluate.side_effect = [
            "https://www.xiaohongshu.com/explore",  # current_url
            f"data:image/png;base64,{fake_b64}",  # qrcode src
        ]
        mock_page.has_element.return_value = False
        png_bytes, _b64_str, already = fetch_qrcode(mock_page)
        assert already is False
        assert png_bytes == b"fake-png-data"

    def test_no_src_raises(self, mock_page):
        mock_page.evaluate.side_effect = [
            "https://www.xiaohongshu.com/explore",
            "",  # empty src
        ]
        mock_page.has_element.return_value = False
        with pytest.raises(RuntimeError, match="二维码图片 src 读取失败"):
            fetch_qrcode(mock_page)


class TestMakeQrcodeUrl:
    @patch("xhs.login._decode_qr_content")
    def test_with_decoded_content(self, mock_decode):
        mock_decode.return_value = "https://example.com/qr"
        image_url, login_url = make_qrcode_url(b"fake-png")
        assert "qrserver.com" in image_url
        assert login_url == "https://example.com/qr"

    @patch("xhs.login._decode_qr_content")
    def test_fallback_base64(self, mock_decode):
        mock_decode.return_value = None
        image_url, login_url = make_qrcode_url(b"fake-png")
        assert image_url.startswith("data:image/png;base64,")
        assert login_url is None


class TestSendPhoneCode:
    def test_already_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: (
            sel == ".main-container .user .link-wrapper .channel"
        )
        result = send_phone_code(mock_page, "13800138000")
        assert result is False

    def test_success(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: (
            sel
            in (
                ".login-container",
                ".agree-icon .icon-wrapper.agreed",
            )
        )
        mock_page.get_element_text.return_value = "60s"
        result = send_phone_code(mock_page, "13800138000")
        assert result is True

    def test_no_login_form_raises(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.return_value = False
        mock_page.wait_for_element.side_effect = Exception("timeout")
        with pytest.raises(RuntimeError, match="找不到登录表单"):
            send_phone_code(mock_page, "13800138000")


class TestWaitForLogin:
    def test_success(self, mock_page):
        mock_page.has_element.return_value = True
        assert wait_for_login(mock_page, timeout=1.0) is True

    def test_timeout(self, mock_page):
        mock_page.has_element.return_value = False
        assert wait_for_login(mock_page, timeout=0.1) is False


class TestWaitForCountdown:
    def test_success_on_first_try(self, mock_page):
        """按钮文字包含数字时立即返回。"""
        mock_page.get_element_text.return_value = "60s"
        _wait_for_countdown(mock_page, timeout=2.0)
        mock_page.get_element_text.assert_called()

    def test_success_after_retries(self, mock_page):
        """前几次无数字，后续出现倒计时后返回。"""
        mock_page.get_element_text.side_effect = ["获取验证码", "获取验证码", "58s"]
        _wait_for_countdown(mock_page, timeout=5.0)
        assert mock_page.get_element_text.call_count == 3

    def test_timeout_raises_rate_limit_error(self, mock_page):
        """始终无数字，超时后抛出 RateLimitError。"""
        mock_page.get_element_text.return_value = "获取验证码"
        with pytest.raises(RateLimitError):
            _wait_for_countdown(mock_page, timeout=0.5)


class TestSaveQrcodeToFile:
    @patch("builtins.open")
    @patch("os.makedirs")
    def test_saves_file_and_returns_path(self, mock_makedirs, mock_open):
        """验证 makedirs 和 open 调用，返回正确路径。"""
        result = save_qrcode_to_file(b"\x89PNG-fake")
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
        assert "login_qrcode.png" in result

    @patch("builtins.open")
    @patch("os.makedirs")
    def test_writes_bytes(self, mock_makedirs, mock_open):
        """验证写入的是 PNG 字节。"""
        fake_handle = mock_open.return_value.__enter__.return_value
        png_data = b"\x89PNG-data"
        save_qrcode_to_file(png_data)
        fake_handle.write.assert_called_once_with(png_data)


class TestSubmitPhoneCode:
    @patch("xhs.login.sleep_random")
    @patch("xhs.login.wait_for_login")
    def test_success(self, mock_wait, mock_sleep, mock_page):
        """无错误提示且 wait_for_login 返回 True，登录成功。"""
        mock_page.get_element_text.return_value = ""
        mock_wait.return_value = True
        assert submit_phone_code(mock_page, "123456") is True
        mock_page.click_element.assert_called()
        mock_page.type_text.assert_called_with("123456", delay_ms=0)

    @patch("xhs.login.sleep_random")
    def test_error_message_returns_false(self, mock_sleep, mock_page):
        """有错误提示文字时返回 False。"""
        mock_page.get_element_text.return_value = "验证码错误"
        assert submit_phone_code(mock_page, "000000") is False

    @patch("xhs.login.sleep_random")
    @patch("xhs.login.wait_for_login")
    def test_wait_for_login_fails(self, mock_wait, mock_sleep, mock_page):
        """无错误提示但 wait_for_login 返回 False。"""
        mock_page.get_element_text.return_value = ""
        mock_wait.return_value = False
        assert submit_phone_code(mock_page, "123456") is False


class TestGetCurrentUserNickname:
    def test_success(self, mock_page):
        """正常获取昵称。"""
        mock_page.evaluate.side_effect = [
            "https://www.xiaohongshu.com/explore",  # check_login_status: location.href
            "/user/profile/abc123",  # profile_href
            "测试用户",  # nickname
        ]
        mock_page.has_element.return_value = True  # check_login_status finds LOGIN_STATUS
        nickname = get_current_user_nickname(mock_page)
        assert nickname == "测试用户"
        assert mock_page.navigate.call_count == 2

    @patch("xhs.login.check_login_status")
    def test_not_logged_in(self, mock_check, mock_page):
        """未登录返回空字符串。"""
        mock_check.return_value = False
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        assert get_current_user_nickname(mock_page) == ""

    @patch("xhs.login.check_login_status")
    def test_no_profile_href(self, mock_check, mock_page):
        """无个人主页链接返回空字符串。"""
        mock_check.return_value = True
        mock_page.evaluate.return_value = ""
        assert get_current_user_nickname(mock_page) == ""

    @patch("xhs.login.check_login_status")
    def test_exception_returns_empty(self, mock_check, mock_page):
        """异常时返回空字符串（best-effort）。"""
        mock_check.side_effect = RuntimeError("boom")
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        assert get_current_user_nickname(mock_page) == ""


class TestLogout:
    @patch("xhs.login.sleep_random")
    def test_success(self, mock_sleep, mock_page):
        """已登录时执行退出流程。"""
        mock_page.has_element.return_value = True
        result = logout(mock_page)
        assert result is True
        mock_page.navigate.assert_called_once()
        mock_page.click_element.assert_called()

    @patch("xhs.login.sleep_random")
    def test_not_logged_in(self, mock_sleep, mock_page):
        """未登录时返回 False。"""
        mock_page.has_element.return_value = False
        result = logout(mock_page)
        assert result is False

    @patch("xhs.login.sleep_random")
    def test_navigates_to_explore(self, mock_sleep, mock_page):
        """验证导航到首页。"""
        mock_page.has_element.return_value = True
        logout(mock_page)
        from xhs.urls import EXPLORE_URL

        mock_page.navigate.assert_called_once_with(EXPLORE_URL)
