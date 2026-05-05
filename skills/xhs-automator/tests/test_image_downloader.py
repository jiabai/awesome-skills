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
        with (
            patch.object(downloader._session, "get", return_value=mock_resp),
            pytest.raises(RuntimeError, match="下载失败"),
        ):
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
            paths = downloader.download_images(
                [
                    "https://example.com/ok.jpg",
                    "not-a-url",
                ]
            )
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
