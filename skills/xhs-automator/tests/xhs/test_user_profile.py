"""用户主页测试。"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from xhs.types import UserProfileResponse
from xhs.user_profile import _extract_user_profile_data, get_user_profile


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
        mock_page.evaluate.side_effect = [
            True,
            json.dumps({"basicInfo": {}, "interactions": []}),
            "",
        ]
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
        mock_page.wait_dom_stable.assert_called()
        assert isinstance(result, UserProfileResponse)
