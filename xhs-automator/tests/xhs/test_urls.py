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
