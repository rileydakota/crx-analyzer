import os
import pytest
import shutil
from unittest.mock import patch

from src.extensions.extension import Extension, Browser


def mock_download_extension(url: str, output_path: str) -> None:
    test_crx_path = os.path.join(
        "test",
        "extensions",
        "test_extension_zip",
        "nnkgneoiohoecpdiaponcejilbhhikei.crx",
    )
    shutil.copyfile(test_crx_path, output_path)


@pytest.mark.integtest
@patch(
    "src.extensions.download.download_extension", side_effect=mock_download_extension
)
def test_edge_extension_download(mock_download):
    extension_id = "nnkgneoiohoecpdiaponcejilbhhikei"

    with Extension(extension_id, Browser.EDGE) as extension:
        # Verify files were downloaded and extracted
        assert os.path.exists(extension.extension_zip_path)
        assert os.path.exists(extension.extension_dir_path)
        assert (
            extension.sha256
            == "f4396645d06777cb879406c3226cb69b60fc923baff1868fb5db4588ef0e07e6"
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
