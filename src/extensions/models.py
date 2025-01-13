from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class IncognitoMode(str, Enum):
    SPANNING = "spanning"
    SPLIT = "split"
    NOT_ALLOWED = "not_allowed"


class FileSystemProviderCapabilities(BaseModel):
    configurable: bool = False
    multiple_mounts: bool = False
    source: str = "network"


class OmniboxConfig(BaseModel):
    keyword: str


class OptionsUI(BaseModel):
    chrome_style: bool = True
    page: str


class BackgroundConfig(BaseModel):
    service_worker: Optional[str] = None
    persistent: bool = False


class ExternallyConnectable(BaseModel):
    matches: Optional[List[str]] = None
    ids: Optional[List[str]] = None
    accepts_tls_channel_id: Optional[bool] = None


class CrossOriginPolicy(BaseModel):
    value: str


class ImportConfig(BaseModel):
    id: str = Field(..., pattern="^[a-zA-Z0-9]{32}$")


class Storage(BaseModel):
    managed_schema: str


class SidePanel(BaseModel):
    default_path: Optional[str] = None


class ChromePermission(str, Enum):
    # Accessibility
    ACCESSIBILITY_FEATURES_MODIFY = "accessibilityFeatures.modify"
    ACCESSIBILITY_FEATURES_READ = "accessibilityFeatures.read"

    # Tab & Window Management
    ACTIVE_TAB = "activeTab"
    TABS = "tabs"
    TAB_CAPTURE = "tabCapture"
    TAB_GROUPS = "tabGroups"

    # System APIs
    ALARMS = "alarms"
    AUDIO = "audio"
    BACKGROUND = "background"
    BOOKMARKS = "bookmarks"
    BROWSING_DATA = "browsingData"

    # Security & Authentication
    CERTIFICATE_PROVIDER = "certificateProvider"
    WEB_AUTHENTICATION_PROXY = "webAuthenticationProxy"

    # Clipboard
    CLIPBOARD_READ = "clipboardRead"
    CLIPBOARD_WRITE = "clipboardWrite"

    # Content & Settings
    CONTENT_SETTINGS = "contentSettings"
    CONTEXT_MENUS = "contextMenus"
    COOKIES = "cookies"

    # Debugging & Development
    DEBUGGER = "debugger"
    DECLARATIVE_CONTENT = "declarativeContent"
    DECLARATIVE_NET_REQUEST = "declarativeNetRequest"
    DECLARATIVE_NET_REQUEST_WITH_HOST_ACCESS = "declarativeNetRequestWithHostAccess"
    DECLARATIVE_NET_REQUEST_FEEDBACK = "declarativeNetRequestFeedback"
    DECLARATIVE_WEB_REQUEST = "declarativeWebRequest"
    EXPERIMENTAL = "experimental"
    # System Features
    DNS = "dns"
    DESKTOP_CAPTURE = "desktopCapture"
    DOCUMENT_SCAN = "documentScan"
    DISPLAY_SOURCE = "displaySource"
    # Downloads
    DOWNLOADS = "downloads"
    DOWNLOADS_OPEN = "downloads.open"
    DOWNLOADS_UI = "downloads.ui"

    # Enterprise
    ENTERPRISE_DEVICE_ATTRIBUTES = "enterprise.deviceAttributes"
    ENTERPRISE_HARDWARE_PLATFORM = "enterprise.hardwarePlatform"
    ENTERPRISE_NETWORKING_ATTRIBUTES = "enterprise.networkingAttributes"
    ENTERPRISE_PLATFORM_KEYS = "enterprise.platformKeys"

    # Files & Storage
    FAVICON = "favicon"
    FILE_BROWSER_HANDLER = "fileBrowserHandler"
    FILE_SYSTEM_PROVIDER = "fileSystemProvider"
    UNLIMITED_STORAGE = "unlimitedStorage"

    # Appearance
    FONT_SETTINGS = "fontSettings"
    WALLPAPER = "wallpaper"

    # Messaging & Communication
    GCM = "gcm"
    NATIVE_MESSAGING = "nativeMessaging"

    # Location & Hardware
    GEOLOCATION = "geolocation"

    # History & Sessions
    HISTORY = "history"
    SESSIONS = "sessions"

    # Identity & Authentication
    IDENTITY = "identity"
    IDENTITY_EMAIL = "identity.email"

    # System State
    IDLE = "idle"
    LOGIN_STATE = "loginState"

    # Management
    MANAGEMENT = "management"

    # UI & Notifications
    NOTIFICATIONS = "notifications"
    OFFSCREEN = "offscreen"
    SIDE_PANEL = "sidePanel"

    # Page Interaction
    PAGE_CAPTURE = "pageCapture"
    PLATFORM_KEYS = "platformKeys"

    # Power Management
    POWER = "power"

    # Printing
    PRINTER_PROVIDER = "printerProvider"
    PRINTING = "printing"
    PRINTING_METRICS = "printingMetrics"

    # Privacy & Security
    PRIVACY = "privacy"
    PROXY = "proxy"

    # System Processes
    PROCESSES = "processes"

    # Reading & Content
    READING_LIST = "readingList"

    # Runtime
    RUNTIME = "runtime"
    SCRIPTING = "scripting"

    # Search & Navigation
    SEARCH = "search"
    TOP_SITES = "topSites"

    # Storage
    STORAGE = "storage"

    # System Information
    SYSTEM_CPU = "system.cpu"
    SYSTEM_DISPLAY = "system.display"
    SYSTEM_MEMORY = "system.memory"
    SYSTEM_STORAGE = "system.storage"

    # Text-to-Speech
    TTS = "tts"
    TTS_ENGINE = "ttsEngine"

    # Network
    VPN_PROVIDER = "vpnProvider"
    WEB_NAVIGATION = "webNavigation"
    WEB_REQUEST = "webRequest"
    WEB_REQUEST_BLOCKING = "webRequestBlocking"


class ChromeManifest(BaseModel):
    # Required fields
    manifest_version: int = Field(..., Literal=[1, 2, 3])
    name: str

    # Recommended fields
    default_locale: Optional[str] = "en"
    description: Optional[str] = None
    icons: Optional[Dict[str, str]] = None

    # Optional fields
    version: Optional[str] = None
    action: Optional[Dict[str, Any]] = None
    author: Optional[str] = None
    automation: Optional[Any] = None
    background: Optional[BackgroundConfig] = None
    chrome_settings_overrides: Optional[Dict[str, Any]] = None
    chrome_url_overrides: Optional[Dict[str, Any]] = None
    commands: Optional[Dict[str, Any]] = None
    content_capabilities: Optional[Any] = None
    content_scripts: Optional[List[Dict[str, Any]]] = None
    content_security_policy: Optional[Union[Dict[str, str], str]] = None
    converted_from_user_script: Optional[Any] = None
    cross_origin_embedder_policy: Optional[CrossOriginPolicy] = None
    cross_origin_opener_policy: Optional[CrossOriginPolicy] = None
    current_locale: Optional[str] = None
    declarative_net_request: Optional[Any] = None
    devtools_page: Optional[str] = None
    differential_fingerprint: Optional[Any] = None
    event_rules: Optional[List[Dict[str, Any]]] = None
    externally_connectable: Optional[ExternallyConnectable] = None
    file_browser_handlers: Optional[List[Any]] = None
    file_system_provider_capabilities: Optional[FileSystemProviderCapabilities] = None
    homepage_url: Optional[HttpUrl] = None
    host_permissions: Optional[List[str]] = None
    import_: Optional[List[ImportConfig]] = Field(None, alias="import")
    incognito: Optional[IncognitoMode] = None
    input_components: Optional[Any] = None
    key: Optional[str] = None
    minimum_chrome_version: Optional[str] = None
    nacl_modules: Optional[List[Any]] = None
    natively_connectable: Optional[Any] = None
    oauth2: Optional[Any] = None
    offline_enabled: Optional[bool] = None
    omnibox: Optional[OmniboxConfig] = None
    optional_permissions: Optional[List[Union[ChromePermission, str]]] = None
    optional_host_permissions: Optional[List[str]] = None
    options_page: Optional[str] = None
    options_ui: Optional[OptionsUI] = None
    permissions: Optional[List[Union[ChromePermission, str]]] = None
    platforms: Optional[Any] = None
    replacement_web_app: Optional[Any] = None
    requirements: Optional[Dict[str, Any]] = None
    sandbox: Optional[List[str]] = None
    short_name: Optional[str] = None
    side_panel: Optional[SidePanel] = None
    storage: Optional[Storage] = None
    system_indicator: Optional[Any] = None
    tts_engine: Optional[Dict[str, Any]] = None
    update_url: Optional[HttpUrl] = None
    version_name: Optional[str] = None
    web_accessible_resources: Optional[List[Union[Dict[str, Any], str]]] = None


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
