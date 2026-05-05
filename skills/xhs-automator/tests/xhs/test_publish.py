"""图文发布测试。"""

from __future__ import annotations

import time
from unittest.mock import call, patch

import pytest
from xhs.errors import (
    ContentTooLongError,
    PublishError,
    TitleTooLongError,
    UploadTimeoutError,
)
from xhs.publish import (
    _check_content_max_length,
    _check_title_max_length,
    _click_publish_tab,
    _confirm_original_declaration,
    _extract_hashtags_from_content,
    _fill_publish_form,
    _find_content_element,
    _input_single_tag,
    _input_tags,
    _navigate_to_publish_page,
    _remove_pop_cover,
    _set_original,
    _set_schedule_publish,
    _set_visibility,
    _upload_images,
    _wait_for_upload_complete,
    click_publish_button,
    fill_publish_form,
    publish_image_content,
    save_as_draft,
)
from xhs.types import PublishImageContent


class TestExtractHashtagsFromContent:
    def test_extracts_hashtags(self):
        content = "正文内容\n#标签1 #标签2"
        cleaned, tags = _extract_hashtags_from_content(content, [])
        assert cleaned == "正文内容"
        assert "标签1" in tags
        assert "标签2" in tags

    def test_no_hashtags(self):
        content = "正文内容，没有标签"
        cleaned, tags = _extract_hashtags_from_content(content, ["已有"])
        assert cleaned == content
        assert tags == ["已有"]

    def test_merges_with_existing(self):
        content = "正文\n#新标签"
        _, tags = _extract_hashtags_from_content(content, ["已有标签"])
        assert "已有标签" in tags
        assert "新标签" in tags

    def test_deduplicates(self):
        content = "正文\n#重复"
        _, tags = _extract_hashtags_from_content(content, ["重复"])
        assert tags.count("重复") == 1


class TestFillPublishForm:
    def test_empty_images_raises(self, mock_page):
        content = PublishImageContent(title="标题", content="内容", image_paths=[])
        with pytest.raises(PublishError, match="图片不能为空"):
            fill_publish_form(mock_page, content)

    @patch("xhs.publish._navigate_to_publish_page")
    @patch("xhs.publish._click_publish_tab")
    @patch("xhs.publish._upload_images")
    @patch("xhs.publish._fill_publish_form")
    def test_success(self, mock_fill, mock_upload, mock_tab, mock_nav, mock_page):
        content = PublishImageContent(title="标题", content="内容", image_paths=["img.jpg"])
        fill_publish_form(mock_page, content)
        mock_upload.assert_called_once()


class TestClickPublishButton:
    def test_success(self, mock_page):
        mock_page.evaluate.return_value = True
        click_publish_button(mock_page)

    def test_button_not_found(self, mock_page):
        mock_page.evaluate.return_value = False
        with pytest.raises(PublishError, match="未找到发布按钮"):
            click_publish_button(mock_page)


class TestSaveAsDraft:
    def test_success(self, mock_page):
        mock_page.evaluate.return_value = True
        save_as_draft(mock_page)

    def test_button_not_found(self, mock_page):
        mock_page.evaluate.return_value = False
        with pytest.raises(PublishError, match="未找到「暂存离开」按钮"):
            save_as_draft(mock_page)


class TestPublishImageContent:
    @patch("xhs.publish.click_publish_button")
    @patch("xhs.publish.fill_publish_form")
    def test_calls_fill_then_click(self, mock_fill, mock_click, mock_page):
        content = PublishImageContent(title="t", content="c", image_paths=["a.jpg"])
        publish_image_content(mock_page, content)
        mock_fill.assert_called_once_with(mock_page, content)
        mock_click.assert_called_once_with(mock_page)


class TestNavigateToPublishPage:
    @patch("xhs.publish.time")
    def test_success(self, mock_time, mock_page):
        _navigate_to_publish_page(mock_page)
        mock_page.navigate.assert_called_once()
        mock_page.wait_for_load.assert_called_once_with(timeout=300)
        mock_page.wait_dom_stable.assert_called_once()


class TestRemovePopCover:
    def test_with_popover(self, mock_page):
        mock_page.has_element.return_value = True
        _remove_pop_cover(mock_page)
        mock_page.has_element.assert_called_once()
        mock_page.remove_element.assert_called_once()
        mock_page.mouse_click.assert_called_once()

    def test_without_popover(self, mock_page):
        mock_page.has_element.return_value = False
        _remove_pop_cover(mock_page)
        mock_page.has_element.assert_called_once()
        mock_page.remove_element.assert_not_called()
        mock_page.mouse_click.assert_called_once()


class TestUploadImages:
    @patch("xhs.publish._wait_for_upload_complete")
    @patch("os.path.exists", return_value=True)
    @patch("xhs.publish.time")
    def test_single_image(self, mock_time, mock_exists, mock_wait, mock_page):
        _upload_images(mock_page, ["img.jpg"])
        mock_page.set_file_input.assert_called_once()
        mock_wait.assert_called_once_with(mock_page, 1)

    @patch("xhs.publish._wait_for_upload_complete")
    @patch("os.path.exists", return_value=True)
    @patch("xhs.publish.time")
    def test_multiple_images(self, mock_time, mock_exists, mock_wait, mock_page):
        _upload_images(mock_page, ["a.jpg", "b.jpg", "c.jpg"])
        assert mock_page.set_file_input.call_count == 3
        assert mock_wait.call_count == 3

    @patch("os.path.exists", return_value=False)
    def test_no_valid_files_raises(self, mock_exists, mock_page):
        with pytest.raises(PublishError, match="没有有效的图片文件"):
            _upload_images(mock_page, ["missing.jpg"])


class TestWaitForUploadComplete:
    @patch("xhs.publish.time")
    def test_immediate_success(self, mock_time, mock_page):
        mock_time.monotonic.side_effect = [0.0, 0.0]
        mock_time.sleep = time.sleep
        mock_page.get_elements_count.return_value = 1
        _wait_for_upload_complete(mock_page, 1)

    @patch("xhs.publish.time")
    def test_timeout_raises(self, mock_time, mock_page):
        # Simulate monotonic always returning a value past max_wait (60s)
        mock_time.monotonic.side_effect = [0.0] + [61.0] * 10
        mock_time.sleep = lambda s: None
        mock_page.get_elements_count.return_value = 0
        with pytest.raises(UploadTimeoutError, match="上传超时"):
            _wait_for_upload_complete(mock_page, 1)

    @patch("xhs.publish.time")
    def test_success_after_retries(self, mock_time, mock_page):
        mock_time.monotonic.side_effect = [0.0, 0.5, 1.0, 1.5]
        mock_time.sleep = lambda s: None
        mock_page.get_elements_count.side_effect = [0, 0, 2]
        _wait_for_upload_complete(mock_page, 2)


class TestCheckTitleMaxLength:
    def test_no_error(self, mock_page):
        mock_page.get_element_text.return_value = ""
        _check_title_max_length(mock_page)

    def test_raises_with_slash_format(self, mock_page):
        mock_page.get_element_text.return_value = "25/20"
        with pytest.raises(TitleTooLongError):
            _check_title_max_length(mock_page)

    def test_raises_without_slash(self, mock_page):
        mock_page.get_element_text.return_value = "超出"
        with pytest.raises(TitleTooLongError):
            _check_title_max_length(mock_page)


class TestCheckContentMaxLength:
    def test_no_error(self, mock_page):
        mock_page.get_element_text.return_value = ""
        _check_content_max_length(mock_page)

    def test_raises_with_slash_format(self, mock_page):
        mock_page.get_element_text.return_value = "1200/1000"
        with pytest.raises(ContentTooLongError):
            _check_content_max_length(mock_page)

    def test_raises_without_slash(self, mock_page):
        mock_page.get_element_text.return_value = "超限"
        with pytest.raises(ContentTooLongError):
            _check_content_max_length(mock_page)


class TestSetSchedulePublish:
    @patch("xhs.publish.time")
    def test_valid_iso_time(self, mock_time, mock_page):
        _set_schedule_publish(mock_page, "2026-06-01T10:30:00")
        mock_page.click_element.assert_called_once()
        mock_page.select_all_text.assert_called_once()
        mock_page.input_text.assert_called_once()
        # Verify the formatted datetime string
        args = mock_page.input_text.call_args
        assert "2026-06-01 10:30" in args[0][1]

    def test_invalid_time_format_raises(self, mock_page):
        with pytest.raises(PublishError, match="定时发布时间格式错误"):
            _set_schedule_publish(mock_page, "not-a-date")


class TestSetVisibility:
    @patch("xhs.publish.time")
    def test_default_public(self, mock_time, mock_page):
        _set_visibility(mock_page, "")
        mock_page.click_element.assert_not_called()

    @patch("xhs.publish.time")
    def test_default_public_explicit(self, mock_time, mock_page):
        _set_visibility(mock_page, "公开可见")
        mock_page.click_element.assert_not_called()

    @patch("xhs.publish.time")
    def test_only_self_visible_success(self, mock_time, mock_page):
        mock_page.evaluate.return_value = True
        _set_visibility(mock_page, "仅自己可见")
        mock_page.click_element.assert_called_once()
        mock_page.evaluate.assert_called_once()

    @patch("xhs.publish.time")
    def test_option_not_found_raises(self, mock_time, mock_page):
        mock_page.evaluate.return_value = False
        with pytest.raises(PublishError, match="未找到可见范围选项"):
            _set_visibility(mock_page, "仅自己可见")

    def test_unsupported_visibility_raises(self, mock_page):
        with pytest.raises(PublishError, match="不支持的可见范围"):
            _set_visibility(mock_page, "仅粉丝可见")


class TestFindContentElement:
    def test_editor_exists(self, mock_page):
        mock_page.has_element.return_value = True
        result = _find_content_element(mock_page)
        assert result == "div.ql-editor"

    def test_textbox_role_found(self, mock_page):
        mock_page.has_element.return_value = False
        mock_page.evaluate.return_value = "found"
        result = _find_content_element(mock_page)
        assert result == "[role='textbox']"

    def test_no_element_raises(self, mock_page):
        mock_page.has_element.return_value = False
        mock_page.evaluate.return_value = ""
        with pytest.raises(PublishError, match="没有找到内容输入框"):
            _find_content_element(mock_page)


class TestClickPublishTab:
    @patch("xhs.publish.time.sleep")
    @patch("xhs.publish.time.monotonic")
    def test_tab_found_on_first_try(self, mock_mono, mock_sleep, mock_page):
        """TAB 第一次就找到 → 直接返回。"""
        mock_mono.return_value = 0.0
        mock_page.evaluate.return_value = "clicked"
        _click_publish_tab(mock_page, "上传图文")
        mock_page.evaluate.assert_called_once()

    @patch("xhs.publish.time.sleep")
    @patch("xhs.publish.time.monotonic")
    def test_tab_blocked_then_found(self, mock_mono, mock_sleep, mock_page):
        """第一次 blocked → 移除弹窗 → 第二次 clicked。"""
        mock_mono.side_effect = [0.0, 0.0, 0.5]
        mock_page.evaluate.side_effect = ["blocked", "clicked"]
        _click_publish_tab(mock_page, "上传图文")
        assert mock_page.evaluate.call_count == 2

    @patch("xhs.publish.time.sleep")
    @patch("xhs.publish.time.monotonic")
    def test_tab_not_found_raises(self, mock_mono, mock_sleep, mock_page):
        """TAB 一直未找到 → 超时后抛出 PublishError。"""
        # deadline = time.monotonic() + 15, then loop checks < deadline
        mock_mono.side_effect = [0.0] + [16.0] * 10
        mock_page.evaluate.return_value = "not_found"
        with pytest.raises(PublishError, match="没有找到发布 TAB"):
            _click_publish_tab(mock_page, "上传图文")


class TestInputSingleTag:
    @patch("xhs.publish.time.sleep")
    @patch("xhs.publish.time.monotonic")
    @patch("xhs.publish.random.uniform", return_value=0.08)
    def test_tag_suggestion_clicked(self, mock_uniform, mock_mono, mock_sleep, mock_page):
        """标签联想出现 → 点击联想项。"""
        mock_mono.return_value = 0.0
        mock_page.has_element.side_effect = [True, True]
        _input_single_tag(mock_page, "div.ql-editor", "Python")
        # type "#" + each char + click suggestion
        assert mock_page.type_text.call_count >= 2  # 至少 "#" + chars
        mock_page.click_element.assert_called_once()

    @patch("xhs.publish.time.sleep")
    @patch("xhs.publish.time.monotonic")
    @patch("xhs.publish.random.uniform", return_value=0.08)
    def test_no_suggestion_types_space(self, mock_uniform, mock_mono, mock_sleep, mock_page):
        """无标签联想 → 直接输入空格。"""
        # monotonic: 0.0 (init deadline), then always past deadline
        mock_mono.side_effect = [0.0] + [4.0] * 20
        mock_page.has_element.return_value = False
        _input_single_tag(mock_page, "div.ql-editor", "测试")
        # Should have called type_text with " "
        space_calls = [c for c in mock_page.type_text.call_args_list if c == call(" ", delay_ms=0)]
        assert len(space_calls) >= 1


class TestInputTags:
    @patch("xhs.publish._input_single_tag")
    @patch("xhs.publish.time.sleep")
    def test_inputs_multiple_tags(self, mock_sleep, mock_input_single, mock_page):
        """多个标签逐个输入。"""
        mock_page.evaluate.return_value = 1
        _input_tags(mock_page, "div.ql-editor", ["标签1", "标签2", "标签3"])
        assert mock_input_single.call_count == 3
        # 每个标签去掉 # 前缀
        mock_input_single.assert_any_call(mock_page, "div.ql-editor", "标签1")

    @patch("xhs.publish._input_single_tag")
    @patch("xhs.publish.time.sleep")
    def test_strips_hash_prefix(self, mock_sleep, mock_input_single, mock_page):
        """标签的 # 前缀被去掉。"""
        mock_page.evaluate.return_value = 1
        _input_tags(mock_page, "div.ql-editor", ["#去掉前缀"])
        mock_input_single.assert_called_once_with(mock_page, "div.ql-editor", "去掉前缀")


class TestSetOriginal:
    @patch("xhs.publish._confirm_original_declaration")
    @patch("xhs.publish.time.sleep")
    def test_clicked(self, mock_sleep, mock_confirm, mock_page):
        """找到开关并点击 → 调用确认弹窗处理。"""
        mock_page.evaluate.return_value = "clicked"
        _set_original(mock_page)
        mock_confirm.assert_called_once()

    def test_already_on(self, mock_page):
        """原创声明已开启 → 直接返回。"""
        mock_page.evaluate.return_value = "already_on"
        _set_original(mock_page)
        # 不调用 confirm

    def test_not_found_raises(self, mock_page):
        """未找到原创声明选项 → 抛出异常。"""
        mock_page.evaluate.return_value = "not_found"
        with pytest.raises(PublishError, match="未找到原创声明选项"):
            _set_original(mock_page)


class TestConfirmOriginalDeclaration:
    @patch("xhs.publish.time.sleep")
    def test_success(self, mock_sleep, mock_page):
        """勾选 checkbox 并点击声明原创按钮。"""
        mock_page.evaluate.side_effect = [None, "clicked"]
        _confirm_original_declaration(mock_page)
        assert mock_page.evaluate.call_count == 2

    @patch("xhs.publish.time.sleep")
    def test_button_not_found_raises(self, mock_sleep, mock_page):
        """未找到声明原创按钮 → 抛出异常。"""
        mock_page.evaluate.side_effect = [None, "button_not_found"]
        with pytest.raises(PublishError, match="未找到声明原创按钮"):
            _confirm_original_declaration(mock_page)

    @patch("xhs.publish.time.sleep")
    def test_button_disabled_raises(self, mock_sleep, mock_page):
        """声明原创按钮禁用 → 抛出异常。"""
        mock_page.evaluate.side_effect = [None, "button_disabled"]
        with pytest.raises(PublishError, match="声明原创按钮仍处于禁用状态"):
            _confirm_original_declaration(mock_page)


class TestFillPublishFormExtended:
    """覆盖 _fill_publish_form 中 schedule/visibility/original 分支。"""

    @patch("xhs.publish._set_original")
    @patch("xhs.publish._set_visibility")
    @patch("xhs.publish._set_schedule_publish")
    @patch("xhs.publish._input_tags")
    @patch("xhs.publish._check_content_max_length")
    @patch("xhs.publish._check_title_max_length")
    @patch("xhs.publish._find_content_element", return_value="div.ql-editor")
    @patch("xhs.publish._extract_hashtags_from_content")
    @patch("title_utils.calc_title_length", return_value=10)
    @patch("xhs.publish.time.sleep")
    def test_with_schedule_and_original(
        self,
        mock_sleep,
        mock_calc,
        mock_extract,
        mock_find,
        mock_check_title,
        mock_check_content,
        mock_input_tags,
        mock_schedule,
        mock_visibility,
        mock_original,
        mock_page,
    ):
        """同时设置定时发布和原创声明。"""
        mock_extract.return_value = ("内容", ["标签"])
        _fill_publish_form(
            mock_page,
            "标题",
            "内容",
            ["标签"],
            schedule_time="2026-06-01T10:00:00",
            is_original=True,
            visibility="仅自己可见",
        )
        mock_schedule.assert_called_once()
        mock_visibility.assert_called_once()
        mock_original.assert_called_once()

    @patch("xhs.publish._set_visibility")
    @patch("xhs.publish._input_tags")
    @patch("xhs.publish._check_content_max_length")
    @patch("xhs.publish._check_title_max_length")
    @patch("xhs.publish._find_content_element", return_value="div.ql-editor")
    @patch("xhs.publish._extract_hashtags_from_content")
    @patch("title_utils.calc_title_length", return_value=10)
    @patch("xhs.publish.time.sleep")
    def test_no_schedule_no_original(
        self,
        mock_sleep,
        mock_calc,
        mock_extract,
        mock_find,
        mock_check_title,
        mock_check_content,
        mock_input_tags,
        mock_visibility,
        mock_page,
    ):
        """无定时发布、无原创声明。"""
        mock_extract.return_value = ("内容", [])
        _fill_publish_form(
            mock_page,
            "标题",
            "内容",
            [],
            schedule_time=None,
            is_original=False,
            visibility="",
        )
        mock_visibility.assert_called_once()

    @patch("xhs.publish._set_original", side_effect=RuntimeError("设置失败"))
    @patch("xhs.publish._set_visibility")
    @patch("xhs.publish._input_tags")
    @patch("xhs.publish._check_content_max_length")
    @patch("xhs.publish._check_title_max_length")
    @patch("xhs.publish._find_content_element", return_value="div.ql-editor")
    @patch("xhs.publish._extract_hashtags_from_content")
    @patch("title_utils.calc_title_length", return_value=10)
    @patch("xhs.publish.time.sleep")
    def test_original_failure_is_caught(
        self,
        mock_sleep,
        mock_calc,
        mock_extract,
        mock_find,
        mock_check_title,
        mock_check_content,
        mock_input_tags,
        mock_visibility,
        mock_original,
        mock_page,
    ):
        """原创声明失败被捕获，不影响整体流程。"""
        mock_extract.return_value = ("内容", [])
        # 应该不抛异常
        _fill_publish_form(
            mock_page,
            "标题",
            "内容",
            [],
            schedule_time=None,
            is_original=True,
            visibility="",
        )
        mock_original.assert_called_once()

    @patch("xhs.publish._set_visibility")
    @patch("xhs.publish._check_content_max_length")
    @patch("xhs.publish._check_title_max_length")
    @patch("xhs.publish._find_content_element", return_value="div.ql-editor")
    @patch("xhs.publish._extract_hashtags_from_content")
    @patch("title_utils.calc_title_length", return_value=10)
    @patch("xhs.publish.time.sleep")
    def test_no_tags_skips_input(
        self,
        mock_sleep,
        mock_calc,
        mock_extract,
        mock_find,
        mock_check_title,
        mock_check_content,
        mock_visibility,
        mock_page,
    ):
        """无标签时跳过 _input_tags 调用。"""
        mock_extract.return_value = ("内容", [])
        _fill_publish_form(
            mock_page,
            "标题",
            "内容",
            [],
            schedule_time=None,
            is_original=False,
            visibility="",
        )
        mock_page.input_content_editable.assert_called_once()

    @patch("xhs.publish._set_visibility")
    @patch("xhs.publish._input_tags")
    @patch("xhs.publish._check_content_max_length")
    @patch("xhs.publish._check_title_max_length")
    @patch("xhs.publish._find_content_element", return_value="div.ql-editor")
    @patch("xhs.publish._extract_hashtags_from_content")
    @patch("title_utils.calc_title_length", return_value=25)
    @patch("xhs.publish.time.sleep")
    def test_title_too_long_raises_in_form(
        self,
        mock_sleep,
        mock_calc,
        mock_extract,
        mock_find,
        mock_check_title,
        mock_check_content,
        mock_input_tags,
        mock_visibility,
        mock_page,
    ):
        """标题超长 → TitleTooLongError。"""
        mock_extract.return_value = ("内容", [])
        with pytest.raises(TitleTooLongError):
            _fill_publish_form(
                mock_page,
                "标题太长了",
                "内容",
                [],
                schedule_time=None,
                is_original=False,
                visibility="",
            )
