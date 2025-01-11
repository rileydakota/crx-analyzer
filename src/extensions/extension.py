from enum import Enum

class Browser(Enum):
    CHROME = "chrome"
    EDGE = "edge"

class Extension:
    def __init__(self, extension_id: str, browser: Browser, working_dir: str = "tmp"):
        self.extension_id = extension_id
        self.working_dir = working_dir
        self.browser = browser