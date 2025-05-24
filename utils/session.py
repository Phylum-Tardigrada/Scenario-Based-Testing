from playwright.sync_api import sync_playwright, Playwright, Browser
import os
import time
from datetime import datetime
from pathlib import Path


class Session:
    def __init__(self, **confs):
        self.confs = confs
        self.framework: Playwright = None
        self.browser: Browser = None

    def __enter__(self):

        now = datetime.now()
        self.confs['run'] = f"out_{int(now.timestamp())}"  # Folder Name
        self.confs['ts'] = now.isoformat()  # Session Time (ISO Format)
        # Create a folder with the current timestamp as its name
        os.makedirs(Path(self.confs['run']).absolute(), exist_ok=True)

        self.framework = sync_playwright().start()
        self.browser = self.framework.chromium.launch(
            headless=self.confs.get('headless', False))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.framework:
            self.framework.stop()

    def new_page(
        self,
        **kwargs
    ):
        if hasattr(self, 'context'):
            self.context.close()
            time.sleep(2)
        self.context = self.browser.new_context(**kwargs)
        return self.context.new_page()