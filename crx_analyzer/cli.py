import click
from importlib.metadata import version
from rich.console import Console
from rich.table import Table
from .extension import Extension, Browser
from .risk import get_risk_report
from .models import RiskLevel


@click.group(name="crx-analyzer")
def cli():
    pass


@cli.command(name="version")
def get_version():
    print(version("crx_analyzer"))


@cli.command(name="analyze")
@click.option(
    "-i", "--id", type=str, help="The ID of the extension to check", required=True
)
@click.option(
    "-b",
    "--browser",
    type=click.Choice(["chrome", "edge"]),
    help="The browser the extension id is associated with",
    required=True,
)
@click.option(
    "--output",
    type=click.Choice(["json", "pretty"]),
    default="pretty",
    help="Output format",
    required=True,
)
@click.option(
    "--max-files",
    type=int,
    default=10,
    help="Maximum number of JavaScript files to display",
)
@click.option(
    "--max-urls",
    type=int,
    default=10,
    help="Maximum number of URLs to display",
)
@click.option(
    "--permissions",
    is_flag=True,
    help="Display only permissions and metadata tables",
)
def analyze(id, browser, output, max_files, max_urls, permissions):
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
            metadata_table.add_row("Hash (SHA256)", extension.sha256)
            metadata_table.add_row("Homepage", extension.homepage_url)
            metadata_table.add_row("Version", extension.version)
            metadata_table.add_row("Manifest Version", str(extension.manifest_version))
            metadata_table.add_row("Risk Score", f"{report.risk_score}/100")

            # Add both tables to grid
            grid.add_column(justify="left")
            grid.add_column(justify="right")
            grid.add_row(metadata_table, permissions_table)

            console = Console(force_terminal=True)
            console.print("\n")
            console.print(
                f"[bold blue reverse white]{browser} extension analysis for extension id {id}",
                justify="center",
            )
            console.print("\n" * 3)
            console.print(grid)

            if not permissions:
                js_files_table = Table(title="JavaScript Files")
                js_files_table.add_column("File")
                for file in report.javascript_files[:max_files]:
                    js_files_table.add_row(file)

                url_ref_table = Table(title="URLs Referenced")
                url_ref_table.add_column("URL")
                for url in report.urls[:max_urls]:
                    url_ref_table.add_row(url)

                console.print(js_files_table)
                console.print(url_ref_table)

                if len(report.javascript_files) > max_files:
                    console.print(
                        f"\n[yellow]Showing {max_files} of {len(report.javascript_files)} JavaScript files. Use --max-files=INT or --output json to show more."
                    )
                if len(report.urls) > max_urls:
                    console.print(
                        f"[yellow]Showing {max_urls} of {len(report.urls)} URLs. Use --max-urls=INT or --output json to show more."
                    )
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
