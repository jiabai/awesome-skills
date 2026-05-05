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
        # viewport=100, ratio=0.1 -> clamped to 400, then +-50 jitter
        delta = calculate_scroll_delta(100, 0.1)
        assert delta >= 350  # 400 - 50 jitter

    def test_normal_delta(self):
        # viewport=1000, ratio=0.7 -> 700-900, then +-50 jitter
        delta = calculate_scroll_delta(1000, 0.7)
        assert 650 <= delta <= 950


class TestInaccessibleKeywords:
    def test_not_empty(self):
        assert len(INACCESSIBLE_KEYWORDS) > 0

    def test_contains_expected(self):
        assert "私密笔记" in INACCESSIBLE_KEYWORDS
        assert "已失效" in INACCESSIBLE_KEYWORDS
