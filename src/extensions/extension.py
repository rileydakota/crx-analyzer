import os
import json
import zipfile
from enum import Enum

import download
from models.manifest import Manifest


class Browser(Enum):
    CHROME = "chrome"
    EDGE = "edge"


class Extension:
    def __init__(self, extension_id: str, browser: Browser, working_dir: str = "tmp"):
        self.extension_id = extension_id
        self.working_dir = working_dir
        self.browser = browser
        self.extension_zip_path = os.path.join(working_dir, f"{self.extension_id}.crx")
        self.extension_dir_path = os.path.join(working_dir, f"{self.extension_id}")

        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        match self.browser:
            case Browser.CHROME:
                self.download_url = download.get_chrome_extension_url(self.extension_id)
            case Browser.EDGE:
                self.download_url = download.get_edge_extension_url(self.extension_id)

        self.__download_extension()
        self.__unzip_extension()

        self.manifest = self.__get_manifest()

    def __unzip_extension(self):
        with zipfile.ZipFile(self.extension_zip_path, "r") as zip_ref:
            zip_ref.extractall(self.working_dir)

    def __download_extension(self):
        download.download_extension(self.download_url, self.extension_zip_path)

    def __get_manifest(self):
        manifest_path = os.path.join(self.extension_dir_path, "manifest.json")
        with open(manifest_path, "r") as manifest_file:
            manifest_data = json.load(manifest_file)
            return Manifest(manifest_data)

    def __exit__(self):
        os.remove(self.extension_zip_path)
        os.rmdir(self.extension_dir_path)
