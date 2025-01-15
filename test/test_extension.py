import os
import shutil
from crx_analyzer.extension import Extension, Browser


def mock_download_extension(url: str, output_path: str) -> None:
    test_crx_path = os.path.join(
        "test",
        "test_extension_zip",
        "test_nnkgneoiohoecpdiaponcejilbhhikei.crx",
    )
    shutil.copyfile(test_crx_path, output_path)


def test_edge_extension_download(monkeypatch):
    monkeypatch.setattr(
        "crx_analyzer.download.download_extension", mock_download_extension
    )

    extension_id = "fake"

    with Extension(extension_id, Browser.EDGE) as extension:
        # Verify files were downloaded and extracted
        assert os.path.exists(extension.extension_zip_path)
        assert os.path.exists(extension.extension_dir_path)
        assert (
            extension.sha256
            == "f4396645d06777cb879406c3226cb69b60fc923baff1868fb5db4588ef0e07e6"
        )
        assert sorted(extension.javascript_files) == sorted(
            [
                "tmp/fake/background.bundle.js",
                "tmp/fake/page.bundle.js",
                "tmp/fake/window.bundle.js",
                "tmp/fake/devtools.bundle.js",
                "tmp/fake/pagewrap.bundle.js",
                "tmp/fake/options.bundle.js",
                "tmp/fake/content.bundle.js",
                "tmp/fake/remote.bundle.js",
                "tmp/fake/devpanel.bundle.js",
            ]
        )
        # Verify manifest was parsed correctly
        assert extension.manifest is not None
        assert extension.manifest.name == "Redux DevTools"
        assert extension.manifest.manifest_version == 2
        assert sorted(extension.permissions) == sorted(
            [
                "notifications",
                "contextMenus",
                "storage",
                "file:///*",
                "http://*/*",
                "https://*/*",
            ]
        )

    # Verify cleanup occurred
    assert not os.path.exists(extension.extension_zip_path)
    assert not os.path.exists(extension.extension_dir_path)
