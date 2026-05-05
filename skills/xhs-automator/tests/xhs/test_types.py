"""数据类型测试。"""

from __future__ import annotations

import pytest
from xhs.types import (
    ActionResult,
    CommentLoadConfig,
    Cover,
    Feed,
    FilterOption,
    ImageInfo,
    InteractInfo,
    PublishImageContent,
    User,
    Video,
    VideoCapability,
)


@pytest.fixture
def sample_feed_data():
    """构造一个完整的 Feed 字典样本。"""
    return {
        "id": "test_feed_id",
        "xsecToken": "token123",
        "modelType": "note",
        "index": 5,
        "noteCard": {
            "type": "normal",
            "displayTitle": "测试标题",
            "user": {
                "userId": "u001",
                "nickname": "作者昵称",
                "nickName": "备用昵称",
                "avatar": "avatar.jpg",
            },
            "interactInfo": {
                "liked": False,
                "likedCount": "50",
                "collected": False,
            },
            "cover": {
                "width": 1080,
                "height": 720,
                "url": "https://example.com/cover.jpg",
                "fileId": "fid1",
                "urlPre": "https://example.com/pre.jpg",
                "urlDefault": "https://example.com/default.jpg",
                "infoList": [{"imageScene": "s1", "url": "u1"}],
            },
        },
    }


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

    def test_from_dict_empty(self):
        v = Video.from_dict({})
        assert v.capa.duration == 0


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
        assert cover.url_pre == "https://example.com/pre.jpg"
        assert cover.url_default == "https://example.com/default.jpg"
        assert len(cover.info_list) == 1
        assert cover.info_list[0].image_scene == "scene1"

    def test_from_dict_empty(self):
        cover = Cover.from_dict({})
        assert cover.width == 0
        assert cover.info_list == []


class TestUser:
    def test_from_dict(self):
        d = {
            "userId": "u123",
            "nickname": "测试用户",
            "nickName": "昵称",
            "avatar": "av.jpg",
        }
        user = User.from_dict(d)
        assert user.user_id == "u123"
        assert user.nickname == "测试用户"
        assert user.nick_name == "昵称"
        assert user.avatar == "av.jpg"

    def test_from_dict_empty(self):
        user = User.from_dict({})
        assert user.user_id == ""
        assert user.nickname == ""


class TestInteractInfo:
    def test_from_dict(self):
        d = {
            "liked": True,
            "likedCount": "100",
            "collected": False,
        }
        info = InteractInfo.from_dict(d)
        assert info.liked is True
        assert info.liked_count == "100"
        assert info.collected is False

    def test_from_dict_defaults(self):
        info = InteractInfo.from_dict({})
        assert info.liked is False
        assert info.liked_count == ""
        assert info.collected is False


class TestFeed:
    def test_from_dict(self, sample_feed_data):
        feed = Feed.from_dict(sample_feed_data)
        assert feed.id == "test_feed_id"
        assert feed.xsec_token == "token123"
        assert feed.model_type == "note"
        assert feed.index == 5
        assert feed.note_card.display_title == "测试标题"
        assert feed.note_card.user.user_id == "u001"

    def test_to_dict(self, sample_feed_data):
        feed = Feed.from_dict(sample_feed_data)
        d = feed.to_dict()
        assert d["id"] == "test_feed_id"
        assert d["xsecToken"] == "token123"
        assert d["displayTitle"] == "测试标题"
        assert d["user"]["userId"] == "u001"
        assert d["cover"] == "https://example.com/cover.jpg"


class TestFilterOption:
    def test_default(self):
        opt = FilterOption()
        assert opt.sort_by == ""
        assert opt.note_type == ""

    def test_fields(self):
        opt = FilterOption(sort_by="最新", note_type="视频")
        assert opt.sort_by == "最新"
        assert opt.note_type == "视频"


class TestPublishImageContent:
    def test_default(self):
        content = PublishImageContent(title="标题", content="内容", image_paths=["a.jpg"])
        assert content.title == "标题"
        assert content.tags == []
        assert content.schedule_time is None
        assert content.is_original is False


class TestActionResult:
    def test_creation(self):
        result = ActionResult(feed_id="f1", success=True, message="ok")
        assert result.success is True
        assert result.feed_id == "f1"
        assert result.to_dict()["feed_id"] == "f1"

    def test_default(self):
        result = ActionResult()
        assert result.success is False
        assert result.to_dict()["success"] is False


class TestCommentLoadConfig:
    def test_default(self):
        config = CommentLoadConfig()
        assert config.click_more_replies is False
        assert config.max_replies_threshold == 10
        assert config.max_comment_items == 0
        assert config.scroll_speed == "normal"
