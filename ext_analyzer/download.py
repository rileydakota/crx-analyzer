import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
CHROME_VERSION = "131.0.6778.265"
EDGE_VERSION = "130.0.2849.142"


def get_chrome_extension_url(
    extension_id: str, chrome_version: str = CHROME_VERSION
) -> str:
    return f"https://clients2.google.com/service/update2/crx?response=redirect&os=mac&arch=arm64&os_arch=arm64&nacl_arch=arm&prod=chromecrx&prodchannel=&prodversion={chrome_version}&lang=en-US&acceptformat=crx3,puff&x=id%3D{extension_id}%26installsource%3Dondemand%26uc&authuser=0"


def get_edge_extension_url(extension_id: str, edge_version: str = EDGE_VERSION) -> str:
    return f"https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&os=linux&arch=x64&os_arch=x86_64&nacl_arch=x86-64&prod=chromiumcrx&prodchannel=dev&prodversion={edge_version}&lang=en-US&acceptformat=crx3&x=id%3D{extension_id}%26installsource%3Dondemand%26uc"


def download_extension(url: str, output_path: str) -> None:
    """Downloads Chrome extension to specified path using extension ID.

    Args:
        extension_id: ID of the Chrome extension to download
        output_path: Local file path where extension should be saved
    """

    response = requests.get(
        url, allow_redirects=True, headers={"User-Agent": USER_AGENT}
    )
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)
