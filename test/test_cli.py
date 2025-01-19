import json
import pytest
from click.testing import CliRunner
from crx_analyzer.cli import cli


@pytest.mark.e2e
def test_cli_help():
    """Test basic CLI help output"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: crx-analyzer" in result.output


@pytest.mark.e2e
def test_analyze_command_help():
    """Test analyze command help output"""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Usage: crx-analyzer analyze" in result.output


@pytest.mark.e2e
def test_analyze_chrome_extension(tmp_path):
    """Test analyzing a known Chrome extension"""
    runner = CliRunner()
    extension_id = "nhdogjmejiglipccpnnnanhbledajbpd"  # Redux DevTools
    result = runner.invoke(cli, [
        "analyze",
        "--browser", "chrome",
        "--output", "json",
        "-i", extension_id
    ])
    
    assert result.exit_code == 0
    
    # Parse JSON output directly from result
    report = json.loads(result.output)
    assert report["name"] == "Vue.js devtools"
    assert "risk_score" in report
    assert "permissions" in report


@pytest.mark.e2e
def test_analyze_edge_extension(tmp_path):
    """Test analyzing a known Edge extension"""
    runner = CliRunner()
    extension_id = "nnkgneoiohoecpdiaponcejilbhhikei"  # Edge Redux DevTools
    result = runner.invoke(cli, [
        "analyze",
        "--browser", "edge",
        "--output", "json",
        "-i", extension_id
    ])
    
    assert result.exit_code == 0
    
    # Parse JSON output directly from result
    report = json.loads(result.output)
    assert report["name"] == "Redux DevTools"
    assert "risk_score" in report
    assert "permissions" in report


@pytest.mark.e2e
def test_analyze_invalid_extension():
    """Test analyzing an invalid extension ID"""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "analyze",
        "--browser", "chrome",
        "invalid_extension_id"
    ])
    
    assert result.exit_code != 0
    assert "Missing option '-i' / '--id'" in result.output


@pytest.mark.e2e
def test_analyze_invalid_browser():
    """Test analyzing with invalid browser"""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "analyze",
        "--browser", "invalid",
        "some_extension_id"
    ])
    
    assert result.exit_code != 0
    assert "Invalid value for '-b' / '--browser': 'invalid' is not one of 'chrome', 'edge'" in result.output
