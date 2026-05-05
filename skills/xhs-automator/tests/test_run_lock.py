"""单实例锁测试。"""

from __future__ import annotations

import os

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
        assert lock2.acquire(timeout=0.1) is False
        lock.release()

    def test_context_manager(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        with RunLock(lock_file):
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
