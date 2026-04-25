from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import time

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        
    def start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            # Launch chromium in non-headless mode so the user can see it
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

    def ensure_started(self):
        if not self.page or self.page.is_closed():
            self.start()

    def open_url(self, url: str):
        self.ensure_started()
        if not url.startswith("http"):
            url = "https://" + url
        self.page.goto(url)

    def click_link(self, text: str):
        self.ensure_started()
        # Look for a link or button containing the text
        locator = self.page.locator(f"text='{text}'").first
        if locator.count() > 0:
            locator.click()
            return True
        else:
            raise Exception(f"Could not find a link with text '{text}'")

    def scroll_up(self):
        self.ensure_started()
        self.page.mouse.wheel(delta_x=0, delta_y=-800)

    def scroll_down(self):
        self.ensure_started()
        self.page.mouse.wheel(delta_x=0, delta_y=800)

    def go_back(self):
        self.ensure_started()
        self.page.go_back()

    def close(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
