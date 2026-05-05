"""视频发布测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from xhs.errors import PublishError, UploadTimeoutError
from xhs.publish_video import (
    _fill_publish_video_form,
    _js_str,
    _upload_video,
    _wait_for_publish_button_clickable,
    click_publish_video_button,
    fill_publish_video_form,
    publish_video_content,
)
from xhs.types import PublishVideoContent


class TestFillPublishVideoForm:
    def test_empty_video_path_raises(self, mock_page):
        content = PublishVideoContent(title="标题", content="内容", video_path="")
        with pytest.raises(PublishError, match="视频不能为空"):
            fill_publish_video_form(mock_page, content)

    @patch("xhs.publish_video._navigate_to_publish_page")
    @patch("xhs.publish_video._click_publish_tab")
    @patch("xhs.publish_video._upload_video")
    @patch("xhs.publish_video._fill_publish_video_form")
    def test_success(self, mock_fill, mock_upload, mock_tab, mock_nav, mock_page):
        content = PublishVideoContent(title="标题", content="内容", video_path="video.mp4")
        fill_publish_video_form(mock_page, content)
        mock_upload.assert_called_once()


class TestClickPublishVideoButton:
    @patch("xhs.publish_video._wait_for_publish_button_clickable")
    def test_clicks_element(self, mock_wait, mock_page):
        click_publish_video_button(mock_page)
        mock_page.click_element.assert_called_once()


class TestPublishVideoContent:
    @patch("xhs.publish_video.fill_publish_video_form")
    @patch("xhs.publish_video.click_publish_video_button")
    def test_success(self, mock_click, mock_fill, mock_page):
        content = PublishVideoContent(title="标题", content="内容", video_path="video.mp4")
        publish_video_content(mock_page, content)
        mock_fill.assert_called_once()
        mock_click.assert_called_once()


class TestJsStr:
    def test_simple_string(self):
        assert _js_str("hello") == '"hello"'

    def test_string_with_quotes(self):
        assert _js_str('say "hi"') == '"say \\"hi\\""'

    def test_empty_string(self):
        assert _js_str("") == '""'


class TestUploadVideo:
    @patch("xhs.publish_video._wait_for_publish_button_clickable")
    @patch("xhs.publish_video.os.path.exists", return_value=True)
    def test_uses_upload_input_when_present(self, mock_exists, mock_wait, mock_page):
        """当 UPLOAD_INPUT 存在时使用它。"""
        mock_page.has_element.return_value = True
        _upload_video(mock_page, "/path/to/video.mp4")
        mock_page.set_file_input.assert_called_once_with(".upload-input", ["/path/to/video.mp4"])

    @patch("xhs.publish_video._wait_for_publish_button_clickable")
    @patch("xhs.publish_video.os.path.exists", return_value=True)
    def test_falls_back_to_file_input(self, mock_exists, mock_wait, mock_page):
        """UPLOAD_INPUT 不存在时回退到 FILE_INPUT。"""
        mock_page.has_element.return_value = False
        _upload_video(mock_page, "/path/to/video.mp4")
        mock_page.set_file_input.assert_called_once_with(
            'input[type="file"]', ["/path/to/video.mp4"]
        )

    @patch("xhs.publish_video.os.path.exists", return_value=False)
    def test_video_not_found_raises(self, mock_exists, mock_page):
        with pytest.raises(PublishError, match="视频文件不存在"):
            _upload_video(mock_page, "/bad/path.mp4")


class TestWaitForPublishButtonClickable:
    @patch("xhs.publish_video.time.sleep")
    @patch("xhs.publish_video.time.monotonic")
    def test_immediately_clickable(self, mock_mono, mock_sleep, mock_page):
        """按钮立即可点击时直接返回。"""
        mock_mono.side_effect = [0.0, 0.0]  # start, first check
        mock_page.evaluate.return_value = True
        _wait_for_publish_button_clickable(mock_page)
        mock_page.evaluate.assert_called_once()

    @patch("xhs.publish_video.time.sleep")
    @patch("xhs.publish_video.time.monotonic")
    def test_clickable_after_retries(self, mock_mono, mock_sleep, mock_page):
        """按钮经过几次重试后可点击。"""
        # start=0, check1=1 (not clickable), check2=2 (clickable)
        mock_mono.side_effect = [0.0, 1.0, 2.0]
        mock_page.evaluate.side_effect = [False, True]
        _wait_for_publish_button_clickable(mock_page)
        assert mock_page.evaluate.call_count == 2

    @patch("xhs.publish_video.time.sleep")
    @patch("xhs.publish_video.time.monotonic")
    def test_timeout_raises(self, mock_mono, mock_sleep, mock_page):
        """超过最大等待时间抛出 UploadTimeoutError。"""
        # start=0, check1=601 (超过600s阈值)
        mock_mono.side_effect = [0.0, 601.0]
        mock_page.evaluate.return_value = False
        with pytest.raises(UploadTimeoutError, match="超时"):
            _wait_for_publish_button_clickable(mock_page)


class TestFillPublishVideoFormInternal:
    @patch("xhs.publish_video._set_visibility")
    @patch("xhs.publish_video._input_tags")
    @patch("xhs.publish_video._find_content_element", return_value="div.ql-editor")
    def test_fills_title_content_tags(self, mock_find, mock_tags, mock_vis, mock_page):
        _fill_publish_video_form(mock_page, "标题", "正文", ["tag1", "tag2"], None, "公开可见")
        mock_page.input_text.assert_called_once()
        mock_page.input_content_editable.assert_called_once()
        mock_tags.assert_called_once_with(mock_page, "div.ql-editor", ["tag1", "tag2"])

    @patch("xhs.publish_video._set_visibility")
    @patch("xhs.publish_video._input_tags")
    @patch("xhs.publish_video._find_content_element", return_value="div.ql-editor")
    def test_no_tags_skips_input_tags(self, mock_find, mock_tags, mock_vis, mock_page):
        _fill_publish_video_form(mock_page, "标题", "正文", [], None, "公开可见")
        mock_tags.assert_not_called()

    @patch("xhs.publish_video._set_schedule_publish")
    @patch("xhs.publish_video._set_visibility")
    @patch("xhs.publish_video._input_tags")
    @patch("xhs.publish_video._find_content_element", return_value="div.ql-editor")
    def test_with_schedule_time(self, mock_find, mock_tags, mock_vis, mock_schedule, mock_page):
        _fill_publish_video_form(mock_page, "标题", "正文", [], "2026-06-01T10:00:00", "仅自己可见")
        mock_schedule.assert_called_once_with(mock_page, "2026-06-01T10:00:00")
