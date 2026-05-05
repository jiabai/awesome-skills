"""标题工具测试。"""

from __future__ import annotations

from title_utils import calc_title_length, truncate_title


class TestCalcTitleLength:
    def test_ascii(self):
        # "hello" = 5 ASCII code units, byte_len=5, (5+1)//2 = 3
        assert calc_title_length("hello") == 3

    def test_chinese(self):
        # 每个中文字符 = 非 ASCII, 权重 2
        # "你好" = byte_len 4, (4+1)//2 = 2
        assert calc_title_length("你好") == 2

    def test_empty(self):
        assert calc_title_length("") == 0

    def test_mixed(self):
        # "hello你好" = 5*1 + 2*2 = 9, (9+1)//2 = 5
        assert calc_title_length("hello你好") == 5

    def test_chinese_four(self):
        # "你好世界" = 4*2 = 8, (8+1)//2 = 4
        assert calc_title_length("你好世界") == 4

    def test_single_ascii(self):
        assert calc_title_length("a") == 1

    def test_single_chinese(self):
        # "好" = byte_len 2, (2+1)//2 = 1
        assert calc_title_length("好") == 1

    def test_max_boundary(self):
        # 20 个中文字符 = byte_len 40, (40+1)//2 = 20
        assert calc_title_length("你" * 20) == 20

    def test_ootd(self):
        # "OOTD穿搭分享" = 4*1 + 4*2 = 12, (12+1)//2 = 6
        assert calc_title_length("OOTD穿搭分享") == 6


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

    def test_exact_boundary(self):
        # 恰好等于 max_length 的标题不被截断
        title = "你" * 20  # length = 20
        result = truncate_title(title, 20)
        assert result == title

    def test_one_over_boundary(self):
        title = "你" * 21  # length = 21
        result = truncate_title(title, 20)
        assert calc_title_length(result) <= 20

    def test_default_max_length(self):
        # 默认 MAX_TITLE_LENGTH = 20
        title = "你" * 25
        result = truncate_title(title)
        assert calc_title_length(result) <= 20
