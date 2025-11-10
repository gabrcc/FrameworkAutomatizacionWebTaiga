from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO

class ProjectsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.new_project_button = "a.create-project-btn[title='New project']"

    def click_new_project(self):
        """Hace clic en el botón 'New project'"""
        try:
            self.page.locator(self.new_project_button).nth(1).click()
            logger.info("Se hizo clic en 'New project'")
        except Exception as e:
            logger.error(f"No se pudo hacer clic en 'New project': {e}")
            raise
