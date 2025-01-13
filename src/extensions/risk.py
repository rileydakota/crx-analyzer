from typing import Union
from extensions.models import ChromePermission, RiskLevel


# credit to https://crxcavator.io/docs.html#/risk_breakdown?id=permissions-breakdown
permissions_risk_map = {
    RiskLevel.NONE: [
        ChromePermission.ALARMS,
        ChromePermission.BROWSING_DATA,
        ChromePermission.CONTEXT_MENUS,
        ChromePermission.DECLARATIVE_CONTENT,
        ChromePermission.ENTERPRISE_DEVICE_ATTRIBUTES,
        ChromePermission.FILE_BROWSER_HANDLER,
        ChromePermission.FONT_SETTINGS,
        ChromePermission.GCM,
        ChromePermission.IDLE,
        ChromePermission.POWER,
        ChromePermission.SESSIONS,
        ChromePermission.SYSTEM_CPU,
        ChromePermission.SYSTEM_DISPLAY,
        ChromePermission.SYSTEM_MEMORY,
        ChromePermission.TTS,
        ChromePermission.UNLIMITED_STORAGE,
        ChromePermission.WALLPAPER,
    ],
    RiskLevel.LOW: [
        ChromePermission.ACTIVE_TAB,
        ChromePermission.BACKGROUND,
        ChromePermission.CERTIFICATE_PROVIDER,
        ChromePermission.DOCUMENT_SCAN,
        ChromePermission.ENTERPRISE_PLATFORM_KEYS,
        ChromePermission.IDENTITY,
        ChromePermission.NOTIFICATIONS,
        ChromePermission.PLATFORM_KEYS,
        ChromePermission.PRINTER_PROVIDER,
        ChromePermission.WEB_REQUEST_BLOCKING,
    ],
    RiskLevel.MEDIUM: [
        ChromePermission.BOOKMARKS,
        ChromePermission.CLIPBOARD_WRITE,
        ChromePermission.DOWNLOADS,
        ChromePermission.FILE_SYSTEM_PROVIDER,
        ChromePermission.GEOLOCATION,
        ChromePermission.MANAGEMENT,
        ChromePermission.NATIVE_MESSAGING,
        ChromePermission.PROCESSES,
        ChromePermission.STORAGE,
        ChromePermission.SYSTEM_STORAGE,
        ChromePermission.TOP_SITES,
        ChromePermission.TTS_ENGINE,
        ChromePermission.WEB_NAVIGATION,
    ],
    RiskLevel.HIGH: [
        ChromePermission.CLIPBOARD_READ,
        ChromePermission.CONTENT_SETTINGS,
        ChromePermission.DECLARATIVE_NET_REQUEST,
        ChromePermission.DESKTOP_CAPTURE,
        ChromePermission.DISPLAY_SOURCE,
        ChromePermission.DNS,
        ChromePermission.EXPERIMENTAL,
        ChromePermission.HISTORY,
        ChromePermission.PAGE_CAPTURE,
        ChromePermission.PRIVACY,
        ChromePermission.PROXY,
        ChromePermission.TAB_CAPTURE,
        ChromePermission.TABS,
        ChromePermission.VPN_PROVIDER,
    ],
    RiskLevel.CRITICAL: [
        ChromePermission.COOKIES,
        ChromePermission.DEBUGGER,
        ChromePermission.WEB_REQUEST,
        ChromePermission.DECLARATIVE_WEB_REQUEST,
        "<all_urls>",
        "https://*/*",
        "http://*/*",
        "*://*/*file:///*",
    ],
}


def get_risk_level(permission: Union[ChromePermission, str]) -> RiskLevel:
    for risk_level, permission_list in permissions_risk_map.items():
        if permission in permission_list:
            return risk_level
    return RiskLevel.NONE
