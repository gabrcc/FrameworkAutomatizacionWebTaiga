from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class TimeLineProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_icon = "a.logo[title='Homepage']"

    def go_to_dashboard(self):
        """Hace clic en la icono de Dashboard"""
        try:
            self.page.locator(self.dashboard_icon).click()
            logger.info("Se hizo clic en el logo para ir a Homepage")
        except Exception as e:
            logger.error(f"No se pudo ir a Homepage: {e}")
            raise