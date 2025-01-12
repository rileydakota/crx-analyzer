import os
import json
import zipfile
import shutil
from enum import Enum

import src.extensions.download as download
from src.extensions.models import ChromeManifest


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
            zip_ref.extractall(self.extension_dir_path)

    def __download_extension(self):
        download.download_extension(self.download_url, self.extension_zip_path)

    def __get_manifest(self):
        manifest_path = os.path.join(self.extension_dir_path, "manifest.json")
        with open(manifest_path, "r") as manifest_file:
            manifest_data = json.load(manifest_file)

        return ChromeManifest(**manifest_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.extension_zip_path)
        shutil.rmtree(self.extension_dir_path)
