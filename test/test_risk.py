from unittest.mock import Mock
from crx_analyzer.risk import get_risk_level, get_risk_score, get_risk_report
from crx_analyzer.models import ChromePermission, RiskLevel


def test_permission_risk_level():
    assert get_risk_level(ChromePermission.COOKIES) == RiskLevel.CRITICAL
    assert get_risk_level(ChromePermission.DEBUGGER) == RiskLevel.CRITICAL
    assert get_risk_level(ChromePermission.WEB_REQUEST) == RiskLevel.CRITICAL
    assert get_risk_level(ChromePermission.GEOLOCATION) == RiskLevel.MEDIUM
    assert get_risk_level(ChromePermission.ALARMS) == RiskLevel.NONE
    assert get_risk_level(ChromePermission.ACTIVE_TAB) == RiskLevel.LOW
    assert get_risk_level("unknown_permission") == RiskLevel.NONE


def test_risk_score():
    assert get_risk_score(RiskLevel.NONE) == 0
    assert get_risk_score(RiskLevel.LOW) == 5
    assert get_risk_score(RiskLevel.MEDIUM) == 10
    assert get_risk_score(RiskLevel.HIGH) == 15
    assert get_risk_score(RiskLevel.CRITICAL) == 45


def test_risk_report():
    # Mock an extension
    extension = Mock()
    extension.name = "Test Extension"
    extension.sha256 = "test_hash"
    extension.permissions = [ChromePermission.COOKIES, ChromePermission.STORAGE]
    extension.javascript_files = ["test.js"]
    extension.urls = ["https://example.com"]

    report = get_risk_report(extension)
    assert report.name == "Test Extension"
    assert report.sha256 == "test_hash"
    assert report.risk_score == 55  # CRITICAL(45) + MEDIUM(10)
    assert len(report.permissions) == 2
    assert report.permissions[0].permission == ChromePermission.COOKIES
    assert report.permissions[0].risk_level == RiskLevel.CRITICAL
    assert report.permissions[1].permission == ChromePermission.STORAGE
    assert report.permissions[1].risk_level == RiskLevel.MEDIUM


def test_risk_score_max():
    # Test that risk score is capped at 100
    extension = Mock()
    extension.name = "Test Extension"
    extension.sha256 = "test_hash"
    extension.permissions = [ChromePermission.COOKIES] * 3  # 3 * 45 would be 135
    extension.javascript_files = []
    extension.urls = []

    report = get_risk_report(extension)
    assert report.risk_score == 100
