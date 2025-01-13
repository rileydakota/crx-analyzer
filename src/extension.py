import os
import json
import zipfile
import shutil
import hashlib
import re

from enum import Enum
from requests import HTTPError
import download
from models import ChromeManifest


class InvalidExtensionIDError(Exception):
    pass


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
        self.sha256 = None  # Will be set after download

        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        match self.browser:
            case Browser.CHROME:
                self.download_url = download.get_chrome_extension_url(self.extension_id)
            case Browser.EDGE:
                self.download_url = download.get_edge_extension_url(self.extension_id)
            case _:
                raise ValueError(f"Invalid browser: {self.browser}")
        try:
            self.__download_extension()
        except HTTPError as e:
            match e.response.status_code:
                case 404:
                    raise InvalidExtensionIDError(
                        f"403: Extension ID {self.extension_id} not found. Requested URL: {e.request.url}"
                    )
                case _:
                    raise e

        self.sha256 = hashlib.sha256(
            open(self.extension_zip_path, "rb").read()
        ).hexdigest()
        self.__unzip_extension()

        self.manifest = self.__get_manifest()

    def __unzip_extension(self) -> None:
        with zipfile.ZipFile(self.extension_zip_path, "r") as zip_ref:
            zip_ref.extractall(self.extension_dir_path)

    def __download_extension(self) -> None:
        download.download_extension(self.download_url, self.extension_zip_path)

    def __get_manifest(self) -> ChromeManifest:
        manifest_path = os.path.join(self.extension_dir_path, "manifest.json")
        with open(manifest_path, "r") as manifest_file:
            manifest_data = json.load(manifest_file)

        return ChromeManifest(**manifest_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.extension_zip_path)
        shutil.rmtree(self.extension_dir_path)

    @property
    def name(self) -> str:
        return self.manifest.name

    @property
    def version(self) -> str:
        return self.manifest.version

    @property
    def manifest_version(self) -> int:
        return self.manifest.manifest_version

    @property
    def permissions(self) -> list[str]:
        match self.manifest_version:
            case 2:
                permissions = self.manifest.permissions or []
                optional = self.manifest.optional_permissions or []
                return permissions + optional
            case 3:
                permissions = self.manifest.permissions or []
                optional = self.manifest.optional_permissions or []
                host = self.manifest.host_permissions or []
                optional_host = self.manifest.optional_host_permissions or []
                return permissions + optional + host + optional_host

    @property
    def javascript_files(self) -> list[str]:
        return [
            os.path.join(self.extension_dir_path, file)
            for file in os.listdir(self.extension_dir_path)
            if file.endswith(".js")
        ]

    @property
    def urls(self) -> list[str]:
        urls = set()
        url_pattern = r'https?://[^\s<>"\']+'

        for js_file in self.javascript_files:
            with open(js_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                found_urls = re.findall(url_pattern, content)
                urls.update(found_urls)

        return list(urls)
