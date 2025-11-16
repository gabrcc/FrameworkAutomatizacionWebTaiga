class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)

    def get_text(self, selector):
        return self.page.text_content(selector)

    def is_visible(self, selector):
        return self.page.is_visible(selector)
    
    def close_cookie_warning(self):
        cookie_close = self.page.locator("cookie-warning a.close")
        if cookie_close.is_visible():
            cookie_close.click()
