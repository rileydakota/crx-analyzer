import click
from rich.console import Console
from rich.table import Table
from extension import Extension, Browser
from risk import get_risk_report
from models import RiskLevel


@click.command(name="crx-analysis")
@click.option("--id", type=str, help="The ID of the extension to check", required=True)
@click.option(
    "--browser",
    type=click.Choice(["chrome", "edge"]),
    help="The browser the extension id is associated with (chrome or edge)",
    required=True,
)
@click.option(
    "--output",
    type=click.Choice(["json", "pretty"]),
    default="pretty",
    help="Output format (json or pretty)",
    required=True,
)
def cli(id, browser, output):
    browser_enum = Browser(browser)
    extension = Extension(id, browser_enum)
    report = get_risk_report(extension)

    match output:
        case "pretty":
            grid = Table.grid(expand=True)
            permissions_table = Table(title="Extension Permissions")
            permissions_table.add_column("Permission")
            permissions_table.add_column("Risk Level")

            # Sort permissions by risk level
            sorted_permissions = sorted(
                report.permissions,
                key=lambda p: RiskLevel[p.risk_level.upper()].value,
            )

            for permission in sorted_permissions:
                match permission.risk_level:
                    case RiskLevel.NONE:
                        perm_str = f"[light_green]{permission.permission}"
                    case RiskLevel.LOW:
                        perm_str = f"[dark_green]{permission.permission}"
                    case RiskLevel.MEDIUM:
                        perm_str = f"[bright_yellow]{permission.permission}"
                    case RiskLevel.HIGH:
                        perm_str = f"[dark_orange]{permission.permission}"
                    case RiskLevel.CRITICAL:
                        perm_str = f"[red1]{permission.permission}"
                permissions_table.add_row(perm_str, permission.risk_level.upper())

            # Create metadata table
            metadata_table = Table(title="Extension Metadata")
            metadata_table.add_column("Field")
            metadata_table.add_column("Value")
            metadata_table.add_row("Name", extension.name)
            metadata_table.add_row("Author", extension.author)
            metadata_table.add_row("Homepage", extension.homepage_url)
            metadata_table.add_row("Version", extension.version)
            metadata_table.add_row("Manifest Version", str(extension.manifest_version))
            metadata_table.add_row("Risk Score", f"{report.risk_score}/100")

            # Add both tables to grid
            grid.add_column(justify="left")
            grid.add_column(justify="right")
            grid.add_row(metadata_table, permissions_table)

            console = Console()
            console.print("\n")
            console.print(
                f"[bold blue reverse]{browser} extension analysis for extesnion id {id}",
                justify="center",
            )
            console.print("\n" * 3)
            console.print(grid)
            console.print(report.javascript_files)
            console.print(report.urls)
        case "json":
            print(report.json())

    # print(extension.name)
    # print(extension.version)
    # print(extension.manifest_version)
    # print(extension.permissions)
    # print(extension.javascript_files)
    # print(extension.urls)


if __name__ == "__main__":
    cli()
