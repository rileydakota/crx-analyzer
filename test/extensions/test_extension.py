import os
import pytest

from src.extensions.extension import Extension, Browser


@pytest.mark.integtest
def test_edge_extension_download():
    extension_id = "nnkgneoiohoecpdiaponcejilbhhikei"

    with Extension(extension_id, Browser.EDGE) as extension:
        # Verify files were downloaded and extracted
        assert os.path.exists(extension.extension_zip_path)
        assert os.path.exists(extension.extension_dir_path)

        # Verify manifest was parsed correctly
    assert extension.manifest is not None
    assert extension.manifest.name == "Redux DevTools"

    # Verify cleanup occurred
    assert not os.path.exists(extension.extension_zip_path)
    assert not os.path.exists(extension.extension_dir_path)
