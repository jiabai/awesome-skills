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
