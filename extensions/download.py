import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_chrome_extension_url(extension_id: str) -> str:
    return f"https://clients2.google.com/service/update2/crx?response=redirect&os=linux&arch=x64&os_arch=x86_64&nacl_arch=x86-64&prod=chromecrx&prodchannel=&prodversion=87.0.4280.88&lang=en-US&acceptformat=zip&x=id%3D{extension_id}%26installsource%3Dondemand%26uc"

def get_edge_extension_url(extension_id: str) -> str:
     return f"https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&os=linux&arch=x64&os_arch=x86_64&nacl_arch=x86-64&prod=chromiumcrx&prodchannel=dev&prodversion=89.0.731.0&lang=en-US&acceptformat=crx3&x=id%3D{extension_id}%26installsource%3Dondemand%26uc"

def download_extension(url: str, output_path: str) -> None:
     """Downloads Chrome extension to specified path using extension ID.
     
     Args:
         extension_id: ID of the Chrome extension to download
         output_path: Local file path where extension should be saved
     """     
     
     response = requests.get(url, allow_redirects=True, headers={"User-Agent": USER_AGENT})
     
     with open(output_path, 'wb') as f:
          f.write(response.content)
