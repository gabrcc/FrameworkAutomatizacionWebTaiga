from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class NewProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators del formulario
        self.project_name_input = "input[name='project-name']"
        self.project_description_input = "textarea[ng-model='vm.projectForm.description']"
        self.public_radio = "input#template-public"
        self.private_radio = "input#template-private"
        self.submit_button = "button.create-project-action-submit"

    def fill_form(self, name: str, description: str, private: bool = False):
        """Llena el formulario de creación de proyecto"""
        try:
            self.page.locator(self.project_name_input).fill(name)
            self.page.locator(self.project_description_input).fill(description)
            if private:
                self.page.locator(self.private_radio).check()
                logger.info(f"Seleccionada opción 'Private Project' para '{name}'")
            else:
                self.page.locator(self.public_radio).check()
                logger.info(f"Seleccionada opción 'Public Project' para '{name}'")
            logger.info(f"Formulario llenado correctamente para el proyecto '{name}'")
        except Exception as e:
            logger.error(f"Error llenando el formulario del proyecto '{name}': {e}")
            raise

    def submit_form(self):
        """Hace clic en el botón 'Create Project'"""
        try:
            self.page.locator(self.submit_button).click()
            logger.info("Botón 'Create Project' presionado correctamente")
        except Exception as e:
            logger.error(f"No se pudo enviar el formulario de creación de proyecto: {e}")
            raise
