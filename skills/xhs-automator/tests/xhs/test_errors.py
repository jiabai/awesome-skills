"""异常体系测试。"""

from __future__ import annotations

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
            NoFeedsError(),
            NoFeedDetailError(),
            NotLoggedInError(),
            PageNotAccessibleError("reason"),
            UploadTimeoutError(),
            PublishError(),
            TitleTooLongError("10", "20"),
            ContentTooLongError("10", "20"),
            RateLimitError(),
            CDPError(),
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
