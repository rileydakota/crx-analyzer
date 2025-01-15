from crx_analyzer.risk import get_risk_level
from crx_analyzer.models import ChromePermission, RiskLevel


def test_permission_risk_level():
    assert get_risk_level(ChromePermission.COOKIES) == RiskLevel.CRITICAL
    assert get_risk_level(ChromePermission.DEBUGGER) == RiskLevel.CRITICAL
    assert get_risk_level(ChromePermission.WEB_REQUEST) == RiskLevel.CRITICAL
    assert get_risk_level(ChromePermission.GEOLOCATION) == RiskLevel.MEDIUM
