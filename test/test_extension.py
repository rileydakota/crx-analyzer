import os
import pytest
import shutil
from unittest.mock import patch
from crx_analyzer.extension import Extension, Browser, InvalidExtensionIDError


def mock_edge_extension(url: str, output_path: str) -> None:
    test_crx_path = os.path.join(
        "test",
        "test_extension_zip",
        "test_edge_nnkgneoiohoecpdiaponcejilbhhikei.crx",
    )
    shutil.copyfile(test_crx_path, output_path)


def mock_chrome_extension(url: str, output_path: str) -> None:
    test_crx_path = os.path.join(
        "test",
        "test_extension_zip",
        "test_chrome_extension.crx",
    )
    shutil.copyfile(test_crx_path, output_path)


def test_edge_extension_download(monkeypatch):
    monkeypatch.setattr(
        "crx_analyzer.download.download_extension", mock_edge_extension
    )

    extension_id = "fake"

    with Extension(extension_id, Browser.EDGE) as extension:
        assert os.path.exists(extension.extension_zip_path)
        assert os.path.exists(extension.extension_dir_path)
        assert extension.browser == Browser.EDGE
        assert extension.manifest.name == "Redux DevTools"
        assert extension.manifest.manifest_version == 2


def test_chrome_extension_download(monkeypatch):
    monkeypatch.setattr(
        "crx_analyzer.download.download_extension", mock_chrome_extension
    )

    extension_id = "fake"

    with Extension(extension_id, Browser.CHROME) as extension:
        assert os.path.exists(extension.extension_zip_path)
        assert os.path.exists(extension.extension_dir_path)
        assert extension.browser == Browser.CHROME
        assert extension.manifest.name == "Test Chrome Extension"
        assert extension.manifest.manifest_version == 3


def test_invalid_extension_id():
    with patch("crx_analyzer.download.download_extension") as mock_download:
        mock_download.side_effect = HTTPError(response=Mock(status_code=404), request=Mock(url="test"))
        with pytest.raises(InvalidExtensionIDError):
            Extension("invalid_id", Browser.CHROME)


def test_invalid_browser():
    with pytest.raises(ValueError, match="Invalid browser"):
        Extension("test_id", "invalid_browser")


def test_extension_properties(monkeypatch):
    monkeypatch.setattr(
        "crx_analyzer.download.download_extension", mock_edge_extension
    )
    
    with Extension("fake", Browser.EDGE) as extension:
        assert extension.name == "Redux DevTools"
        assert extension.version == "3.1.6"
        assert extension.manifest_version == 2
        assert sorted(extension.permissions) == sorted([
            "notifications",
            "contextMenus",
            "storage",
            "file:///*",
            "http://*/*",
            "https://*/*",
        ])


def test_url_extraction(monkeypatch):
    monkeypatch.setattr(
        "crx_analyzer.download.download_extension", mock_edge_extension
    )
    
    with Extension("fake", Browser.EDGE) as extension:
        urls = extension.urls
        assert any(url.startswith("http://") for url in urls)
        assert any(url.startswith("https://") for url in urls)
        assert any(url.startswith("file://") for url in urls)

    # Verify cleanup occurred
    assert not os.path.exists(extension.extension_zip_path)
    assert not os.path.exists(extension.extension_dir_path)
