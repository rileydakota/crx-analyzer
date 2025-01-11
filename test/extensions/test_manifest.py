import pytest, json
from src.extensions.models import ChromeManifest, BackgroundConfig, OptionsUI, IncognitoMode

def test_minimal_valid_manifest():
    """Test manifest with only required fields"""
    manifest_data = {
        "manifest_version": 3,
        "name": "Test Extension",
        "version": "1.0.0"
    }
    manifest = ChromeManifest(**manifest_data)
    assert manifest.name == "Test Extension"
    assert manifest.version == "1.0.0"
    assert manifest.manifest_version == 3

def test_full_manifest():
    """Test manifest with optional fields"""
    manifest_data = {
        "manifest_version": 3,
        "name": "Full Test Extension",
        "version": "1.0.0",
        "description": "A test extension",
        "background": {
            "service_worker": "background.js"
        },
        "options_ui": {
            "page": "options.html",
            "chrome_style": True
        },
        "permissions": ["storage", "tabs"],
        "incognito": "split",
        "icons": {
            "16": "icon16.png",
            "48": "icon48.png",
            "128": "icon128.png"
        }
    }
    manifest = ChromeManifest(**manifest_data)
    assert manifest.description == "A test extension"
    assert isinstance(manifest.background, BackgroundConfig)
    assert manifest.background.service_worker == "background.js"
    assert isinstance(manifest.options_ui, OptionsUI)
    assert manifest.options_ui.page == "options.html"
    assert manifest.permissions == ["storage", "tabs"]
    assert manifest.incognito == IncognitoMode.SPLIT
    assert manifest.icons == {
        "16": "icon16.png",
        "48": "icon48.png",
        "128": "icon128.png"
    }

def test_invalid_manifest_version():
    """Test that invalid manifest version raises error"""
    manifest_data = {
        "manifest_version": "", 
        "name": "Test Extension",
        "version": "1.0.0"
    }
    with pytest.raises(ValueError):
        ChromeManifest(**manifest_data)

def test_invalid_incognito_mode():
    """Test that invalid incognito mode raises error"""
    manifest_data = {
        "manifest_version": 3,
        "name": "Test Extension",
        "version": "1.0.0",
        "incognito": "invalid_mode"
    }
    with pytest.raises(ValueError):
        ChromeManifest(**manifest_data)

def test_missing_required_fields():
    """Test that missing required fields raise error"""
    manifest_data = {
        "manifest_version": 3,
        "name": "Test Extension"
        # Missing version field
    }
    with pytest.raises(ValueError):
        ChromeManifest(**manifest_data)

def test_manifest_from_file():
    manifest_data = json.load(open("test/extensions/test_manifests/manifest1.json"))
    manifest = ChromeManifest(**manifest_data)
    assert manifest.name == "Hello Extensions"
    assert manifest.version == "1.0"
    assert manifest.manifest_version == 3
    assert manifest.action['default_popup'] == "hello.html"
    assert manifest.action['default_icon'] == "hello_extensions.png"
    assert manifest.permissions == ["webRequest", "cookies"]
    assert manifest.host_permissions == ["<all_urls>"]
    assert manifest.background.service_worker == "background.js"
