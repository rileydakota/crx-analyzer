import pytest
from click.testing import CliRunner
from crx_analyzer.cli import cli

test_cases = [
    # Edge extensions
    ("edge", "nnkgneoiohoecpdiaponcejilbhhikei"),  # Redux DevTools
    ("edge", "njpoigijhgbionbfdbaopheedbpdoddi"),  # JSON Formatter
    ("edge", "bdaafgjhhjkdplpffldcncdignokfkbo"),  # Norton Safe Web
    ("edge", "fphgeikpdcdcheaochkhldmnfblfogla"),  # NordVPN
    ("edge", "icahgcdchandbkbhminlkmeljdoflpoi"),  # Elder Scrolls Skyrim
    ("edge", "iifjijkgednpbhdbgoopbmikphckgbfj"),  # Google to Microsoft CDN
    ("edge", "eghgdppgmgnipiomjkkhhcihpogpcodk"),  # AI Tweet Regenerator
    # Chrome extensions
    # Chrome security/privacy extensions
    ("chrome", "gighmmpiobklfepjocnamgkkbiglidom"),  # AdBlock
    ("chrome", "cfhdojbkjhnklbpkdaibdccddilifddb"),  # AdBlock Plus
    ("chrome", "epcnnfbjfcgphgdmggkamkmgojdagdnn"),  # uBlock
    ("chrome", "cjpalhdlnbpafiamejdnhcphjbkeiagm"),  # uBlock Origin
    ("chrome", "mlomiejdfkolichcflejclcbmpeaniij"),  # Ghostery
    ("chrome", "jeoacafpbcihiomhlakheieifhpjdfeo"),  # Disconnect
    ("chrome", "efbjojhplkelaegfbieplglfidafgoka"),  # VTchromizer
    ("chrome", "aleggpabliehgbeagmfhnodcijcmbonb"),  # Dr Web Link Checker
    ("chrome", "eaijffijbobmnonfhilihbejadplhddo"),  # Bitwarden
    ("chrome", "hdokiejnpimakedhajhdlcegeplioahd"),  # LastPass
    ("chrome", "ojkchikaholjmcnefhjlbohackpeeknd"),  # Vue.js devtools
    ("chrome", "bmnlcjabgnpnenekpadlanbbkooimhnj"),  # Honey
    ("chrome", "ccbpbkebodcjkknkfkpmfeciinhidaeh"),  # Avira
    ("chrome", "dnhpnfgdlenaccegplpojghhmaamnnfp"),  # Augmented Steam
]


@pytest.mark.e2e
@pytest.mark.parametrize("browser,extension_id", test_cases)
def test_analyze_extension_nightly(browser, extension_id):
    """Test that analyzing extensions completes successfully"""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--browser", browser, "-i", extension_id])

    assert result.exit_code == 0
