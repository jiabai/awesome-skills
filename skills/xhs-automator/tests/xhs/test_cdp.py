"""CDP 客户端测试。"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from xhs.cdp import Browser, CDPClient, Page
from xhs.errors import CDPError, ElementNotFoundError


class TestCDPClient:
    def test_send_success(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_ws.recv.return_value = json.dumps({"id": 1, "result": {"value": "ok"}})
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://localhost:9222/devtools")
            result = client.send("Test.method")
            assert result == {"value": "ok"}

    def test_send_error(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_ws.recv.return_value = json.dumps({"id": 1, "error": {"message": "fail"}})
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://localhost:9222/devtools")
            with pytest.raises(CDPError, match="CDP 错误"):
                client.send("Test.method")

    def test_send_timeout(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_ws.recv.side_effect = TimeoutError
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://localhost:9222/devtools")
            with pytest.raises(CDPError, match="超时"):
                client.send("Test.method")

    def test_close(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://localhost:9222/devtools")
            client.close()
            mock_ws.close.assert_called_once()


class TestPage:
    def test_navigate(self, mock_page):
        mock_page.navigate("https://example.com")
        mock_page.navigate.assert_called_once_with("https://example.com")

    def test_evaluate(self, mock_page):
        mock_page.evaluate.return_value = "hello"
        result = mock_page.evaluate("document.title")
        assert result == "hello"

    def test_has_element_true(self, mock_page):
        mock_page.has_element.return_value = True
        assert mock_page.has_element(".selector") is True

    def test_has_element_false(self, mock_page):
        mock_page.has_element.return_value = False
        assert mock_page.has_element(".selector") is False

    def test_click_element(self, mock_page):
        mock_page.click_element(".button")
        mock_page.click_element.assert_called_once_with(".button")

    def test_get_element_text(self, mock_page):
        mock_page.get_element_text.return_value = "文本内容"
        result = mock_page.get_element_text(".el")
        assert result == "文本内容"

    def test_get_elements_count(self, mock_page):
        mock_page.get_elements_count.return_value = 5
        assert mock_page.get_elements_count(".items") == 5

    def test_wait_for_element(self, mock_page):
        mock_page.wait_for_element.return_value = "object-id-123"
        oid = mock_page.wait_for_element(".el", timeout=10)
        assert oid == "object-id-123"

    def test_scroll_by(self, mock_page):
        mock_page.scroll_by(0, 500)
        mock_page.scroll_by.assert_called_once_with(0, 500)

    def test_input_text(self, mock_page):
        mock_page.input_text(".input", "hello")
        mock_page.input_text.assert_called_once_with(".input", "hello")

    def test_set_file_input(self, mock_page):
        mock_page.set_file_input("input[type=file]", ["/path/to/file.jpg"])
        mock_page.set_file_input.assert_called_once()


class TestBrowser:
    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_connect(self, mock_cdp_cls, mock_get):
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        browser = Browser()
        browser.connect()
        assert browser._chrome_version == "134.0.6998.88"

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_new_page(self, mock_cdp_cls, mock_get):
        mock_cdp = MagicMock()
        mock_cdp.send.side_effect = [
            {"targetId": "target-1"},
            {"sessionId": "session-1"},
        ]
        # Page._send_session uses cdp._ws directly for send/recv,
        # so we need _ws.recv to return valid JSON responses.
        # _id_counter starts at 1000; _setup_page makes 3 _send_session calls
        # (ids 1001, 1002, 1003).
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        browser = Browser()
        browser.connect()
        page = browser.new_page()
        assert page.target_id == "target-1"
        assert page.session_id == "session-1"


_next_id_counter = 0
_response_queue: list[str] = []


def _make_real_page() -> tuple[Page, MagicMock]:
    """Create a real Page backed by a mocked WebSocket.

    Returns (page, mock_ws) so tests can configure mock_ws.recv/send.
    """
    global _next_id_counter, _response_queue
    _next_id_counter = 1000
    _response_queue = []
    with patch("xhs.cdp.ws_client.connect") as mock_connect:
        mock_ws = MagicMock()
        mock_connect.return_value = mock_ws
        client = CDPClient("ws://test")
        page = Page(client, "target-1", "session-1")
        # Use a callable side_effect so we can accumulate responses
        # without MagicMock converting the list to an iterator.
        mock_ws.recv.side_effect = lambda **kw: _response_queue.pop(0)
        return page, mock_ws


def _session_response(mock_ws: MagicMock, result: dict | None = None) -> None:
    """Append a response for the next _send_session / _wait_session call.

    _id_counter starts at 1000, incremented before each _send_session call.
    """
    global _next_id_counter
    _next_id_counter += 1
    msg_id = _next_id_counter
    _response_queue.append(json.dumps({"id": msg_id, "result": result or {}}))


class TestPageScroll:
    """Test Page scroll methods with real implementation."""

    def test_scroll_to(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.scroll_to(100, 200)
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert sent["method"] == "Runtime.evaluate"
        assert "window.scrollTo(100, 200)" in sent["params"]["expression"]

    def test_scroll_to_bottom(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.scroll_to_bottom()
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert "window.scrollTo(0, document.body.scrollHeight)" in sent["params"]["expression"]

    def test_get_scroll_top_returns_int(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "number", "value": 42}})
        result = page.get_scroll_top()
        assert result == 42

    def test_get_scroll_top_returns_zero_for_none(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        result = page.get_scroll_top()
        assert result == 0

    def test_get_viewport_height_returns_int(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "number", "value": 900}})
        result = page.get_viewport_height()
        assert result == 900

    def test_get_viewport_height_returns_default_for_none(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        result = page.get_viewport_height()
        assert result == 768


class TestPageMouse:
    """Test Page mouse methods with real implementation."""

    def test_mouse_move_sends_event(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        page.mouse_move(150.0, 250.0)
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert sent["method"] == "Input.dispatchMouseEvent"
        assert sent["params"]["type"] == "mouseMoved"
        assert sent["params"]["x"] == 150.0
        assert sent["params"]["y"] == 250.0
        assert sent["sessionId"] == "session-1"

    def test_mouse_click_left_button(self):
        page, mock_ws = _make_real_page()
        # mouse_click sends two events: mousePressed + mouseReleased
        _session_response(mock_ws)
        _session_response(mock_ws)
        page.mouse_click(100.0, 200.0, button="left")
        calls = mock_ws.send.call_args_list
        pressed = json.loads(calls[-2][0][0])
        released = json.loads(calls[-1][0][0])
        assert pressed["params"]["type"] == "mousePressed"
        assert pressed["params"]["button"] == "left"
        assert released["params"]["type"] == "mouseReleased"
        assert released["params"]["button"] == "left"

    def test_mouse_click_right_button(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        _session_response(mock_ws)
        page.mouse_click(100.0, 200.0, button="right")
        calls = mock_ws.send.call_args_list
        pressed = json.loads(calls[-2][0][0])
        assert pressed["params"]["button"] == "right"


class TestPageKeyboard:
    """Test Page keyboard methods with real implementation."""

    def test_press_key_enter(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        _session_response(mock_ws)
        page.press_key("Enter")
        calls = mock_ws.send.call_args_list
        key_down = json.loads(calls[-2][0][0])
        key_up = json.loads(calls[-1][0][0])
        assert key_down["params"]["type"] == "keyDown"
        assert key_down["params"]["key"] == "Enter"
        assert key_down["params"]["windowsVirtualKeyCode"] == 13
        assert key_up["params"]["type"] == "keyUp"

    def test_press_key_arrow_down(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        _session_response(mock_ws)
        page.press_key("ArrowDown")
        calls = mock_ws.send.call_args_list
        key_down = json.loads(calls[-2][0][0])
        assert key_down["params"]["key"] == "ArrowDown"
        assert key_down["params"]["windowsVirtualKeyCode"] == 40

    def test_press_key_unknown(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        _session_response(mock_ws)
        page.press_key("Escape")
        calls = mock_ws.send.call_args_list
        key_down = json.loads(calls[-2][0][0])
        assert key_down["params"]["key"] == "Escape"
        assert key_down["params"]["code"] == "Escape"

    def test_type_text_sends_key_events(self):
        page, mock_ws = _make_real_page()
        # "ab" = 4 _send_session calls (keyDown+keyUp per char)
        for _ in range(4):
            _session_response(mock_ws)
        page.type_text("ab", delay_ms=0)
        calls = mock_ws.send.call_args_list
        # Verify the first keyDown has text "a"
        first = json.loads(calls[-4][0][0])
        assert first["params"]["type"] == "keyDown"
        assert first["params"]["text"] == "a"
        # Verify the third keyDown has text "b"
        third = json.loads(calls[-2][0][0])
        assert third["params"]["type"] == "keyDown"
        assert third["params"]["text"] == "b"


class TestPageEvaluate:
    """Test Page evaluate-based methods with real implementation."""

    def test_evaluate_function(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "number", "value": 42}})
        result = page.evaluate_function("() => { return 42; }")
        assert result == 42
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert "(() => { return 42; })()" in sent["params"]["expression"]

    def test_evaluate_function_raises_on_exception(self):
        page, mock_ws = _make_real_page()
        _session_response(
            mock_ws,
            {"result": {"type": "object"}, "exceptionDetails": {"text": "err"}},
        )
        with pytest.raises(CDPError, match="JS 函数执行异常"):
            page.evaluate_function("() => { throw 'err'; }")


class TestPageSelectors:
    """Test Page selector-based methods with real implementation."""

    def test_query_selector_returns_object_id(self):
        page, mock_ws = _make_real_page()
        _session_response(
            mock_ws,
            {"result": {"type": "object", "objectId": "obj-123"}},
        )
        oid = page.query_selector(".my-class")
        assert oid == "obj-123"

    def test_query_selector_returns_none_for_null(self):
        page, mock_ws = _make_real_page()
        _session_response(
            mock_ws,
            {"result": {"subtype": "null", "type": "object"}},
        )
        oid = page.query_selector(".missing")
        assert oid is None

    def test_query_selector_returns_none_for_undefined(self):
        page, mock_ws = _make_real_page()
        _session_response(
            mock_ws,
            {"result": {"type": "undefined"}},
        )
        oid = page.query_selector(".missing")
        assert oid is None

    def test_query_selector_all_returns_list(self):
        page, mock_ws = _make_real_page()
        # First call: evaluate returns count=2
        _session_response(mock_ws, {"result": {"type": "number", "value": 2}})
        # Second call: querySelectorAll[0]
        _session_response(
            mock_ws,
            {"result": {"type": "object", "objectId": "obj-0"}},
        )
        # Third call: querySelectorAll[1]
        _session_response(
            mock_ws,
            {"result": {"type": "object", "objectId": "obj-1"}},
        )
        oids = page.query_selector_all(".items")
        assert oids == ["obj-0", "obj-1"]

    def test_query_selector_all_empty(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "number", "value": 0}})
        oids = page.query_selector_all(".items")
        assert oids == []

    def test_get_element_attribute(self):
        page, mock_ws = _make_real_page()
        _session_response(
            mock_ws,
            {"result": {"type": "string", "value": "https://img.example.com/1.jpg"}},
        )
        val = page.get_element_attribute("img.hero", "src")
        assert val == "https://img.example.com/1.jpg"
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert "getAttribute" in sent["params"]["expression"]

    def test_get_element_attribute_returns_none(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "object", "subtype": "null"}})
        val = page.get_element_attribute(".missing", "href")
        assert val is None


class TestPageElementActions:
    """Test Page element action methods with real implementation."""

    def test_scroll_element_into_view(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.scroll_element_into_view(".target")
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert "scrollIntoView" in sent["params"]["expression"]

    def test_scroll_nth_element_into_view(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.scroll_nth_element_into_view(".items", 2)
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert "els[2]" in sent["params"]["expression"]

    def test_remove_element(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.remove_element(".overlay")
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert ".remove()" in sent["params"]["expression"]

    def test_hover_element_sends_mouse_move(self):
        page, mock_ws = _make_real_page()
        # evaluate returns center coords (JS already computes center)
        _session_response(
            mock_ws,
            {
                "result": {
                    "type": "object",
                    "value": {"x": 150, "y": 125},
                }
            },
        )
        # mouse_move call
        _session_response(mock_ws)
        page.hover_element(".card")
        # The last send should be the mouse move
        last_msg = json.loads(mock_ws.send.call_args_list[-1][0][0])
        assert last_msg["method"] == "Input.dispatchMouseEvent"
        assert last_msg["params"]["type"] == "mouseMoved"
        assert last_msg["params"]["x"] == 150
        assert last_msg["params"]["y"] == 125

    def test_hover_element_no_element(self):
        page, mock_ws = _make_real_page()
        # evaluate returns None (element not found)
        _session_response(
            mock_ws,
            {"result": {"type": "object", "subtype": "null"}},
        )
        page.hover_element(".missing")
        # Only one send call (the evaluate), no mouse move
        assert mock_ws.send.call_count == 1

    def test_dispatch_wheel_event(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.dispatch_wheel_event(100.0)
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert "WheelEvent" in sent["params"]["expression"]
        assert "100.0" in sent["params"]["expression"]


class TestPageFileInput:
    """Test Page.set_file_input with real implementation."""

    def test_set_file_input_success(self):
        page, mock_ws = _make_real_page()
        # DOM.getDocument
        _session_response(mock_ws, {"root": {"nodeId": 1}})
        # DOM.querySelector
        _session_response(mock_ws, {"nodeId": 5})
        # DOM.setFileInputFiles
        _session_response(mock_ws)
        page.set_file_input("input[type=file]", ["/a.jpg", "/b.jpg"])
        calls = mock_ws.send.call_args_list
        doc_msg = json.loads(calls[-3][0][0])
        assert doc_msg["method"] == "DOM.getDocument"
        query_msg = json.loads(calls[-2][0][0])
        assert query_msg["method"] == "DOM.querySelector"
        assert query_msg["params"]["nodeId"] == 1
        set_msg = json.loads(calls[-1][0][0])
        assert set_msg["method"] == "DOM.setFileInputFiles"
        assert set_msg["params"]["nodeId"] == 5
        assert set_msg["params"]["files"] == ["/a.jpg", "/b.jpg"]

    def test_set_file_input_not_found(self):
        page, mock_ws = _make_real_page()
        # DOM.getDocument
        _session_response(mock_ws, {"root": {"nodeId": 1}})
        # DOM.querySelector returns nodeId=0 (not found)
        _session_response(mock_ws, {"nodeId": 0})
        with pytest.raises(ElementNotFoundError):
            page.set_file_input("input[type=file]", ["/a.jpg"])


class TestPageNavigate:
    """Test Page.navigate with real implementation."""

    def test_navigate_sends_command(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        page.navigate("https://example.com")
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert sent["method"] == "Page.navigate"
        assert sent["params"]["url"] == "https://example.com"
        assert sent["sessionId"] == "session-1"


class TestPageSessionCommands:
    """Test Page _send_session plumbing."""

    def test_send_session_includes_session_id(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        page._send_session("Test.method", {"foo": "bar"})
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert sent["sessionId"] == "session-1"
        assert sent["method"] == "Test.method"
        assert sent["params"]["foo"] == "bar"
        assert sent["id"] == 1001

    def test_send_session_increments_id(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws)
        _session_response(mock_ws)
        page._send_session("A.method")
        page._send_session("B.method")
        first = json.loads(mock_ws.send.call_args_list[-2][0][0])
        second = json.loads(mock_ws.send.call_args_list[-1][0][0])
        assert first["id"] == 1001
        assert second["id"] == 1002

    def test_wait_session_raises_on_error(self):
        page, _mock_ws = _make_real_page()
        _response_queue.append(json.dumps({"id": 1001, "error": {"message": "fail"}}))
        with pytest.raises(CDPError, match="CDP 错误"):
            page._send_session("Test.method")

    def test_wait_session_timeout(self):
        page, mock_ws = _make_real_page()
        mock_ws.recv.side_effect = TimeoutError
        with pytest.raises(CDPError, match="超时"):
            page._send_session("Test.method")


class TestBrowserMethods:
    """Test Browser.close, get_existing_page, get_page_by_target_id."""

    def test_close(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://test")
            browser = Browser()
            browser._cdp = client
            browser.close()
            mock_ws.close.assert_called_once()
            assert browser._cdp is None

    def test_close_when_no_cdp(self):
        browser = Browser()
        browser._cdp = None
        browser.close()  # Should not raise

    @patch("xhs.cdp.requests.get")
    def test_get_existing_page_returns_non_blank(self, mock_get):
        version_resp = MagicMock()
        version_resp.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        version_resp.raise_for_status = MagicMock()
        targets_resp = MagicMock()
        targets_resp.json.return_value = [
            {"type": "page", "id": "t1", "url": "about:blank"},
            {"type": "page", "id": "t2", "url": "https://example.com"},
        ]
        mock_get.side_effect = [version_resp, targets_resp]
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            browser = Browser()
            browser.connect()
            # CDPClient.send for Target.attachToTarget
            # Page._send_session calls: Page.enable, DOM.enable, Runtime.enable
            mock_ws.recv.side_effect = [
                json.dumps({"id": 1, "result": {"sessionId": "sess-1"}}),
                json.dumps({"id": 1001, "result": {}}),
                json.dumps({"id": 1002, "result": {}}),
                json.dumps({"id": 1003, "result": {}}),
            ]
            page = browser.get_existing_page()
            assert page is not None
            assert page.target_id == "t2"
            assert page.session_id == "sess-1"

    @patch("xhs.cdp.requests.get")
    def test_get_existing_page_returns_none_when_only_blank(self, mock_get):
        version_resp = MagicMock()
        version_resp.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        version_resp.raise_for_status = MagicMock()
        targets_resp = MagicMock()
        targets_resp.json.return_value = [
            {"type": "page", "id": "t1", "url": "about:blank"},
        ]
        mock_get.side_effect = [version_resp, targets_resp]
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            browser = Browser()
            browser.connect()
            page = browser.get_existing_page()
            assert page is None

    @patch("xhs.cdp.requests.get")
    def test_get_page_by_target_id_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            browser = Browser()
            browser.connect()
            # CDPClient.send for Target.attachToTarget
            mock_ws.recv.side_effect = [
                json.dumps({"id": 1, "result": {"sessionId": "sess-x"}}),
                json.dumps({"id": 1001, "result": {}}),
                json.dumps({"id": 1002, "result": {}}),
                json.dumps({"id": 1003, "result": {}}),
            ]
            page = browser.get_page_by_target_id("target-x")
            assert page is not None
            assert page.target_id == "target-x"
            assert page.session_id == "sess-x"

    @patch("xhs.cdp.requests.get")
    def test_get_page_by_target_id_failure(self, mock_get):
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            browser = Browser()
            browser.connect()
            # CDPClient.send raises
            mock_ws.recv.return_value = json.dumps({"id": 1, "error": {"message": "not found"}})
            page = browser.get_page_by_target_id("bad-target")
            assert page is None

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_get_page_by_target_id_empty_session(self, mock_cdp_cls, mock_get):
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        mock_cdp = MagicMock()
        mock_cdp.send.return_value = {"sessionId": ""}
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        browser.connect()
        page = browser.get_page_by_target_id("target-x")
        assert page is None

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_get_page_by_target_id_auto_connects(self, mock_cdp_cls, mock_get):
        """get_page_by_target_id calls connect() when _cdp is None."""
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        mock_cdp = MagicMock()
        mock_cdp.send.return_value = {"sessionId": "sess-auto"}
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        # Don't call connect() explicitly — _cdp is None
        page = browser.get_page_by_target_id("target-auto")
        assert page is not None
        assert page.target_id == "target-auto"


class TestWaitForLoad:
    """Test Page.wait_for_load polling logic.

    _wait_session uses time.monotonic() 3x per call (deadline, while-check,
    recv-timeout), so each evaluate() inside the loop costs 3 monotonic calls
    plus 1 for the loop's own while-check = 4 per iteration.
    """

    def test_returns_when_complete_immediately(self):
        page, mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # 1(deadline) + 1(while) + 3(_wait_session) = 5
            mock_time.monotonic.side_effect = [0.0] * 5
            _session_response(
                mock_ws,
                {"result": {"type": "string", "value": "complete"}},
            )
            page.wait_for_load()
            mock_time.sleep.assert_not_called()

    def test_loops_through_loading_then_complete(self):
        page, mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # 1(deadline) + 2 iterations * (1+3) = 9
            mock_time.monotonic.side_effect = [0.0] * 9
            _session_response(
                mock_ws,
                {"result": {"type": "string", "value": "loading"}},
            )
            _session_response(
                mock_ws,
                {"result": {"type": "string", "value": "complete"}},
            )
            page.wait_for_load()
            mock_time.sleep.assert_called_once_with(0.5)

    def test_handles_cdp_error_and_continues(self):
        page, _mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # 1(deadline) + 2 iterations * (1+3) = 9
            mock_time.monotonic.side_effect = [0.0] * 9
            # First evaluate: CDPError (id 1001)
            _response_queue.append(json.dumps({"id": 1001, "error": {"message": "fail"}}))
            # Second evaluate: complete (id 1002)
            _response_queue.append(
                json.dumps(
                    {
                        "id": 1002,
                        "result": {"result": {"type": "string", "value": "complete"}},
                    }
                )
            )
            page.wait_for_load()
            mock_time.sleep.assert_called_once_with(0.5)

    def test_timeout_logs_warning(self):
        page, mock_ws = _make_real_page()
        with (
            patch("xhs.cdp.time") as mock_time,
            patch("xhs.cdp.logger") as mock_logger,
        ):
            # 1(deadline) + 1 iteration*(1+3) + 1(exit-while) = 6
            # Last call returns large value to exceed deadline
            mock_time.monotonic.side_effect = [0.0] * 5 + [100.0]
            _session_response(
                mock_ws,
                {"result": {"type": "string", "value": "loading"}},
            )
            page.wait_for_load(timeout=60.0)
            mock_logger.warning.assert_called_once()


class TestWaitDomStable:
    """Test Page.wait_dom_stable polling logic.

    Same monotonic budgeting as wait_for_load: 1(deadline) + N*(1+3).
    """

    def test_returns_when_two_snapshots_match(self):
        page, mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # 1 + 2*(1+3) = 9
            mock_time.monotonic.side_effect = [0.0] * 9
            _session_response(mock_ws, {"result": {"type": "number", "value": 100}})
            _session_response(mock_ws, {"result": {"type": "number", "value": 100}})
            page.wait_dom_stable()
            mock_time.sleep.assert_called_once_with(0.5)

    def test_handles_cdp_error_and_continues(self):
        page, _mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # 1 + 3*(1+3) = 13
            mock_time.monotonic.side_effect = [0.0] * 13
            # First: CDPError (id 1001)
            _response_queue.append(json.dumps({"id": 1001, "error": {"message": "fail"}}))
            # Second: value 50 (id 1002)
            _response_queue.append(
                json.dumps(
                    {
                        "id": 1002,
                        "result": {"result": {"type": "number", "value": 50}},
                    }
                )
            )
            # Third: same value 50 -> stable (id 1003)
            _response_queue.append(
                json.dumps(
                    {
                        "id": 1003,
                        "result": {"result": {"type": "number", "value": 50}},
                    }
                )
            )
            page.wait_dom_stable()
            assert mock_time.sleep.call_count == 2

    def test_timeout_returns_silently(self):
        page, mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # 1 + 1*(1+3) + 1(exit) = 6
            mock_time.monotonic.side_effect = [0.0] * 5 + [100.0]
            _session_response(mock_ws, {"result": {"type": "number", "value": 100}})
            page.wait_dom_stable(timeout=10.0)
            # Should return without raising


class TestClickElementReal:
    """Test Page.click_element with real implementation."""

    def test_click_with_valid_rect(self):
        page, mock_ws = _make_real_page()
        with (
            patch("xhs.cdp.random") as mock_random,
            patch("xhs.cdp.time") as mock_time,
        ):
            # 4 _send_session calls * 3 monotonic each = 12
            mock_time.monotonic.side_effect = [0.0] * 12
            # x offset, y offset, sleep duration
            mock_random.uniform.side_effect = [2.0, 1.0, 0.05]
            # evaluate returns rect coords
            _session_response(
                mock_ws,
                {
                    "result": {
                        "type": "object",
                        "value": {"x": 100, "y": 200},
                    }
                },
            )
            # mouse_move
            _session_response(mock_ws)
            # mouse_click: mousePressed + mouseReleased
            _session_response(mock_ws)
            _session_response(mock_ws)
            page.click_element(".button")
            calls = mock_ws.send.call_args_list
            # Verify mouse_move call (3rd from last)
            move_msg = json.loads(calls[-3][0][0])
            assert move_msg["method"] == "Input.dispatchMouseEvent"
            assert move_msg["params"]["type"] == "mouseMoved"
            assert move_msg["params"]["x"] == 102.0
            assert move_msg["params"]["y"] == 201.0
            mock_time.sleep.assert_called_once_with(0.05)

    def test_click_element_not_found(self):
        page, mock_ws = _make_real_page()
        # evaluate returns null (element not found)
        _session_response(
            mock_ws,
            {"result": {"type": "object", "subtype": "null"}},
        )
        page.click_element(".missing")
        # Only one send call (the evaluate), no mouse events
        assert mock_ws.send.call_count == 1


class TestInputTextReal:
    """Test Page.input_text with real implementation."""

    def test_input_text_sends_evaluate_with_js(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.input_text("#name", "hello")
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert sent["method"] == "Runtime.evaluate"
        expr = sent["params"]["expression"]
        assert "hello" in expr
        assert "el.focus()" in expr
        assert "el.value" in expr
        assert "input" in expr
        assert "change" in expr


class TestSelectAllText:
    """Test Page.select_all_text with real implementation."""

    def test_select_all_text_sends_evaluate(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"result": {"type": "undefined"}})
        page.select_all_text("input[type=text]")
        sent = json.loads(mock_ws.send.call_args[0][0])
        assert sent["method"] == "Runtime.evaluate"
        assert "el.select()" in sent["params"]["expression"]


class TestScreenshotElement:
    """Test Page.screenshot_element with real implementation."""

    def test_screenshot_success(self):
        import base64 as _b64

        page, mock_ws = _make_real_page()
        fake_png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 10
        fake_b64 = _b64.b64encode(fake_png).decode()
        # DOM.getDocument
        _session_response(mock_ws, {"root": {"nodeId": 1}})
        # DOM.querySelector
        _session_response(mock_ws, {"nodeId": 5})
        # DOM.getBoxModel
        _session_response(
            mock_ws,
            {
                "model": {
                    "content": [10, 20, 110, 20, 110, 120, 10, 120],
                    "width": 100,
                    "height": 100,
                }
            },
        )
        # Page.captureScreenshot
        _session_response(mock_ws, {"data": fake_b64})
        result = page.screenshot_element(".target")
        assert result == fake_png
        calls = mock_ws.send.call_args_list
        screenshot_msg = json.loads(calls[-1][0][0])
        assert screenshot_msg["method"] == "Page.captureScreenshot"
        clip = screenshot_msg["params"]["clip"]
        assert clip["x"] == 10.0
        assert clip["y"] == 20.0
        assert clip["width"] == 100.0
        assert clip["height"] == 100.0

    def test_screenshot_with_padding(self):
        import base64 as _b64

        page, mock_ws = _make_real_page()
        fake_b64 = _b64.b64encode(b"png").decode()
        _session_response(mock_ws, {"root": {"nodeId": 1}})
        _session_response(mock_ws, {"nodeId": 5})
        _session_response(
            mock_ws,
            {
                "model": {
                    "content": [10, 20, 110, 20, 110, 120, 10, 120],
                    "width": 100,
                    "height": 100,
                }
            },
        )
        _session_response(mock_ws, {"data": fake_b64})
        page.screenshot_element(".target", padding=5)
        calls = mock_ws.send.call_args_list
        clip = json.loads(calls[-1][0][0])["params"]["clip"]
        assert clip["x"] == 5.0  # max(0, 10-5)
        assert clip["y"] == 15.0  # max(0, 20-5)
        assert clip["width"] == 110.0  # 100 + 5*2
        assert clip["height"] == 110.0

    def test_screenshot_element_not_found(self):
        page, mock_ws = _make_real_page()
        _session_response(mock_ws, {"root": {"nodeId": 1}})
        _session_response(mock_ws, {"nodeId": 0})
        result = page.screenshot_element(".missing")
        assert result == b""

    def test_screenshot_cdp_error_returns_empty(self):
        page, _mock_ws = _make_real_page()
        # DOM.getDocument raises CDPError
        _response_queue.append(json.dumps({"id": 1001, "error": {"message": "fail"}}))
        result = page.screenshot_element(".target")
        assert result == b""


class TestTypeTextWithDelay:
    """Test Page.type_text with delay_ms > 0."""

    def test_type_text_sleeps_between_chars(self):
        page, mock_ws = _make_real_page()
        with patch("xhs.cdp.time") as mock_time:
            # "ab" = 4 _send_session calls * 3 monotonic each = 12
            mock_time.monotonic.side_effect = [0.0] * 12
            for _ in range(4):
                _session_response(mock_ws)
            page.type_text("ab", delay_ms=50)
            assert mock_time.sleep.call_count == 2
            mock_time.sleep.assert_called_with(0.05)


class TestEvaluateException:
    """Test Page.evaluate raises on exceptionDetails."""

    def test_evaluate_raises_on_exception_details(self):
        page, mock_ws = _make_real_page()
        _session_response(
            mock_ws,
            {
                "result": {"type": "object"},
                "exceptionDetails": {"text": "SyntaxError"},
            },
        )
        with pytest.raises(CDPError, match="JS 执行异常"):
            page.evaluate("invalid JS")


class TestBrowserGetOrCreatePage:
    """Test Browser.get_or_create_page with real implementation."""

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_reuses_blank_tab(self, mock_cdp_cls, mock_get):
        version_resp = MagicMock()
        version_resp.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        version_resp.raise_for_status = MagicMock()
        targets_resp = MagicMock()
        targets_resp.json.return_value = [
            {"type": "page", "id": "t1", "url": "about:blank"},
            {"type": "page", "id": "t2", "url": "https://example.com"},
        ]
        mock_get.side_effect = [version_resp, targets_resp]
        mock_cdp = MagicMock()
        mock_cdp.send.return_value = {"sessionId": "sess-reuse"}
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        browser.connect()
        page = browser.get_or_create_page()
        assert page is not None
        assert page.target_id == "t1"
        assert page.session_id == "sess-reuse"

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_creates_new_when_no_blank_tab(self, mock_cdp_cls, mock_get):
        version_resp = MagicMock()
        version_resp.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        version_resp.raise_for_status = MagicMock()
        targets_resp = MagicMock()
        targets_resp.json.return_value = [
            {"type": "page", "id": "t2", "url": "https://example.com"},
        ]
        mock_get.side_effect = [version_resp, targets_resp]
        mock_cdp = MagicMock()
        mock_cdp.send.side_effect = [
            {"targetId": "new-target"},
            {"sessionId": "new-session"},
        ]
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        browser.connect()
        page = browser.get_or_create_page()
        assert page is not None
        assert page.target_id == "new-target"
        assert page.session_id == "new-session"

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_creates_new_when_attach_fails(self, mock_cdp_cls, mock_get):
        version_resp = MagicMock()
        version_resp.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        version_resp.raise_for_status = MagicMock()
        targets_resp = MagicMock()
        targets_resp.json.return_value = [
            {"type": "page", "id": "t1", "url": "about:blank"},
        ]
        mock_get.side_effect = [version_resp, targets_resp]
        mock_cdp = MagicMock()
        # First send (attach) raises, then new_page sends
        mock_cdp.send.side_effect = [
            Exception("attach failed"),
            {"targetId": "new-target"},
            {"sessionId": "new-session"},
        ]
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        browser.connect()
        page = browser.get_or_create_page()
        assert page is not None
        assert page.target_id == "new-target"

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_auto_connects_when_cdp_is_none(self, mock_cdp_cls, mock_get):
        """get_or_create_page calls connect() when _cdp is None."""
        version_resp = MagicMock()
        version_resp.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        version_resp.raise_for_status = MagicMock()
        targets_resp = MagicMock()
        targets_resp.json.return_value = [
            {"type": "page", "id": "t1", "url": "https://example.com"},
        ]
        mock_get.side_effect = [version_resp, targets_resp]
        mock_cdp = MagicMock()
        mock_cdp.send.side_effect = [
            {"targetId": "new-t"},
            {"sessionId": "new-s"},
        ]
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        # Don't call connect() — let get_or_create_page do it
        page = browser.get_or_create_page()
        assert page is not None


class TestBrowserSetupPage:
    """Test Browser._setup_page enables CDP domains."""

    @patch("xhs.cdp.requests.get")
    @patch("xhs.cdp.CDPClient")
    def test_setup_page_enables_domains(self, mock_cdp_cls, mock_get):
        mock_get.return_value.json.return_value = {
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools",
            "Browser": "Chrome/134.0.6998.88",
        }
        mock_cdp = MagicMock()
        mock_ws = MagicMock()
        mock_ws.recv.side_effect = [
            json.dumps({"id": 1001, "result": {}}),
            json.dumps({"id": 1002, "result": {}}),
            json.dumps({"id": 1003, "result": {}}),
        ]
        mock_cdp._ws = mock_ws
        mock_cdp_cls.return_value = mock_cdp
        browser = Browser()
        browser.connect()
        page = Page(mock_cdp, "target-1", "session-1")
        result = browser._setup_page(page)
        assert result is page
        calls = mock_ws.send.call_args_list
        methods = [json.loads(c[0][0])["method"] for c in calls]
        assert "Page.enable" in methods
        assert "DOM.enable" in methods
        assert "Runtime.enable" in methods


class TestBrowserClosePage:
    """Test Browser.close_page."""

    def test_close_page_with_cdp(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://test")
            browser = Browser()
            browser._cdp = client
            with patch.object(client, "send") as mock_send:
                page = Page(client, "target-1", "session-1")
                browser.close_page(page)
                mock_send.assert_called_once_with("Target.closeTarget", {"targetId": "target-1"})

    def test_close_page_without_cdp(self):
        browser = Browser()
        browser._cdp = None
        page = MagicMock()
        page.target_id = "target-1"
        browser.close_page(page)  # Should not raise

    def test_close_page_suppresses_cdp_error(self):
        with patch("xhs.cdp.ws_client.connect") as mock_connect:
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            client = CDPClient("ws://test")
            browser = Browser()
            browser._cdp = client
            with patch.object(client, "send", side_effect=CDPError("close failed")):
                page = Page(client, "target-1", "session-1")
                browser.close_page(page)  # Should not raise
