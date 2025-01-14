import json

import pytest

from ext_analyzer.models import (
    BackgroundConfig,
    ChromeManifest,
    IncognitoMode,
    OptionsUI,
)


def test_minimal_valid_manifest():
    """Test manifest with only required fields"""
    manifest_data = {
        "manifest_version": 3,
        "name": "Test Extension",
        "version": "1.0.0",
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
        "background": {"service_worker": "background.js"},
        "options_ui": {"page": "options.html", "chrome_style": True},
        "permissions": ["storage", "tabs"],
        "incognito": "split",
        "icons": {"16": "icon16.png", "48": "icon48.png", "128": "icon128.png"},
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
        "128": "icon128.png",
    }


def test_invalid_incognito_mode():
    """Test that invalid incognito mode raises error"""
    manifest_data = {
        "manifest_version": 3,
        "name": "Test Extension",
        "version": "1.0.0",
        "incognito": "invalid_mode",
    }
    with pytest.raises(ValueError):
        ChromeManifest(**manifest_data)


test_cases = [
    (
        "test/test_manifests/manifest_edge_redux.json",
        {
            "name": "Redux DevTools",
            "version": "3.2.7",
            "manifest_version": 3,
            "action": {
                "default_popup": "devpanel.html#popup",
                "default_icon": "img/logo/gray.png",
                "default_title": "Redux DevTools",
            },
            "permissions": ["notifications", "contextMenus", "storage"],
            "host_permissions": ["file:///*", "http://*/*", "https://*/*"],
            "background": {"service_worker": "background.bundle.js"},
        },
    ),
    (
        "test/test_manifests/manifest_edge_redux_v2.json",
        {
            "name": "Redux DevTools",
            "version": "3.1.6",
            "manifest_version": 2,
            "page_action": {
                "default_popup": "window.html#popup",
                "default_icon": "img/logo/gray.png",
                "default_title": "Redux DevTools",
            },
            "permissions": [
                "notifications",
                "contextMenus",
                "storage",
                "file:///*",
                "http://*/*",
                "https://*/*",
            ],
            "background": {"scripts": ["background.bundle.js"], "persistent": False},
            "options_ui": {"page": "options.html", "chrome_style": True},
        },
    ),
    (
        "test/test_manifests/manifest_chrome_redux.json",
        {
            "name": "Redux DevTools",
            "version": "3.2.7",
            "manifest_version": 3,
            "action": {
                "default_popup": "devpanel.html#popup",
                "default_icon": "img/logo/gray.png",
                "default_title": "Redux DevTools",
            },
            "permissions": ["notifications", "contextMenus", "storage"],
            "host_permissions": ["file:///*", "http://*/*", "https://*/*"],
            "background": {"service_worker": "background.bundle.js"},
        },
    ),
    (
        "test/test_manifests/manifest_malicious_poc.json",
        {
            "name": "Hello Extensions",
            "version": "1.0",
            "manifest_version": 3,
            "action": {
                "default_popup": "hello.html",
                "default_icon": "hello_extensions.png",
            },
            "permissions": ["webRequest", "cookies"],
            "host_permissions": ["<all_urls>"],
            "background": {"service_worker": "background.js"},
        },
    ),
    (
        "test/test_manifests/manifest_edge_example.json",
        {
            "name": "NASA picture of the day viewer",
            "version": "0.0.0.1",
            "manifest_version": 3,
            "description": "An extension that uses JavaScript to insert an image at the top of the webpage.",
            "content_scripts": [
                {
                    "matches": ["<all_urls>"],
                    "js": ["lib/jquery.min.js", "content-scripts/content.js"],
                }
            ],
        },
    ),
    (
        "test/test_manifests/manifest_pixiv_batch_downloader.json",
        {
            "name": "Powerful Pixiv Downloader",
            "version": "17.3.1",
            "manifest_version": 3,
            "permissions": [
                "downloads",
                "downloads.shelf",
                "storage",
                "declarativeNetRequestWithHostAccess",
                "webRequest",
            ],
            "incognito": "split",
            "background": {"service_worker": "js/background.js"},
        },
    ),
    (
        "test/test_manifests/manifest_chrome_vite.json",
        {
            "name": "name in manifest.json",
            "manifest_version": 3,
            "description": "description in manifest.json",
            "options_ui": {"page": "src/pages/options/index.html"},
            "action": {
                "default_popup": "src/pages/popup/index.html",
                "default_icon": {"32": "icon-32.png"},
            },
            "permissions": ["activeTab"],
            "content_scripts": [
                {
                    "matches": ["http://*/*", "https://*/*", "<all_urls>"],
                    "js": ["src/pages/content/index.tsx"],
                    "css": ["contentStyle.css"],
                }
            ],
            "devtools_page": "src/pages/devtools/index.html",
        },
    ),
]


@pytest.mark.parametrize("manifest_file,expected", test_cases)
def test_manifest_from_file(manifest_file, expected):
    manifest_data = json.load(open(manifest_file))
    manifest = ChromeManifest(**manifest_data)

    # Check core fields that should exist in all manifests
    assert manifest.name == expected["name"]
    assert manifest.manifest_version == expected["manifest_version"]

    # Check optional fields if they exist in expected

    if "version" in expected:
        assert manifest.version == expected["version"]
    if "action" in expected:
        assert manifest.action == expected["action"]
    if "permissions" in expected:
        assert manifest.permissions == expected["permissions"]
    if "host_permissions" in expected:
        assert manifest.host_permissions == expected["host_permissions"]
    if "content_scripts" in expected:
        assert manifest.content_scripts == expected["content_scripts"]
    if "description" in expected:
        assert manifest.description == expected["description"]
    if "incognito" in expected:
        assert manifest.incognito == expected["incognito"]
