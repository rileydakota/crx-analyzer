import click
from extensions.extension import Extension, Browser


@click.command()
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
    print(extension.name)
    print(extension.version)
    print(extension.manifest_version)
    print(extension.permissions)
    print(extension.javascript_files)
    print(extension.urls)


if __name__ == "__main__":
    cli()
