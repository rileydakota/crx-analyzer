import os
import pytest
import shutil
from unittest.mock import patch, Mock
from requests import HTTPError
from crx_analyzer.extension import Extension, Browser, InvalidExtensionIDError


def mock_edge_extension(url: str, output_path: str) -> None:
    test_crx_path = os.path.join(
        "test",
        "test_extension_zip",
        "test_edge_nnkgneoiohoecpdiaponcejilbhhikei.crx",
    )
    shutil.copyfile(test_crx_path, output_path)


def test_edge_extension_download(monkeypatch):
    monkeypatch.setattr("crx_analyzer.download.download_extension", mock_edge_extension)

    extension_id = "fake"

    with Extension(extension_id, Browser.EDGE) as extension:
        assert os.path.exists(extension.extension_zip_path)
        assert os.path.exists(extension.extension_dir_path)
        assert extension.browser == Browser.EDGE
        assert extension.manifest.name == "Redux DevTools"
        assert extension.manifest.manifest_version == 2


def test_invalid_extension_id():
    with patch("crx_analyzer.download.download_extension") as mock_download:
        mock_download.side_effect = HTTPError(
            response=Mock(status_code=404), request=Mock(url="test")
        )
        with pytest.raises(InvalidExtensionIDError):
            Extension("invalid_id", Browser.CHROME)


def test_invalid_browser():
    with pytest.raises(ValueError, match="Invalid browser"):
        Extension("test_id", "invalid_browser")


def test_edge_extension_manifest_fields(monkeypatch):
    """Test detailed manifest field extraction"""
    monkeypatch.setattr("crx_analyzer.download.download_extension", mock_edge_extension)

    with Extension("fake", Browser.EDGE) as extension:
        # Test basic fields
        assert extension.name == "Redux DevTools"
        assert extension.version == "3.1.6"
        assert extension.manifest_version == 2

        # Test optional fields
        assert extension.manifest.options_ui.page == "options.html"
        assert extension.manifest.options_ui.chrome_style
        assert not extension.manifest.background.persistent
        assert extension.manifest.background.scripts == ["background.bundle.js"]


def test_edge_extension_permissions(monkeypatch):
    """Test permission parsing"""
    monkeypatch.setattr("crx_analyzer.download.download_extension", mock_edge_extension)

    with Extension("fake", Browser.EDGE) as extension:
        expected_permissions = [
            "notifications",
            "contextMenus",
            "storage",
            "file:///*",
            "http://*/*",
            "https://*/*",
        ]
        assert sorted(extension.permissions) == sorted(expected_permissions)


def test_edge_extension_cleanup(monkeypatch):
    """Test proper cleanup of temporary files"""
    monkeypatch.setattr("crx_analyzer.download.download_extension", mock_edge_extension)

    extension_path = None
    extension_dir = None

    with Extension("fake", Browser.EDGE) as extension:
        extension_path = extension.extension_zip_path
        extension_dir = extension.extension_dir_path
        assert os.path.exists(extension_path)
        assert os.path.exists(extension_dir)

    assert not os.path.exists(extension_path)
    assert not os.path.exists(extension_dir)


def test_edge_extension_javascript_files(monkeypatch):
    """Test JavaScript file detection"""
    monkeypatch.setattr("crx_analyzer.download.download_extension", mock_edge_extension)

    with Extension("fake", Browser.EDGE) as extension:
        js_files = extension.javascript_files
        assert any("background.bundle.js" in f for f in js_files)


def test_url_extraction(monkeypatch):
    monkeypatch.setattr("crx_analyzer.download.download_extension", mock_edge_extension)

    with Extension("fake", Browser.EDGE) as extension:
        urls = extension.urls
        assert any(url.startswith("http://") for url in urls)
        assert any(url.startswith("https://") for url in urls)
        assert any(url.startswith("file://") for url in urls)

    # Verify cleanup occurred
    assert not os.path.exists(extension.extension_zip_path)
    assert not os.path.exists(extension.extension_dir_path)
