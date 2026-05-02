"""长文发布测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from xhs.errors import PublishError
from xhs.publish_long_article import (
    _click_auto_format,
    _click_button_by_text,
    _click_new_creation,
    _fill_long_content,
    _fill_long_title,
    _wait_for_templates,
    click_next_and_fill_description,
    get_template_names,
    publish_long_article,
    select_template,
)


class TestSelectTemplate:
    def test_success(self, mock_page):
        mock_page.evaluate.return_value = True
        result = select_template(mock_page, "简约模板")
        assert result is True
        mock_page.evaluate.assert_called_once()

    def test_template_not_found(self, mock_page):
        mock_page.evaluate.return_value = False
        result = select_template(mock_page, "不存在的模板")
        assert result is False


class TestClickNextAndFillDescription:
    @patch("xhs.publish_long_article._click_button_by_text")
    @patch("xhs.publish_long_article._find_content_element")
    def test_success(self, mock_find, mock_click, mock_page):
        mock_find.return_value = ".content-editor"
        click_next_and_fill_description(mock_page, "描述内容")
        mock_click.assert_called_once()
        mock_page.input_content_editable.assert_called_once()

    @patch("xhs.publish_long_article._click_button_by_text")
    @patch("xhs.publish_long_article._find_content_element")
    def test_empty_description(self, mock_find, mock_click, mock_page):
        mock_find.return_value = ".content-editor"
        click_next_and_fill_description(mock_page, "")
        mock_click.assert_called_once()
        mock_page.input_content_editable.assert_not_called()


class TestGetTemplateNames:
    def test_returns_names(self, mock_page):
        mock_page.evaluate.return_value = ["模板A", "模板B"]
        names = get_template_names(mock_page)
        assert names == ["模板A", "模板B"]

    def test_empty(self, mock_page):
        mock_page.evaluate.return_value = []
        names = get_template_names(mock_page)
        assert names == []

    def test_none_returns_empty(self, mock_page):
        mock_page.evaluate.return_value = None
        names = get_template_names(mock_page)
        assert names == []


class TestPublishLongArticle:
    @patch("xhs.publish_long_article.get_template_names")
    @patch("xhs.publish_long_article._wait_for_templates")
    @patch("xhs.publish_long_article._click_auto_format")
    @patch("xhs.publish_long_article._fill_long_content")
    @patch("xhs.publish_long_article._fill_long_title")
    @patch("xhs.publish_long_article._click_new_creation")
    @patch("xhs.publish_long_article._click_publish_tab")
    @patch("xhs.publish_long_article._navigate_to_publish_page")
    def test_success(
        self,
        mock_nav,
        mock_tab,
        mock_new,
        mock_title,
        mock_content,
        mock_format,
        mock_wait,
        mock_names,
        mock_page,
    ):
        mock_names.return_value = ["模板A"]
        result = publish_long_article(mock_page, "标题", "内容", ["img.jpg"])
        assert result == ["模板A"]
        mock_nav.assert_called_once()
        mock_tab.assert_called_once()
        mock_new.assert_called_once()
        mock_title.assert_called_once()
        mock_content.assert_called_once()
        mock_format.assert_called_once()
        mock_wait.assert_called_once()
        mock_names.assert_called_once()

    @patch("xhs.publish_long_article.get_template_names")
    @patch("xhs.publish_long_article._wait_for_templates")
    @patch("xhs.publish_long_article._click_auto_format")
    @patch("xhs.publish_long_article._fill_long_content")
    @patch("xhs.publish_long_article._fill_long_title")
    @patch("xhs.publish_long_article._click_new_creation")
    @patch("xhs.publish_long_article._click_publish_tab")
    @patch("xhs.publish_long_article._navigate_to_publish_page")
    def test_no_images(
        self,
        mock_nav,
        mock_tab,
        mock_new,
        mock_title,
        mock_content,
        mock_format,
        mock_wait,
        mock_names,
        mock_page,
    ):
        mock_names.return_value = ["模板B", "模板C"]
        result = publish_long_article(mock_page, "标题", "内容")
        assert result == ["模板B", "模板C"]
        mock_nav.assert_called_once()


# ─── click_next_and_fill_description truncation test ────────────────────────


class TestClickNextAndFillDescriptionTruncation:
    @patch("xhs.publish_long_article._click_button_by_text")
    @patch("xhs.publish_long_article._find_content_element")
    def test_long_description_truncated(self, mock_find, mock_click, mock_page, caplog):
        """Description over 1000 chars should be truncated to 800."""
        mock_find.return_value = ".content-editor"
        long_desc = "a" * 1500
        click_next_and_fill_description(mock_page, long_desc)
        # Verify the truncated content was passed
        call_args = mock_page.input_content_editable.call_args
        assert len(call_args[0][1]) == 800


# ─── _click_new_creation tests ──────────────────────────────────────────────


class TestClickNewCreation:
    @patch("xhs.publish_long_article._click_button_by_text")
    def test_calls_button_and_waits(self, mock_click, mock_page):
        _click_new_creation(mock_page)
        mock_click.assert_called_once()
        mock_page.wait_dom_stable.assert_called_once()


# ─── _fill_long_title tests ─────────────────────────────────────────────────


class TestFillLongTitle:
    def test_fills_title_via_evaluate(self, mock_page):
        mock_page.evaluate.return_value = True
        _fill_long_title(mock_page, "TestTitle")
        mock_page.wait_for_element.assert_called_once()
        mock_page.evaluate.assert_called_once()
        # Verify the JS contains the title
        js = mock_page.evaluate.call_args[0][0]
        assert "TestTitle" in js


# ─── _fill_long_content tests ───────────────────────────────────────────────


class TestFillLongContent:
    def test_with_content_editor_present(self, mock_page):
        mock_page.has_element.return_value = True
        _fill_long_content(mock_page, "正文内容")
        mock_page.input_content_editable.assert_called_once()
        call_args = mock_page.input_content_editable.call_args[0]
        assert call_args[1] == "正文内容"

    @patch("xhs.publish_long_article._find_content_element")
    def test_fallback_to_find_content_element(self, mock_find, mock_page):
        mock_page.has_element.return_value = False
        mock_find.return_value = ".custom-editor"
        _fill_long_content(mock_page, "正文内容")
        mock_find.assert_called_once_with(mock_page)
        mock_page.input_content_editable.assert_called_once_with(".custom-editor", "正文内容")


# ─── _click_auto_format tests ───────────────────────────────────────────────


class TestClickAutoFormat:
    @patch("xhs.publish_long_article._click_button_by_text")
    def test_calls_button(self, mock_click, mock_page):
        _click_auto_format(mock_page)
        mock_click.assert_called_once()


# ─── _wait_for_templates tests ──────────────────────────────────────────────


class TestWaitForTemplates:
    def test_immediate_found(self, mock_page):
        mock_page.get_elements_count.return_value = 3
        result = _wait_for_templates(mock_page)
        assert result is True
        mock_page.get_elements_count.assert_called_once()

    def test_found_after_polling(self, mock_page):
        mock_page.get_elements_count.side_effect = [0, 0, 0, 5]
        result = _wait_for_templates(mock_page)
        assert result is True
        assert mock_page.get_elements_count.call_count == 4

    def test_timeout(self, mock_page):
        mock_page.get_elements_count.return_value = 0
        result = _wait_for_templates(mock_page)
        assert result is False


# ─── _click_button_by_text tests ────────────────────────────────────────────


class TestClickButtonByText:
    def test_success(self, mock_page):
        mock_page.evaluate.return_value = True
        _click_button_by_text(mock_page, "一键排版")
        mock_page.evaluate.assert_called_once()

    def test_not_found_raises(self, mock_page):
        mock_page.evaluate.return_value = False
        with pytest.raises(PublishError, match="未找到"):
            _click_button_by_text(mock_page, "不存在的按钮")
