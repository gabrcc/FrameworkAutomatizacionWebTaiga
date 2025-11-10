from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class TypeProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.kanban_option = "a[tg-nav='create-project-kanban'][title='Kanban']"

    def select_kanban(self):
        """Hace clic en la opción Kanban para crear un proyecto"""
        try:
            self.page.locator(self.kanban_option).click()
            logger.info("Opción 'Kanban' seleccionada correctamente")
        except Exception as e:
            logger.error(f"No se pudo seleccionar la opción 'Kanban': {e}")
            raise
