# 测试覆盖实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 xhs-automator 项目建立全面的测试覆盖，使用纯 mock 策略，目标行覆盖率 ≥90%

**Architecture:** 采用模块镜像结构，tests/ 目录与 scripts/ 保持一致。所有功能模块使用 `create_autospec(Page)` 模拟 CDP Page 对象，通过 `autouse` fixture 自动 mock `time.sleep` 加速测试。

**Tech Stack:** pytest, pytest-cov, unittest.mock

**Spec:** `docs/product-specs/2026-05-01-test-coverage-design.md`

---

## Task 1: 基础设施配置

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/__init__.py`
- Create: `tests/xhs/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/xhs/conftest.py`

- [ ] **Step 1: 更新 pyproject.toml 添加测试依赖**

在 `[project.optional-dependencies] dev` 和 `[dependency-groups] dev` 中添加 `pytest-cov>=5.0`：

```toml
[project.optional-dependencies]
dev = [
    "ruff>=0.9.0",
    "pytest>=9.0.2",
    "pytest-cov>=5.0",
]

[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-cov>=5.0",
]
```

- [ ] **Step 2: 添加 pytest 和 coverage 配置**

在 `pyproject.toml` 末尾添加：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["scripts"]

[tool.coverage.run]
source = ["scripts"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.",
    "if sys.platform",
    "platform.system()",
    "raise NotImplementedError",
]
omit = [
    "scripts/xhs/__init__.py",
    "scripts/bridge_server.py",
    "scripts/validate_agents_docs.py",
]
```

- [ ] **Step 3: 创建 tests/__init__.py**

```python
```

（空文件）

- [ ] **Step 4: 创建 tests/xhs/__init__.py**

```python
```

（空文件）

- [ ] **Step 5: 创建 tests/conftest.py**

```python
"""共享测试 fixtures。"""

from __future__ import annotations

import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_sleep():
    """自动 mock time.sleep，加速测试。"""
    with patch("time.sleep"):
        yield


@pytest.fixture
def sample_feed_data():
    """示例 Feed 数据。"""
    return {
        "id": "test_feed_id",
        "noteCard": {
            "displayTitle": "测试标题",
            "user": {"userId": "user123", "nickname": "测试用户"},
            "interactInfo": {"likedCount": "100", "commentCount": "50"},
        },
    }


@pytest.fixture
def tmp_cookies(tmp_path):
    """临时 Cookie 文件。"""
    cookie_file = tmp_path / "cookies.json"
    cookie_file.write_bytes(b'{"cookies": []}')
    return str(cookie_file)
```

- [ ] **Step 6: 创建 tests/xhs/conftest.py**

```python
"""xhs 模块专用测试 fixtures。"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, create_autospec

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
```

- [ ] **Step 7: 安装依赖并验证**

Run: `uv sync`
Run: `uv run pytest --co` (收集测试，应显示 0 tests collected)

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml tests/__init__.py tests/xhs/__init__.py tests/conftest.py tests/xhs/conftest.py
git commit -m "test: 添加测试基础设施配置"
```

---

## Task 2: test_selectors.py — CSS 选择器常量测试

**Files:**
- Create: `tests/xhs/test_selectors.py`
- Read: `scripts/xhs/selectors.py`

- [ ] **Step 1: 编写测试**

```python
"""CSS 选择器常量测试。"""

from __future__ import annotations

from xhs import selectors


class TestSelectorsExist:
    """验证所有选择器常量存在且非空。"""

    def test_login_selectors(self):
        assert selectors.LOGIN_STATUS
        assert selectors.QRCODE_IMG

    def test_phone_login_selectors(self):
        assert selectors.LOGIN_CONTAINER
        assert selectors.PHONE_INPUT
        assert selectors.GET_CODE_BUTTON
        assert selectors.CODE_INPUT
        assert selectors.PHONE_LOGIN_SUBMIT
        assert selectors.AGREE_CHECKBOX
        assert selectors.LOGIN_ERR_MSG

    def test_feed_selectors(self):
        assert selectors.FILTER_BUTTON
        assert selectors.FILTER_PANEL

    def test_comment_selectors(self):
        assert selectors.COMMENTS_CONTAINER
        assert selectors.PARENT_COMMENT
        assert selectors.COMMENT_INPUT_TRIGGER
        assert selectors.COMMENT_INPUT_FIELD
        assert selectors.COMMENT_SUBMIT_BUTTON

    def test_like_favorite_selectors(self):
        assert selectors.LIKE_BUTTON
        assert selectors.COLLECT_BUTTON

    def test_publish_selectors(self):
        assert selectors.UPLOAD_CONTENT
        assert selectors.CREATOR_TAB
        assert selectors.UPLOAD_INPUT
        assert selectors.FILE_INPUT
        assert selectors.TITLE_INPUT
        assert selectors.CONTENT_EDITOR
        assert selectors.PUBLISH_BUTTON

    def test_user_profile_selectors(self):
        assert selectors.SIDEBAR_PROFILE
        assert selectors.USER_PROFILE_NAV_LINK
        assert selectors.USER_NICKNAME
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_selectors.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_selectors.py
git commit -m "test: 添加 selectors 模块测试"
```

---

## Task 3: test_types.py — 数据类型测试

**Files:**
- Create: `tests/xhs/test_types.py`
- Read: `scripts/xhs/types.py`

- [ ] **Step 1: 编写测试**

```python
"""数据类型测试。"""

from __future__ import annotations

from xhs.types import (
    ActionResult,
    CommentLoadConfig,
    Cover,
    Feed,
    FeedDetail,
    FilterOption,
    ImageInfo,
    InteractInfo,
    PublishImageContent,
    User,
    Video,
    VideoCapability,
)


class TestImageInfo:
    def test_from_dict(self):
        d = {"imageScene": "test_scene", "url": "https://example.com/img.jpg"}
        info = ImageInfo.from_dict(d)
        assert info.image_scene == "test_scene"
        assert info.url == "https://example.com/img.jpg"

    def test_from_dict_empty(self):
        info = ImageInfo.from_dict({})
        assert info.image_scene == ""
        assert info.url == ""


class TestVideoCapability:
    def test_from_dict(self):
        cap = VideoCapability.from_dict({"duration": 120})
        assert cap.duration == 120

    def test_from_dict_default(self):
        cap = VideoCapability.from_dict({})
        assert cap.duration == 0


class TestVideo:
    def test_from_dict(self):
        v = Video.from_dict({"capa": {"duration": 60}})
        assert v.capa.duration == 60


class TestCover:
    def test_from_dict(self):
        d = {
            "width": 1080,
            "height": 720,
            "url": "https://example.com/cover.jpg",
            "fileId": "file123",
            "urlPre": "https://example.com/pre.jpg",
            "urlDefault": "https://example.com/default.jpg",
            "infoList": [{"imageScene": "scene1", "url": "url1"}],
        }
        cover = Cover.from_dict(d)
        assert cover.width == 1080
        assert cover.height == 720
        assert cover.file_id == "file123"
        assert len(cover.info_list) == 1


class TestUser:
    def test_from_dict(self):
        d = {"userId": "u123", "nickname": "测试用户", "nickName": "昵称", "avatar": "av.jpg"}
        user = User.from_dict(d)
        assert user.user_id == "u123"
        assert user.nickname == "测试用户"

    def test_from_dict_empty(self):
        user = User.from_dict({})
        assert user.user_id == ""


class TestInteractInfo:
    def test_from_dict(self):
        d = {"liked": True, "likedCount": "100", "collected": False}
        info = InteractInfo.from_dict(d)
        assert info.liked is True
        assert info.liked_count == "100"
        assert info.collected is False


class TestFeed:
    def test_from_dict(self, sample_feed_data):
        feed = Feed.from_dict(sample_feed_data)
        assert feed.id == "test_feed_id"
        assert feed.note_card.display_title == "测试标题"

    def test_to_dict(self, sample_feed_data):
        feed = Feed.from_dict(sample_feed_data)
        d = feed.to_dict()
        assert d["id"] == "test_feed_id"


class TestFilterOption:
    def test_default(self):
        opt = FilterOption()
        assert opt.sort_by == ""
        assert opt.note_type == ""


class TestPublishImageContent:
    def test_default(self):
        content = PublishImageContent(title="标题", content="内容", image_paths=["a.jpg"])
        assert content.title == "标题"
        assert content.tags == []


class TestActionResult:
    def test_creation(self):
        result = ActionResult(feed_id="f1", success=True, message="ok")
        assert result.success is True
        assert result.to_dict()["feed_id"] == "f1"


class TestCommentLoadConfig:
    def test_default(self):
        config = CommentLoadConfig()
        assert config.click_more_replies is False
        assert config.max_replies_threshold == 10
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_types.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_types.py
git commit -m "test: 添加 types 模块测试"
```

---

## Task 4: test_errors.py — 异常体系测试

**Files:**
- Create: `tests/xhs/test_errors.py`
- Read: `scripts/xhs/errors.py`

- [ ] **Step 1: 编写测试**

```python
"""异常体系测试。"""

from __future__ import annotations

import pytest

from xhs.errors import (
    CDPError,
    ContentTooLongError,
    ElementNotFoundError,
    NoFeedDetailError,
    NoFeedsError,
    NotLoggedInError,
    PageNotAccessibleError,
    PublishError,
    RateLimitError,
    TitleTooLongError,
    UploadTimeoutError,
    XHSError,
)


class TestExceptionHierarchy:
    """验证异常继承链。"""

    def test_all_inherit_xhs_error(self):
        exceptions = [
            NoFeedsError,
            NoFeedDetailError,
            NotLoggedInError,
            PageNotAccessibleError("reason"),
            UploadTimeoutError,
            PublishError,
            TitleTooLongError("10", "20"),
            ContentTooLongError("10", "20"),
            RateLimitError,
            CDPError,
            ElementNotFoundError("sel"),
        ]
        for exc in exceptions:
            assert isinstance(exc, XHSError)
            assert isinstance(exc, Exception)

    def test_title_too_long_inherits_publish_error(self):
        exc = TitleTooLongError("10", "20")
        assert isinstance(exc, PublishError)

    def test_content_too_long_inherits_publish_error(self):
        exc = ContentTooLongError("10", "20")
        assert isinstance(exc, PublishError)


class TestExceptionMessages:
    """验证异常消息格式。"""

    def test_no_feeds_error(self):
        exc = NoFeedsError()
        assert "feeds" in str(exc)

    def test_not_logged_in_error(self):
        exc = NotLoggedInError()
        assert "未登录" in str(exc)

    def test_page_not_accessible(self):
        exc = PageNotAccessibleError("违规删除")
        assert "违规删除" in str(exc)
        assert exc.reason == "违规删除"

    def test_title_too_long(self):
        exc = TitleTooLongError("50", "20")
        assert "50" in str(exc)
        assert "20" in str(exc)
        assert exc.current == "50"
        assert exc.maximum == "20"

    def test_rate_limit_error(self):
        exc = RateLimitError()
        assert "频繁" in str(exc)

    def test_element_not_found(self):
        exc = ElementNotFoundError(".my-selector")
        assert ".my-selector" in str(exc)
        assert exc.selector == ".my-selector"
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_errors.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_errors.py
git commit -m "test: 添加 errors 模块测试"
```

---

## Task 5: test_urls.py — URL 构建测试

**Files:**
- Create: `tests/xhs/test_urls.py`
- Read: `scripts/xhs/urls.py`

- [ ] **Step 1: 编写测试**

```python
"""URL 构建函数测试。"""

from __future__ import annotations

from xhs.urls import (
    EXPLORE_URL,
    HOME_URL,
    PUBLISH_URL,
    make_feed_detail_url,
    make_search_url,
    make_user_profile_url,
)


class TestConstants:
    def test_explore_url(self):
        assert "xiaohongshu.com/explore" in EXPLORE_URL

    def test_home_url(self):
        assert "xiaohongshu.com" in HOME_URL

    def test_publish_url(self):
        assert "creator.xiaohongshu.com" in PUBLISH_URL


class TestMakeFeedDetailUrl:
    def test_basic(self):
        url = make_feed_detail_url("feed123", "token456")
        assert "feed123" in url
        assert "token456" in url
        assert "xsec_token=token456" in url
        assert "xsec_source=pc_feed" in url

    def test_special_characters(self):
        url = make_feed_detail_url("id/with/slash", "token+special")
        assert "id/with/slash" in url


class TestMakeSearchUrl:
    def test_basic(self):
        url = make_search_url("关键词")
        assert "keyword=" in url
        assert "source=web_explore_feed" in url

    def test_chinese_keyword(self):
        url = make_search_url("小红书")
        assert "小红书" in url or "%E5%B0%8F" in url


class TestMakeUserProfileUrl:
    def test_basic(self):
        url = make_user_profile_url("user123", "token456")
        assert "user/profile/user123" in url
        assert "xsec_token=token456" in url
        assert "xsec_source=pc_note" in url
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_urls.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_urls.py
git commit -m "test: 添加 urls 模块测试"
```

---

## Task 6: test_human.py — 行为模拟测试

**Files:**
- Create: `tests/xhs/test_human.py`
- Read: `scripts/xhs/human.py`

- [ ] **Step 1: 编写测试**

```python
"""人类行为模拟测试。"""

from __future__ import annotations

from unittest.mock import patch

from xhs.human import (
    INACCESSIBLE_KEYWORDS,
    calculate_scroll_delta,
    get_scroll_interval,
    get_scroll_ratio,
    sleep_random,
)


class TestSleepRandom:
    @patch("xhs.human.time.sleep")
    def test_within_range(self, mock_sleep):
        sleep_random(100, 200)
        mock_sleep.assert_called_once()
        delay = mock_sleep.call_args[0][0]
        assert 0.1 <= delay <= 0.2

    @patch("xhs.human.time.sleep")
    def test_equal_min_max(self, mock_sleep):
        sleep_random(100, 100)
        mock_sleep.assert_called_once()
        delay = mock_sleep.call_args[0][0]
        assert delay == 0.1


class TestGetScrollInterval:
    def test_slow(self):
        interval = get_scroll_interval("slow")
        assert 1.2 <= interval <= 1.5

    def test_normal(self):
        interval = get_scroll_interval("normal")
        assert 0.6 <= interval <= 0.8

    def test_fast(self):
        interval = get_scroll_interval("fast")
        assert 0.3 <= interval <= 0.4


class TestGetScrollRatio:
    def test_slow(self):
        assert get_scroll_ratio("slow") == 0.5

    def test_normal(self):
        assert get_scroll_ratio("normal") == 0.7

    def test_fast(self):
        assert get_scroll_ratio("fast") == 0.9


class TestCalculateScrollDelta:
    def test_minimum_delta(self):
        # viewport=100, ratio=0.1 → 100*(0.1+rand*0.2) ≈ 10-30, clamped to 400, then ±50 jitter
        delta = calculate_scroll_delta(100, 0.1)
        assert delta >= 350  # 400 - 50 jitter

    def test_normal_delta(self):
        # viewport=1000, ratio=0.7 → 1000*(0.7+rand*0.2) ≈ 700-900, then ±50 jitter
        delta = calculate_scroll_delta(1000, 0.7)
        assert 650 <= delta <= 950


class TestInaccessibleKeywords:
    def test_not_empty(self):
        assert len(INACCESSIBLE_KEYWORDS) > 0

    def test_contains_expected(self):
        assert "私密笔记" in INACCESSIBLE_KEYWORDS
        assert "已失效" in INACCESSIBLE_KEYWORDS
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_human.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_human.py
git commit -m "test: 添加 human 模块测试"
```

---

## Task 7: test_cookies.py — Cookie 持久化测试

**Files:**
- Create: `tests/xhs/test_cookies.py`
- Read: `scripts/xhs/cookies.py`

- [ ] **Step 1: 编写测试**

```python
"""Cookie 持久化测试。"""

from __future__ import annotations

import os
from unittest.mock import patch

from xhs.cookies import delete_cookies, get_cookies_file_path, load_cookies, save_cookies


class TestGetCookiesFilePath:
    def test_with_account(self):
        path = get_cookies_file_path("test_account")
        assert "test_account" in path
        assert path.endswith("cookies.json")

    def test_env_variable(self):
        with patch.dict(os.environ, {"COOKIES_PATH": "/tmp/test_cookies.json"}):
            path = get_cookies_file_path()
            assert path == "/tmp/test_cookies.json"

    def test_default_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("tempfile.gettempdir", return_value="/fake_tmp"):
                with patch("os.path.exists", return_value=False):
                    path = get_cookies_file_path()
                    assert path == "cookies.json"


class TestCookieFileOperations:
    def test_save_and_load(self, tmp_path):
        cookie_file = str(tmp_path / "test_cookies.json")
        data = b'{"cookies": [{"name": "test"}]}'
        save_cookies(cookie_file, data)
        loaded = load_cookies(cookie_file)
        assert loaded == data

    def test_load_nonexistent(self):
        result = load_cookies("/nonexistent/path/cookies.json")
        assert result is None

    def test_delete_cookies(self, tmp_path):
        cookie_file = str(tmp_path / "test_cookies.json")
        save_cookies(cookie_file, b"test")
        assert os.path.exists(cookie_file)
        delete_cookies(cookie_file)
        assert not os.path.exists(cookie_file)

    def test_delete_nonexistent(self):
        # 不应抛出异常
        delete_cookies("/nonexistent/path/cookies.json")
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_cookies.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_cookies.py
git commit -m "test: 添加 cookies 模块测试"
```

---

## Task 8: test_title_utils.py — 标题工具测试

**Files:**
- Create: `tests/test_title_utils.py`
- Read: `scripts/title_utils.py`

- [ ] **Step 1: 编写测试**

```python
"""标题工具测试。"""

from __future__ import annotations

from title_utils import calc_title_length, truncate_title


class TestCalcTitleLength:
    def test_ascii(self):
        assert calc_title_length("hello") == 5

    def test_chinese(self):
        # 中文字符在 UTF-16 中占 2 字节，calc_title_length 返回字节数/2
        length = calc_title_length("你好")
        assert length >= 2

    def test_empty(self):
        assert calc_title_length("") == 0

    def test_mixed(self):
        length = calc_title_length("hello你好")
        assert length > 5


class TestTruncateTitle:
    def test_short_title(self):
        title = "短标题"
        result = truncate_title(title, 20)
        assert result == title

    def test_long_title(self):
        title = "这是一个很长的标题" * 10
        result = truncate_title(title, 10)
        assert calc_title_length(result) <= 10

    def test_empty_title(self):
        result = truncate_title("", 10)
        assert result == ""
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/test_title_utils.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_title_utils.py
git commit -m "test: 添加 title_utils 模块测试"
```

---

## Task 9: test_run_lock.py — 单实例锁测试

**Files:**
- Create: `tests/test_run_lock.py`
- Read: `scripts/run_lock.py`

- [ ] **Step 1: 编写测试**

```python
"""单实例锁测试。"""

from __future__ import annotations

import os
from unittest.mock import patch

from run_lock import RunLock


class TestRunLock:
    def test_acquire_and_release(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        lock = RunLock(lock_file)
        assert lock.acquire() is True
        assert os.path.exists(lock_file)
        lock.release()
        assert not os.path.exists(lock_file)

    def test_double_acquire(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        lock = RunLock(lock_file)
        assert lock.acquire() is True
        # 第二次获取应该失败（锁已存在）
        lock2 = RunLock(lock_file)
        assert lock2.acquire() is False
        lock.release()

    def test_context_manager(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        with RunLock(lock_file) as lock:
            assert os.path.exists(lock_file)
        assert not os.path.exists(lock_file)

    def test_stale_lock_cleanup(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        # 创建一个过期的锁文件
        with open(lock_file, "w") as f:
            f.write("999999999")  # 不存在的 PID
        lock = RunLock(lock_file)
        # 应该能获取到锁（清理过期锁）
        assert lock.acquire() is True
        lock.release()
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/test_run_lock.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_run_lock.py
git commit -m "test: 添加 run_lock 模块测试"
```

---

## Task 10: test_bridge.py — Bridge 通信测试

**Files:**
- Create: `tests/xhs/test_bridge.py`
- Read: `scripts/xhs/bridge.py`

- [ ] **Step 1: 编写测试**

```python
"""Bridge 通信测试。"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from xhs.bridge import BridgePage
from xhs.errors import CDPError


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
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_bridge.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_bridge.py
git commit -m "test: 添加 bridge 模块测试"
```

---

## Task 11: test_cdp.py — CDP 客户端测试

**Files:**
- Create: `tests/xhs/test_cdp.py`
- Read: `scripts/xhs/cdp.py`

- [ ] **Step 1: 编写测试**

```python
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
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_cdp.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_cdp.py
git commit -m "test: 添加 cdp 模块测试"
```

---

## Task 12: test_login.py — 登录模块测试

**Files:**
- Create: `tests/xhs/test_login.py`
- Read: `scripts/xhs/login.py`

- [ ] **Step 1: 编写测试**

```python
"""登录模块测试。"""

from __future__ import annotations

import base64
from unittest.mock import patch

import pytest

from xhs.errors import RateLimitError
from xhs.login import (
    check_login_status,
    fetch_qrcode,
    get_current_user_nickname,
    make_qrcode_url,
    send_phone_code,
    submit_phone_code,
    wait_for_login,
)


class TestCheckLoginStatus:
    def test_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: sel == ".login-status"
        assert check_login_status(mock_page) is True

    def test_not_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: sel == ".login-container"
        assert check_login_status(mock_page) is False

    def test_navigates_when_not_explore(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/other"
        mock_page.has_element.side_effect = lambda sel: sel == ".login-status"
        check_login_status(mock_page)
        mock_page.navigate.assert_called()


class TestFetchQrcode:
    def test_already_logged_in(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.return_value = True
        png_bytes, b64_str, already = fetch_qrcode(mock_page)
        assert already is True
        assert png_bytes == b""

    def test_success(self, mock_page):
        fake_b64 = base64.b64encode(b"fake-png-data").decode()
        mock_page.evaluate.side_effect = [
            "https://www.xiaohongshu.com/explore",  # current_url
            False,  # has_element LOGIN_STATUS
            f"data:image/png;base64,{fake_b64}",  # qrcode src
        ]
        mock_page.has_element.return_value = False
        png_bytes, b64_str, already = fetch_qrcode(mock_page)
        assert already is False
        assert png_bytes == b"fake-png-data"

    def test_no_src_raises(self, mock_page):
        mock_page.evaluate.side_effect = [
            "https://www.xiaohongshu.com/explore",
            False,
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
        mock_page.has_element.side_effect = lambda sel: sel == ".login-status"
        result = send_phone_code(mock_page, "13800138000")
        assert result is False

    def test_success(self, mock_page):
        mock_page.evaluate.return_value = "https://www.xiaohongshu.com/explore"
        mock_page.has_element.side_effect = lambda sel: sel in (".login-container", ".agree-checked")
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
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_login.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_login.py
git commit -m "test: 添加 login 模块测试"
```

---

## Task 13: test_search.py — 搜索模块测试

**Files:**
- Create: `tests/xhs/test_search.py`
- Read: `scripts/xhs/search.py`

- [ ] **Step 1: 编写测试**

```python
"""搜索模块测试。"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from xhs.errors import NoFeedsError
from xhs.search import _convert_filters, _find_internal_option, search_feeds
from xhs.types import FilterOption


class TestFindInternalOption:
    def test_valid_option(self):
        group, tag = _find_internal_option(1, "最新")
        assert group == 1
        assert tag == 2

    def test_invalid_group(self):
        with pytest.raises(ValueError, match="筛选组 99 不存在"):
            _find_internal_option(99, "测试")

    def test_invalid_text(self):
        with pytest.raises(ValueError, match="未找到"):
            _find_internal_option(1, "不存在的选项")


class TestConvertFilters:
    def test_empty_filter(self):
        opt = FilterOption()
        assert _convert_filters(opt) == []

    def test_sort_by(self):
        opt = FilterOption(sort_by="最多点赞")
        result = _convert_filters(opt)
        assert (1, 3) in result

    def test_note_type(self):
        opt = FilterOption(note_type="图文")
        result = _convert_filters(opt)
        assert (2, 3) in result

    def test_multiple_filters(self):
        opt = FilterOption(sort_by="最新", note_type="视频")
        result = _convert_filters(opt)
        assert len(result) == 2


class TestSearchFeeds:
    def test_success(self, mock_page):
        feed_data = [{"id": "f1", "noteCard": {"displayTitle": "测试"}}]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        with patch("xhs.search._wait_for_initial_state"):
            feeds = search_feeds(mock_page, "关键词")
        assert len(feeds) == 1
        assert feeds[0].id == "f1"

    def test_no_feeds_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with patch("xhs.search._wait_for_initial_state"):
            with pytest.raises(NoFeedsError):
                search_feeds(mock_page, "关键词")

    def test_with_filter(self, mock_page):
        feed_data = [{"id": "f1", "noteCard": {"displayTitle": "测试"}}]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        filter_opt = FilterOption(sort_by="最新")
        with patch("xhs.search._wait_for_initial_state"), \
             patch("xhs.search._apply_filters"):
            feeds = search_feeds(mock_page, "关键词", filter_opt)
        assert len(feeds) == 1
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_search.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_search.py
git commit -m "test: 添加 search 模块测试"
```

---

## Task 14: test_feeds.py — Feed 列表测试

**Files:**
- Create: `tests/xhs/test_feeds.py`
- Read: `scripts/xhs/feeds.py`

- [ ] **Step 1: 编写测试**

```python
"""Feed 列表测试。"""

from __future__ import annotations

import json

import pytest

from xhs.errors import NoFeedsError
from xhs.feeds import list_feeds


class TestListFeeds:
    def test_success(self, mock_page):
        feed_data = [
            {"id": "f1", "noteCard": {"displayTitle": "标题1"}},
            {"id": "f2", "noteCard": {"displayTitle": "标题2"}},
        ]
        mock_page.evaluate.return_value = json.dumps(feed_data)
        feeds = list_feeds(mock_page)
        assert len(feeds) == 2
        assert feeds[0].id == "f1"
        assert feeds[1].id == "f2"

    def test_no_feeds_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with pytest.raises(NoFeedsError):
            list_feeds(mock_page)

    def test_empty_array(self, mock_page):
        mock_page.evaluate.return_value = json.dumps([])
        feeds = list_feeds(mock_page)
        assert len(feeds) == 0

    def test_navigates_to_home(self, mock_page):
        mock_page.evaluate.return_value = json.dumps([])
        try:
            list_feeds(mock_page)
        except NoFeedsError:
            pass
        mock_page.navigate.assert_called()
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_feeds.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_feeds.py
git commit -m "test: 添加 feeds 模块测试"
```

---

## Task 15: test_feed_detail.py — Feed 详情测试

**Files:**
- Create: `tests/xhs/test_feed_detail.py`
- Read: `scripts/xhs/feed_detail.py`

- [ ] **Step 1: 编写测试**

```python
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
    _extract_feed_detail,
    _get_comment_count,
    _is_scan_qrcode_verification,
    get_feed_detail,
)
from xhs.types import CommentLoadConfig, FeedDetailResponse


class TestCheckPageAccessible:
    def test_accessible(self, mock_page):
        mock_page.get_element_text.return_value = None
        # 不应抛出异常
        _check_page_accessible(mock_page)

    def test_inaccessible_keyword(self, mock_page):
        mock_page.get_element_text.return_value = "该笔记已被删除"
        with pytest.raises(PageNotAccessibleError, match="该笔记已被删除"):
            _check_page_accessible(mock_page)

    def test_scan_qrcode_retry(self, mock_page):
        mock_page.get_element_text.side_effect = ["扫码查看", ""]
        # 第二次返回空，验证消失，应继续
        _check_page_accessible(mock_page, url="https://example.com")


class TestIsScanQrcodeVerification:
    def test_positive(self):
        assert _is_scan_qrcode_verification("请使用小红书App扫码") is True

    def test_negative(self):
        assert _is_scan_qrcode_verification("该笔记已被删除") is False


class TestExtractFeedDetail:
    def test_success(self, mock_page):
        detail = {"note": {"title": "测试"}, "comments": []}
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
                "comments": [],
            }
        }
        mock_page.evaluate.return_value = json.dumps(detail_data)
        with patch("xhs.feed_detail._check_page_accessible"), \
             patch("xhs.feed_detail.sleep_random"):
            result = get_feed_detail(mock_page, "feed123", "token456")
        assert isinstance(result, FeedDetailResponse)
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_feed_detail.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_feed_detail.py
git commit -m "test: 添加 feed_detail 模块测试"
```

---

## Task 16: test_publish.py — 图文发布测试

**Files:**
- Create: `tests/xhs/test_publish.py`
- Read: `scripts/xhs/publish.py`

- [ ] **Step 1: 编写测试**

```python
"""图文发布测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from xhs.errors import ContentTooLongError, PublishError, TitleTooLongError
from xhs.publish import (
    _extract_hashtags_from_content,
    click_publish_button,
    fill_publish_form,
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
    @patch("xhs.publish.calc_title_length", return_value=5)
    def test_success(
        self, mock_calc, mock_fill, mock_upload, mock_tab, mock_nav, mock_page
    ):
        content = PublishImageContent(
            title="标题", content="内容", image_paths=["img.jpg"]
        )
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
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_publish.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_publish.py
git commit -m "test: 添加 publish 模块测试"
```

---

## Task 17: test_publish_video.py — 视频发布测试

**Files:**
- Create: `tests/xhs/test_publish_video.py`
- Read: `scripts/xhs/publish_video.py`

- [ ] **Step 1: 编写测试**

```python
"""视频发布测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from xhs.errors import PublishError
from xhs.publish_video import (
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
        content = PublishVideoContent(
            title="标题", content="内容", video_path="video.mp4"
        )
        fill_publish_video_form(mock_page, content)
        mock_upload.assert_called_once()


class TestClickPublishVideoButton:
    @patch("xhs.publish_video._wait_for_publish_button_clickable")
    def test_clicks_element(self, mock_wait, mock_page):
        click_publish_video_button(mock_page)
        mock_page.click_element.assert_called_once()


class TestPublishVideoContent:
    @patch("xhs.publish_video.fill_publish_video_form")
    @patch("xhs.publish_video._wait_for_publish_button_clickable")
    def test_success(self, mock_wait, mock_fill, mock_page):
        content = PublishVideoContent(
            title="标题", content="内容", video_path="video.mp4"
        )
        publish_video_content(mock_page, content)
        mock_fill.assert_called_once()
        mock_page.click_element.assert_called_once()
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_publish_video.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_publish_video.py
git commit -m "test: 添加 publish_video 模块测试"
```

---

## Task 18: test_publish_long_article.py — 长文发布测试

**Files:**
- Create: `tests/xhs/test_publish_long_article.py`
- Read: `scripts/xhs/publish_long_article.py`

- [ ] **Step 1: 编写测试**

```python
"""长文发布测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from xhs.publish_long_article import (
    click_next_and_fill_description,
    get_template_names,
    publish_long_article,
    select_template,
)


class TestSelectTemplate:
    @patch("xhs.publish_long_article._click_button_by_text")
    def test_success(self, mock_click, mock_page):
        mock_page.evaluate.return_value = True
        result = select_template(mock_page, "简约模板")
        mock_click.assert_called_once()

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


class TestGetTemplateNames:
    def test_returns_names(self, mock_page):
        mock_page.evaluate.return_value = '["模板A", "模板B"]'
        names = get_template_names(mock_page)
        assert names == ["模板A", "模板B"]

    def test_empty(self, mock_page):
        mock_page.evaluate.return_value = "[]"
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
        self, mock_nav, mock_tab, mock_new, mock_title,
        mock_content, mock_format, mock_wait, mock_names, mock_page
    ):
        mock_names.return_value = ["模板A"]
        result = publish_long_article(mock_page, "标题", "内容", ["img.jpg"])
        assert result == ["模板A"]
        mock_nav.assert_called_once()
        mock_tab.assert_called_once()
        mock_new.assert_called_once()
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_publish_long_article.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_publish_long_article.py
git commit -m "test: 添加 publish_long_article 模块测试"
```

---

## Task 19: test_comment.py — 评论模块测试

**Files:**
- Create: `tests/xhs/test_comment.py`
- Read: `scripts/xhs/comment.py`

- [ ] **Step 1: 编写测试**

```python
"""评论模块测试。"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from xhs.comment import post_comment, reply_comment


class TestPostComment:
    def test_success(self, mock_page):
        mock_page.has_element.return_value = True
        with patch("xhs.comment._check_page_accessible"), \
             patch("xhs.comment.sleep_random"):
            post_comment(mock_page, "feed123", "token456", "好文章！")
        mock_page.click_element.assert_called()
        mock_page.input_content_editable.assert_called()

    def test_no_input_trigger_raises(self, mock_page):
        mock_page.has_element.return_value = False
        with patch("xhs.comment._check_page_accessible"), \
             patch("xhs.comment.sleep_random"):
            with pytest.raises(RuntimeError, match="未找到评论输入框"):
                post_comment(mock_page, "feed123", "token456", "评论")


class TestReplyComment:
    def test_no_ids_raises(self, mock_page):
        with pytest.raises(ValueError, match="至少提供一个"):
            reply_comment(mock_page, "feed123", "token456", "回复", comment_id="", user_id="")

    @patch("xhs.comment._find_and_scroll_to_comment")
    def test_reply_by_comment_id(self, mock_find, mock_page):
        mock_find.return_value = True
        mock_page.has_element.return_value = True
        with patch("xhs.comment._check_page_accessible"), \
             patch("xhs.comment.sleep_random"):
            reply_comment(
                mock_page, "feed123", "token456", "回复",
                comment_id="c123",
            )
        mock_find.assert_called_once()

    @patch("xhs.comment._find_and_scroll_to_comment")
    def test_comment_not_found_raises(self, mock_find, mock_page):
        mock_find.return_value = False
        with patch("xhs.comment._check_page_accessible"), \
             patch("xhs.comment.sleep_random"):
            with pytest.raises(RuntimeError, match="未找到评论"):
                reply_comment(
                    mock_page, "feed123", "token456", "回复",
                    comment_id="c999",
                )
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_comment.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_comment.py
git commit -m "test: 添加 comment 模块测试"
```

---

## Task 20: test_like_favorite.py — 点赞/收藏测试

**Files:**
- Create: `tests/xhs/test_like_favorite.py`
- Read: `scripts/xhs/like_favorite.py`

- [ ] **Step 1: 编写测试**

```python
"""点赞/收藏测试。"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from xhs.errors import NoFeedDetailError
from xhs.like_favorite import (
    _get_interact_state,
    _toggle_favorite,
    _toggle_like,
    favorite_feed,
    like_feed,
    unfavorite_feed,
    unlike_feed,
)


class TestGetInteractState:
    def test_success(self, mock_page):
        data = {
            "feed123": {
                "note": {"interactInfo": {"liked": True, "collected": False}}
            }
        }
        mock_page.evaluate.return_value = json.dumps(data)
        liked, collected = _get_interact_state(mock_page, "feed123")
        assert liked is True
        assert collected is False

    def test_empty_result_raises(self, mock_page):
        mock_page.evaluate.return_value = ""
        with pytest.raises(NoFeedDetailError):
            _get_interact_state(mock_page, "feed123")

    def test_missing_feed_single_entry(self, mock_page):
        data = {"other": {"note": {"interactInfo": {"liked": True}}}}
        mock_page.evaluate.return_value = json.dumps(data)
        liked, _ = _get_interact_state(mock_page, "feed123")
        assert liked is True


class TestToggleLike:
    def test_already_liked_skip(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", return_value=(True, False)):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        assert result.success is True
        assert "已点赞" in result.message

    def test_like_success(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", side_effect=[(False, False), (True, False)]):
            result = _toggle_like(mock_page, "feed123", target_liked=True)
        assert result.success is True
        mock_page.click_element.assert_called()


class TestToggleFavorite:
    def test_already_collected_skip(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", return_value=(False, True)):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is True
        assert "已收藏" in result.message

    def test_collect_success(self, mock_page):
        with patch("xhs.like_favorite._get_interact_state", side_effect=[(False, False), (False, True)]), \
             patch("xhs.like_favorite._wait_collect_button", return_value=True):
            result = _toggle_favorite(mock_page, "feed123", target_collected=True)
        assert result.success is True


class TestLikeFeed:
    @patch("xhs.like_favorite._prepare_page")
    @patch("xhs.like_favorite._toggle_like")
    def test_delegates(self, mock_toggle, mock_prepare, mock_page):
        mock_toggle.return_value = None
        like_feed(mock_page, "feed123", "token")
        mock_prepare.assert_called_once()
        mock_toggle.assert_called_once()


class TestFavoriteFeed:
    @patch("xhs.like_favorite._prepare_page")
    @patch("xhs.like_favorite._toggle_favorite")
    def test_delegates(self, mock_toggle, mock_prepare, mock_page):
        mock_toggle.return_value = None
        favorite_feed(mock_page, "feed123", "token")
        mock_prepare.assert_called_once()
        mock_toggle.assert_called_once()
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_like_favorite.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_like_favorite.py
git commit -m "test: 添加 like_favorite 模块测试"
```

---

## Task 21: test_user_profile.py — 用户主页测试

**Files:**
- Create: `tests/xhs/test_user_profile.py`
- Read: `scripts/xhs/user_profile.py`

- [ ] **Step 1: 编写测试**

```python
"""用户主页测试。"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from xhs.user_profile import _extract_user_profile_data, get_user_profile
from xhs.types import UserProfileResponse


class TestExtractUserProfileData:
    def test_success(self, mock_page):
        user_data = {
            "basicInfo": {"nickname": "测试用户", "userId": "u123"},
            "interactions": [{"type": "follows", "count": 100}],
        }
        notes_data = [[{"id": "f1", "noteCard": {"displayTitle": "帖子1"}}]]

        mock_page.evaluate.side_effect = [
            True,  # __INITIAL_STATE__ exists
            json.dumps(user_data),
            json.dumps(notes_data),
        ]
        result = _extract_user_profile_data(mock_page)
        assert isinstance(result, UserProfileResponse)
        assert result.user_basic_info.nickname == "测试用户"
        assert len(result.feeds) == 1

    def test_no_user_data_raises(self, mock_page):
        mock_page.evaluate.side_effect = [True, ""]
        with pytest.raises(RuntimeError, match="userPageData"):
            _extract_user_profile_data(mock_page)

    def test_no_notes_raises(self, mock_page):
        mock_page.evaluate.side_effect = [True, json.dumps({"basicInfo": {}, "interactions": []}), ""]
        with pytest.raises(RuntimeError, match="notes"):
            _extract_user_profile_data(mock_page)


class TestGetUserProfile:
    @patch("xhs.user_profile._extract_user_profile_data")
    def test_success(self, mock_extract, mock_page):
        mock_extract.return_value = UserProfileResponse(
            user_basic_info=None, interactions=[], feeds=[]
        )
        result = get_user_profile(mock_page, "user123", "token456")
        mock_page.navigate.assert_called()
        mock_page.wait_for_load.assert_called()
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/xhs/test_user_profile.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/xhs/test_user_profile.py
git commit -m "test: 添加 user_profile 模块测试"
```

---

## Task 22: test_image_downloader.py — 图片下载测试

**Files:**
- Create: `tests/test_image_downloader.py`
- Read: `scripts/image_downloader.py`

- [ ] **Step 1: 编写测试**

```python
"""图片下载器测试。"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from image_downloader import ImageDownloader, is_image_url, process_images


class TestIsImageUrl:
    def test_http(self):
        assert is_image_url("http://example.com/img.jpg") is True

    def test_https(self):
        assert is_image_url("https://example.com/img.jpg") is True

    def test_local_path(self):
        assert is_image_url("/path/to/file.jpg") is False

    def test_relative_path(self):
        assert is_image_url("file.jpg") is False


class TestImageDownloader:
    def test_download_image_success(self, tmp_path):
        downloader = ImageDownloader(str(tmp_path))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b"fake-image-data"
        with patch.object(downloader._session, "get", return_value=mock_resp):
            path = downloader.download_image("https://example.com/photo.jpg")
        assert os.path.exists(path)
        assert path.endswith(".jpg")
        with open(path, "rb") as f:
            assert f.read() == b"fake-image-data"

    def test_download_image_invalid_url(self, tmp_path):
        downloader = ImageDownloader(str(tmp_path))
        with pytest.raises(ValueError, match="无效的图片 URL"):
            downloader.download_image("not-a-url")

    def test_download_image_server_error(self, tmp_path):
        downloader = ImageDownloader(str(tmp_path))
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        with patch.object(downloader._session, "get", return_value=mock_resp):
            with pytest.raises(RuntimeError, match="下载失败"):
                downloader.download_image("https://example.com/missing.jpg")

    def test_download_cached(self, tmp_path):
        downloader = ImageDownloader(str(tmp_path))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b"data"
        with patch.object(downloader._session, "get", return_value=mock_resp):
            path1 = downloader.download_image("https://example.com/cached.png")
            path2 = downloader.download_image("https://example.com/cached.png")
        assert path1 == path2

    def test_detect_extension(self, tmp_path):
        downloader = ImageDownloader(str(tmp_path))
        assert downloader._detect_extension("https://example.com/photo.webp") == ".webp"
        assert downloader._detect_extension("https://example.com/photo") == ".jpg"

    def test_download_images_partial_failure(self, tmp_path):
        downloader = ImageDownloader(str(tmp_path))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b"data"
        with patch.object(downloader._session, "get", return_value=mock_resp):
            paths = downloader.download_images([
                "https://example.com/ok.jpg",
                "not-a-url",
            ])
        assert len(paths) == 1


class TestProcessImages:
    def test_local_paths(self, tmp_path):
        local_file = tmp_path / "test.jpg"
        local_file.write_bytes(b"local")
        result = process_images([str(local_file)], save_dir=str(tmp_path / "out"))
        assert len(result) == 1
        assert os.path.exists(result[0])

    def test_url_download(self, tmp_path):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b"downloaded"
        with patch("image_downloader.requests.Session.get", return_value=mock_resp):
            result = process_images(
                ["https://example.com/img.jpg"],
                save_dir=str(tmp_path / "out"),
            )
        assert len(result) == 1

    def test_nonexistent_local_path(self, tmp_path):
        result = process_images(["/nonexistent/file.jpg"], save_dir=str(tmp_path / "out"))
        assert len(result) == 0
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/test_image_downloader.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_image_downloader.py
git commit -m "test: 添加 image_downloader 模块测试"
```

---

## Task 23: test_cli.py — CLI 参数解析测试

**Files:**
- Create: `tests/test_cli.py`
- Read: `scripts/cli.py`

- [ ] **Step 1: 编写测试**

```python
"""CLI 参数解析测试。"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from cli import build_parser


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
        args = parser.parse_args([
            "search-feeds",
            "--keyword", "测试",
            "--sort-by", "最多点赞",
            "--note-type", "图文",
        ])
        assert args.sort_by == "最多点赞"
        assert args.note_type == "图文"

    def test_publish_command(self):
        parser = build_parser()
        args = parser.parse_args([
            "publish",
            "--title-file", "title.txt",
            "--content-file", "content.txt",
            "--images", "img1.jpg", "img2.jpg",
            "--tags", "标签1", "标签2",
        ])
        assert args.command == "publish"
        assert args.images == ["img1.jpg", "img2.jpg"]

    def test_like_feed_command(self):
        parser = build_parser()
        args = parser.parse_args([
            "like-feed",
            "--feed-id", "f123",
            "--xsec-token", "token456",
        ])
        assert args.feed_id == "f123"

    def test_like_feed_unlike(self):
        parser = build_parser()
        args = parser.parse_args([
            "like-feed",
            "--feed-id", "f123",
            "--xsec-token", "token456",
            "--unlike",
        ])
        assert args.unlike is True
```

- [ ] **Step 2: 运行测试**

Run: `uv run pytest tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_cli.py
git commit -m "test: 添加 CLI 参数解析测试"
```

---

## Task 24: 最终验证

- [ ] **Step 1: 运行全部测试**

Run: `uv run pytest -v`
Expected: 所有测试 PASS

- [ ] **Step 2: 检查覆盖率**

Run: `uv run pytest --cov=scripts --cov-report=term-missing`
Expected: 行覆盖率 ≥90%

- [ ] **Step 3: 生成 HTML 覆盖率报告**

Run: `uv run pytest --cov=scripts --cov-report=html`
Expected: 在 `htmlcov/` 目录生成报告

- [ ] **Step 4: 最终 Commit**

```bash
git add -A
git commit -m "test: 完成测试覆盖，行覆盖率 ≥90%"
```

---

## Validation

```bash
# 运行全部测试
uv run pytest -v

# 检查覆盖率
uv run pytest --cov=scripts --cov-fail-under=90

# Lint 检查
uv run ruff check tests/
```
