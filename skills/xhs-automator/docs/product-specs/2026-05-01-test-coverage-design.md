# 测试覆盖设计方案

## 背景

xhs-automator 项目目前没有任何测试用例（`tests/` 目录只有空的 `__init__.py`）。随着功能增加，缺乏测试导致：
- 重构时无法确认功能完整性
- 新贡献者难以验证改动是否破坏现有功能
- CI/CD 无法提供质量保障

## 目标

为项目建立全面的测试覆盖，确保：
1. 所有核心模块都有对应的测试文件
2. 使用纯 mock 策略，不依赖真实浏览器
3. 行覆盖率 ≥90%，分支覆盖率 ≥80%，函数覆盖率 100%

## 非目标

- 不搭建真实的浏览器测试环境
- 不测试小红书网站本身的行为
- 不测试网络连接或外部服务
- 不测试 `bridge_server.py`（独立服务，需集成测试环境）
- 不测试 `validate_agents_docs.py`（文档验证工具，独立于核心功能）

## 测试结构

采用模块镜像结构，与源码保持一致。所有 `scripts/xhs/` 模块的测试放在 `tests/xhs/` 下：

```
tests/
├── __init__.py                # 包标识（空文件）
├── conftest.py                # 共享 fixtures
├── test_cli.py                # tests/scripts/cli.py
├── test_image_downloader.py   # tests/scripts/image_downloader.py
├── test_title_utils.py        # tests/scripts/title_utils.py
├── test_run_lock.py           # tests/scripts/run_lock.py
└── xhs/
    ├── __init__.py            # 包标识（空文件）
    ├── conftest.py            # xhs 模块专用 fixtures
    ├── test_selectors.py      # tests/scripts/xhs/selectors.py
    ├── test_types.py          # tests/scripts/xhs/types.py
    ├── test_errors.py         # tests/scripts/xhs/errors.py
    ├── test_urls.py           # tests/scripts/xhs/urls.py
    ├── test_human.py          # tests/scripts/xhs/human.py
    ├── test_cookies.py        # tests/scripts/xhs/cookies.py
    ├── test_bridge.py         # tests/scripts/xhs/bridge.py
    ├── test_cdp.py            # tests/scripts/xhs/cdp.py
    ├── test_login.py          # tests/scripts/xhs/login.py
    ├── test_search.py         # tests/scripts/xhs/search.py
    ├── test_feed_detail.py    # tests/scripts/xhs/feed_detail.py
    ├── test_feeds.py          # tests/scripts/xhs/feeds.py
    ├── test_publish.py        # tests/scripts/xhs/publish.py
    ├── test_publish_video.py  # tests/scripts/xhs/publish_video.py
    ├── test_publish_long_article.py  # tests/scripts/xhs/publish_long_article.py
    ├── test_comment.py        # tests/scripts/xhs/comment.py
    ├── test_like_favorite.py  # tests/scripts/xhs/like_favorite.py
    └── test_user_profile.py   # tests/scripts/xhs/user_profile.py
```

## Page 类型说明

项目有两种 Page 抽象，mock 策略不同：

| 类型 | 位置 | 用途 | Mock 方式 |
|------|------|------|-----------|
| `cdp.Page` | `scripts/xhs/cdp.py` | 功能模块直接使用 | `create_autospec(Page)` |
| `cdp.Browser` | `scripts/xhs/cdp.py` | 浏览器连接管理 | Mock `requests.get` + `CDPClient` |
| `bridge.BridgePage` | `scripts/xhs/bridge.py` | CLI 通过 bridge 调用 | Mock WebSocket 连接 |

**各模块使用的 Page 类型：**

| 模块 | Page 类型 | 说明 |
|------|-----------|------|
| `login.py` | `cdp.Page` | `from .cdp import Page` |
| `search.py` | `cdp.Page` | `from .cdp import Page` |
| `feed_detail.py` | `cdp.Page` | `from .cdp import Page` |
| `feeds.py` | `cdp.Page` | `from .cdp import Page` |
| `publish.py` | `cdp.Page` | `from .cdp import Page` |
| `publish_video.py` | `cdp.Page` | `from .cdp import Page` |
| `publish_long_article.py` | `cdp.Page` | `from .cdp import Page` |
| `comment.py` | `cdp.Page` | `from .cdp import Page` |
| `like_favorite.py` | `cdp.Page` | `from .cdp import Page` |
| `user_profile.py` | `cdp.Page` | `from .cdp import Page` |

## 测试策略

### 核心工具模块（无 mock）

这些模块不依赖浏览器，可以直接测试：

| 模块 | 测试重点 |
|------|----------|
| `selectors.py` | CSS 选择器格式正确性、常量值 |
| `types.py` | 数据类构造、`from_dict` 方法、`to_dict` 序列化、默认值 |
| `errors.py` | 异常继承链（XHSError 子类）、错误消息格式 |
| `urls.py` | URL 构建函数、参数编码、特殊字符处理 |
| `human.py` | 延迟函数范围、滚动计算、随机性验证 |
| `cookies.py` | 文件读写、路径解析、环境变量处理 |
| `title_utils.py` | 标题长度计算（UTF-16）、截断逻辑 |
| `run_lock.py` | 锁文件创建、过期锁检测、清理 |
| `image_downloader.py` | Mock HTTP 请求下载图片、文件 I/O、SHA256 缓存、URL/路径处理 |

### CLI 模块

| 测试类型 | 测试内容 |
|----------|----------|
| 参数解析 | `build_parser()` 各子命令参数验证 |
| 输出格式 | JSON 输出结构、`ensure_ascii=False` |
| 退出码 | 0/1/2 对应场景 |
| 错误处理 | 异常捕获和错误消息 |

### XHS 功能模块（mock cdp.Page）

使用 `unittest.mock.create_autospec(Page)` 自动模拟所有 Page 方法：

| 模块 | Mock 策略 | 测试重点 |
|------|-----------|----------|
| `bridge.py` | Mock `websockets.sync.client.connect` | 消息发送/接收、错误处理、超时、上下文管理器协议 |
| `cdp.py` (CDPClient) | Mock WebSocket | CDP 命令、超时处理、会话管理 |
| `cdp.py` (Browser) | Mock `requests.get` + `CDPClient` | 浏览器连接、页面创建/获取、Target 管理 |
| `login.py` | Mock `cdp.Page` | 登录状态检查、二维码获取、手机号登录 |
| `search.py` | Mock `cdp.Page` | 搜索流程、筛选应用、结果解析 |
| `feed_detail.py` | Mock `cdp.Page` | 详情获取、评论加载、分页 |
| `feeds.py` | Mock `cdp.Page` | Feed 列表获取 |
| `publish.py` | Mock `cdp.Page` | 表单填写、图片上传、发布流程 |
| `publish_video.py` | Mock `cdp.Page` | 视频上传、表单填写、发布流程 |
| `publish_long_article.py` | Mock `cdp.Page` | 长文填写、模板选择、排版 |
| `comment.py` | Mock `cdp.Page` | 评论发表、回复、评论查找 |
| `like_favorite.py` | Mock `cdp.Page` | 点赞/收藏状态切换、幂等性 |
| `user_profile.py` | Mock `cdp.Page` | 用户信息提取、帖子列表 |

### bridge.py Mock 模式

`BridgePage._call()` 使用 `websockets.sync.client.connect` 作为上下文管理器：

```python
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_ws():
    """模拟 WebSocket 连接"""
    ws = MagicMock()
    ws.recv.return_value = json.dumps({"result": "ok"})
    return ws

@pytest.fixture
def bridge_page(mock_ws):
    """模拟 BridgePage"""
    with patch("xhs.bridge.ws_client.connect") as mock_connect:
        mock_connect.return_value.__enter__ = MagicMock(return_value=mock_ws)
        mock_connect.return_value.__exit__ = MagicMock(return_value=False)
        from xhs.bridge import BridgePage
        return BridgePage("ws://localhost:9333")
```

### time.sleep Mock 策略

为避免测试变慢，所有 `time.sleep` 调用都需要 mock：

```python
# 在 conftest.py 中添加
@pytest.fixture(autouse=True)
def mock_sleep():
    """自动 mock time.sleep，加速测试"""
    with patch("time.sleep"):
        yield
```

对于 `human.sleep_random()`，需要单独 mock：

```python
@patch("xhs.human.time.sleep")
def test_sleep_random(mock_sleep):
    sleep_random(100, 200)
    mock_sleep.assert_called_once()
    delay = mock_sleep.call_args[0][0]
    assert 0.1 <= delay <= 0.2
```

## 共享 Fixtures

### tests/conftest.py

```python
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_sleep():
    """自动 mock time.sleep，加速测试"""
    with patch("time.sleep"):
        yield

@pytest.fixture
def sample_feed_data():
    """示例 Feed 数据"""
    return {
        "id": "test_feed_id",
        "noteCard": {
            "displayTitle": "测试标题",
            "user": {"userId": "user123", "nickname": "测试用户"},
            "interactInfo": {"likedCount": "100", "commentCount": "50"}
        }
    }

@pytest.fixture
def tmp_cookies(tmp_path):
    """临时 Cookie 文件"""
    cookie_file = tmp_path / "cookies.json"
    cookie_file.write_bytes(b'{"cookies": []}')
    return str(cookie_file)
```

### tests/xhs/conftest.py

```python
import pytest
from unittest.mock import create_autospec, MagicMock
from xhs.cdp import Page

@pytest.fixture
def mock_page():
    """模拟 cdp.Page 对象，自动生成所有方法存根"""
    page = create_autospec(Page, instance=True)
    page.target_id = "test-target-id"
    page.session_id = "test-session-id"
    return page

@pytest.fixture
def mock_bridge_page():
    """模拟 bridge.BridgePage 对象"""
    from xhs.bridge import BridgePage
    page = MagicMock(spec=BridgePage)
    page.evaluate.return_value = ""
    page.has_element.return_value = False
    page.is_server_running.return_value = True
    page.is_extension_connected.return_value = True
    return page
```

## 覆盖配置

### pyproject.toml 变更

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

### 覆盖目标

| 指标 | 目标 |
|------|------|
| 行覆盖率 | ≥90% |
| 分支覆盖率 | ≥80% |
| 函数覆盖率 | 100% |

### 覆盖排除

以下情况使用 `# pragma: no cover` 标记：
- 平台特定代码（Windows/macOS/Linux 分支）
- `if __name__ == "__main__"` 入口
- 需要真实网络的错误路径

## 实施顺序

1. **Phase 1: 基础设施**
   - 更新 `pyproject.toml` 添加 `pytest-cov` 依赖和 `pythonpath` 配置
   - 创建 `tests/__init__.py` 和 `tests/xhs/__init__.py`（空包标识文件）
   - 创建 `tests/conftest.py` 和共享 fixtures
   - 创建 `tests/xhs/conftest.py` 和 xhs 专用 fixtures

2. **Phase 2: 核心工具模块**
   - `tests/xhs/test_selectors.py`
   - `tests/xhs/test_types.py`
   - `tests/xhs/test_errors.py`
   - `tests/xhs/test_urls.py`
   - `tests/xhs/test_human.py`
   - `tests/xhs/test_cookies.py`

3. **Phase 3: CLI 模块**
   - `tests/test_cli.py`

4. **Phase 4: XHS 功能模块**
   - 按依赖顺序：bridge → cdp → login → search → feeds → feed_detail → publish → publish_video → publish_long_article → comment → like_favorite → user_profile

5. **Phase 5: 辅助模块**
   - `tests/test_image_downloader.py`
   - `tests/test_title_utils.py`
   - `tests/test_run_lock.py`

## 验证方式

```bash
# 运行全部测试
uv run pytest

# 运行并生成覆盖率报告
uv run pytest --cov=scripts --cov-report=html

# 只运行特定模块测试
uv run pytest tests/xhs/test_types.py

# 检查覆盖率是否达标
uv run pytest --cov=scripts --cov-fail-under=90
```

## 约束

- 所有测试必须是纯 mock，不依赖真实浏览器或网络
- 测试文件名必须以 `test_` 开头
- 测试函数名必须以 `test_` 开头
- 使用中文注释描述测试场景
- 每个测试函数只测试一个行为
- 使用 `create_autospec(Page)` 确保 mock 与真实接口一致
- 测试不应验证 mock 行为本身，而应验证被测逻辑

## 测试反模式（应避免）

- 不要 mock 过于底层（如单个 CDP 消息），应 mock Page 级接口
- 不要写只验证 mock 被调用的测试，应验证逻辑正确性
- 不要在测试中使用真实 `time.sleep`，会拖慢测试速度
- 不要忽略边界条件和异常路径
