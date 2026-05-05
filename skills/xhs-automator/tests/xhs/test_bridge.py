"""Bridge 通信测试。"""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest
from xhs.bridge import BridgePage
from xhs.errors import CDPError, ElementNotFoundError


class TestBridgePageCall:
    def test_success(self):
        ws = MagicMock()
        ws.recv.return_value = json.dumps({"result": "ok"})
        with patch("xhs.bridge.ws_client.connect") as mock_connect:
            mock_connect.return_value.__enter__ = MagicMock(return_value=ws)
            mock_connect.return_value.__exit__ = MagicMock(return_value=False)
            page = BridgePage("ws://localhost:9333")
            result = page._call("test_method", {"key": "value"})
            assert result == "ok"

    def test_error_response(self):
        ws = MagicMock()
        ws.recv.return_value = json.dumps({"error": "something failed"})
        with patch("xhs.bridge.ws_client.connect") as mock_connect:
            mock_connect.return_value.__enter__ = MagicMock(return_value=ws)
            mock_connect.return_value.__exit__ = MagicMock(return_value=False)
            page = BridgePage("ws://localhost:9333")
            with pytest.raises(CDPError, match="Bridge 错误"):
                page._call("test_method")

    def test_connection_error(self):
        with patch("xhs.bridge.ws_client.connect", side_effect=OSError("refused")):
            page = BridgePage("ws://localhost:9333")
            with pytest.raises(CDPError, match="无法连接"):
                page._call("test_method")


class TestBridgePageNavigation:
    def test_navigate(self):
        ws = MagicMock()
        ws.recv.return_value = json.dumps({"result": None})
        with patch("xhs.bridge.ws_client.connect") as mock_connect:
            mock_connect.return_value.__enter__ = MagicMock(return_value=ws)
            mock_connect.return_value.__exit__ = MagicMock(return_value=False)
            page = BridgePage("ws://localhost:9333")
            page.navigate("https://example.com")


class TestBridgePageServerStatus:
    def test_is_server_running_true(self):
        ws = MagicMock()
        ws.recv.return_value = json.dumps({"result": {"extension_connected": True}})
        with patch("xhs.bridge.ws_client.connect") as mock_connect:
            mock_connect.return_value.__enter__ = MagicMock(return_value=ws)
            mock_connect.return_value.__exit__ = MagicMock(return_value=False)
            page = BridgePage("ws://localhost:9333")
            assert page.is_server_running() is True

    def test_is_server_running_false(self):
        with patch("xhs.bridge.ws_client.connect", side_effect=OSError("refused")):
            page = BridgePage("ws://localhost:9333")
            assert page.is_server_running() is False


class TestWaitMethods:
    def test_wait_for_load(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.wait_for_load(30.0)
            mock_call.assert_called_once_with("wait_for_load", {"timeout": 30000})

    def test_wait_for_load_default(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.wait_for_load()
            mock_call.assert_called_once_with("wait_for_load", {"timeout": 60000})

    def test_wait_dom_stable(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.wait_dom_stable(5.0, 0.3)
            mock_call.assert_called_once_with("wait_dom_stable", {"timeout": 5000, "interval": 300})

    def test_wait_dom_stable_default(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.wait_dom_stable()
            mock_call.assert_called_once_with(
                "wait_dom_stable", {"timeout": 10000, "interval": 500}
            )


class TestEvaluateMethods:
    def test_evaluate(self):
        with patch.object(BridgePage, "_call", return_value="result") as mock_call:
            page = BridgePage()
            result = page.evaluate("1 + 1")
            mock_call.assert_called_once_with("evaluate", {"expression": "1 + 1"})
            assert result == "result"

    def test_evaluate_function(self):
        with patch.object(BridgePage, "_call", return_value=42) as mock_call:
            page = BridgePage()
            result = page.evaluate_function("function() { return 42; }")
            mock_call.assert_called_once_with(
                "evaluate", {"expression": "(function() { return 42; })()"}
            )
            assert result == 42


class TestElementQueryMethods:
    def test_query_selector_found(self):
        with patch.object(BridgePage, "_call", return_value=True):
            page = BridgePage()
            assert page.query_selector("div.foo") == "found"

    def test_query_selector_not_found(self):
        with patch.object(BridgePage, "_call", return_value=False):
            page = BridgePage()
            assert page.query_selector("div.foo") is None

    def test_query_selector_all(self):
        with patch.object(BridgePage, "_call", return_value=3):
            page = BridgePage()
            result = page.query_selector_all("li.item")
            assert result == ["found", "found", "found"]

    def test_has_element_true(self):
        with patch.object(BridgePage, "_call", return_value=True):
            page = BridgePage()
            assert page.has_element("div") is True

    def test_has_element_false(self):
        with patch.object(BridgePage, "_call", return_value=False):
            page = BridgePage()
            assert page.has_element("div") is False

    def test_wait_for_element_found(self):
        with patch.object(BridgePage, "_call", return_value=True):
            page = BridgePage()
            result = page.wait_for_element("div.target", 10.0)
            assert result == "found"

    def test_wait_for_element_not_found(self):
        with patch.object(BridgePage, "_call", return_value=False):
            page = BridgePage()
            with pytest.raises(ElementNotFoundError):
                page.wait_for_element("div.target")


class TestElementActionMethods:
    def test_click_element(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.click_element("button#submit")
            mock_call.assert_called_once()
            args = mock_call.call_args[0]
            assert args[0] == "evaluate"
            assert "button#submit" in args[1]["expression"]

    def test_input_text(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.input_text("input.name", "hello")
            mock_call.assert_called_once_with(
                "input_text", {"selector": "input.name", "text": "hello"}
            )

    def test_input_content_editable(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.input_content_editable("div.editor", "rich text")
            mock_call.assert_called_once_with(
                "input_content_editable",
                {"selector": "div.editor", "text": "rich text"},
            )

    def test_get_element_text(self):
        with patch.object(BridgePage, "_call", return_value="hello"):
            page = BridgePage()
            assert page.get_element_text("p") == "hello"

    def test_get_element_attribute(self):
        with patch.object(BridgePage, "_call", return_value="value"):
            page = BridgePage()
            assert page.get_element_attribute("input", "value") == "value"

    def test_get_elements_count(self):
        with patch.object(BridgePage, "_call", return_value=5):
            page = BridgePage()
            assert page.get_elements_count("li") == 5

    def test_get_elements_count_none(self):
        with patch.object(BridgePage, "_call", return_value=None):
            page = BridgePage()
            assert page.get_elements_count("li") == 0

    def test_remove_element(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.remove_element("div.ad")
            mock_call.assert_called_once_with("remove_element", {"selector": "div.ad"})

    def test_hover_element(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.hover_element("a.link")
            mock_call.assert_called_once_with("hover_element", {"selector": "a.link"})

    def test_select_all_text(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.select_all_text("textarea")
            mock_call.assert_called_once_with("select_all_text", {"selector": "textarea"})


class TestScrollMethods:
    def test_scroll_by(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.scroll_by(100, 200)
            mock_call.assert_called_once_with("scroll_by", {"x": 100, "y": 200})

    def test_scroll_to(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.scroll_to(0, 500)
            mock_call.assert_called_once_with("scroll_to", {"x": 0, "y": 500})

    def test_scroll_to_bottom(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.scroll_to_bottom()
            mock_call.assert_called_once_with("scroll_to_bottom")

    def test_scroll_element_into_view(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.scroll_element_into_view("div.footer")
            mock_call.assert_called_once_with(
                "scroll_element_into_view", {"selector": "div.footer"}
            )

    def test_scroll_nth_element_into_view(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.scroll_nth_element_into_view("li.item", 2)
            mock_call.assert_called_once_with(
                "scroll_nth_element_into_view", {"selector": "li.item", "index": 2}
            )

    def test_get_scroll_top(self):
        with patch.object(BridgePage, "_call", return_value=150):
            page = BridgePage()
            assert page.get_scroll_top() == 150

    def test_get_scroll_top_none(self):
        with patch.object(BridgePage, "_call", return_value=None):
            page = BridgePage()
            assert page.get_scroll_top() == 0

    def test_get_viewport_height(self):
        with patch.object(BridgePage, "_call", return_value=900):
            page = BridgePage()
            assert page.get_viewport_height() == 900

    def test_get_viewport_height_none(self):
        with patch.object(BridgePage, "_call", return_value=None):
            page = BridgePage()
            assert page.get_viewport_height() == 768


class TestInputEventMethods:
    def test_press_key(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.press_key("Enter")
            mock_call.assert_called_once_with("press_key", {"key": "Enter"})

    def test_type_text(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.type_text("hello", delay_ms=100)
            mock_call.assert_called_once_with("type_text", {"text": "hello", "delayMs": 100})

    def test_type_text_default_delay(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.type_text("hello")
            mock_call.assert_called_once_with("type_text", {"text": "hello", "delayMs": 50})

    def test_mouse_move(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.mouse_move(10.5, 20.5)
            mock_call.assert_called_once_with("mouse_move", {"x": 10.5, "y": 20.5})

    def test_mouse_click(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.mouse_click(100, 200, button="right")
            mock_call.assert_called_once_with(
                "mouse_click", {"x": 100, "y": 200, "button": "right"}
            )

    def test_mouse_click_default_button(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.mouse_click(50, 60)
            mock_call.assert_called_once_with("mouse_click", {"x": 50, "y": 60, "button": "left"})

    def test_dispatch_wheel_event(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.dispatch_wheel_event(300.0)
            mock_call.assert_called_once_with("dispatch_wheel_event", {"deltaY": 300.0})


class TestFileUpload:
    def test_set_file_input(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.set_file_input("input[type=file]", ["/tmp/a.jpg", "/tmp/b.jpg"])
            expected = [os.path.abspath("/tmp/a.jpg"), os.path.abspath("/tmp/b.jpg")]
            mock_call.assert_called_once_with(
                "set_file_input", {"selector": "input[type=file]", "files": expected}
            )


class TestScreenshot:
    def test_screenshot_element_with_data(self):
        import base64

        encoded = base64.b64encode(b"imagedata").decode()
        with patch.object(BridgePage, "_call", return_value={"data": encoded}) as mock_call:
            page = BridgePage()
            result = page.screenshot_element("div.target", padding=10)
            mock_call.assert_called_once_with(
                "screenshot_element", {"selector": "div.target", "padding": 10}
            )
            assert result == b"imagedata"

    def test_screenshot_element_no_data(self):
        with patch.object(BridgePage, "_call", return_value=None):
            page = BridgePage()
            assert page.screenshot_element("div.target") == b""

    def test_screenshot_element_default_padding(self):
        with patch.object(BridgePage, "_call", return_value=None) as mock_call:
            page = BridgePage()
            page.screenshot_element("div.target")
            mock_call.assert_called_once_with(
                "screenshot_element", {"selector": "div.target", "padding": 0}
            )


class TestInjectStealth:
    def test_inject_stealth_is_noop(self):
        with patch.object(BridgePage, "_call") as mock_call:
            page = BridgePage()
            page.inject_stealth()
            mock_call.assert_not_called()


class TestIsExtensionConnected:
    def test_connected(self):
        ws = MagicMock()
        ws.recv.return_value = json.dumps({"result": {"extension_connected": True}})
        with patch("xhs.bridge.ws_client.connect") as mock_connect:
            mock_connect.return_value.__enter__ = MagicMock(return_value=ws)
            mock_connect.return_value.__exit__ = MagicMock(return_value=False)
            page = BridgePage("ws://localhost:9333")
            assert page.is_extension_connected() is True

    def test_not_connected(self):
        ws = MagicMock()
        ws.recv.return_value = json.dumps({"result": {"extension_connected": False}})
        with patch("xhs.bridge.ws_client.connect") as mock_connect:
            mock_connect.return_value.__enter__ = MagicMock(return_value=ws)
            mock_connect.return_value.__exit__ = MagicMock(return_value=False)
            page = BridgePage("ws://localhost:9333")
            assert page.is_extension_connected() is False

    def test_connection_error(self):
        with patch("xhs.bridge.ws_client.connect", side_effect=OSError("refused")):
            page = BridgePage("ws://localhost:9333")
            assert page.is_extension_connected() is False


class TestTargetId:
    def test_target_id(self):
        page = BridgePage()
        assert page.target_id == "extension-bridge"
