"""xhs 模块专用测试 fixtures。"""

from __future__ import annotations

from unittest.mock import MagicMock, create_autospec

import pytest
from xhs.cdp import Page


@pytest.fixture
def mock_page():
    """模拟 cdp.Page 对象，自动生成所有方法存根。"""
    page = create_autospec(Page, instance=True)
    page.target_id = "test-target-id"
    page.session_id = "test-session-id"
    return page


@pytest.fixture
def mock_bridge_page():
    """模拟 bridge.BridgePage 对象。"""
    from xhs.bridge import BridgePage

    page = MagicMock(spec=BridgePage)
    page.evaluate.return_value = ""
    page.has_element.return_value = False
    page.is_server_running.return_value = True
    page.is_extension_connected.return_value = True
    return page
