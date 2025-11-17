from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class NewProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators del formulario
        self.project_name_input = page.locator("input[name='project-name']")
        self.project_description_input = page.locator("textarea[ng-model='vm.projectForm.description']")
        self.public_label = page.locator("label[for='template-public']")
        self.private_label = page.locator("label[for='template-private']")
        self.submit_button = page.locator("button.create-project-action-submit")

    def fill_form(self, name: str, description: str):
        """Llena el formulario de creación de proyecto"""
        try:
            self.project_name_input.fill(name)
            self.project_description_input.fill(description)
            logger.info(f"Llenando espacios requeridos del formulario para crear el proyecto '{name}'")
        except Exception as e:
            logger.error(f"Error llenando el formulario del proyecto '{name}': {e}")
            raise

    def submit_form(self):
        """Hace clic en el botón 'Create Project'"""
        try:
            self.submit_button.click()
            logger.info("Botón 'Create Project' presionado correctamente")
        except Exception as e:
            logger.error(f"No se pudo enviar el formulario de creación de proyecto: {e}")
            raise
    
    def set_privacy(self, privacy: str):
        """Define privacy: public, private o toggle."""
        try:
            if privacy == "public":
                self.public_label.click()
                logger.info("Privacidad seleccionada: PUBLIC")
            elif privacy == "private":
                self.private_label.click()
                logger.info("Privacidad seleccionada: PRIVATE")
            elif privacy == "toggle":
                self.public_label.click()
                self.private_label.click()
                self.public_label.click()
                logger.info("Privacidad alternada (toggle realizado)")
            else:
                logger.error(f"Valor de privacidad inválido: {privacy}")
        except Exception as e:
            logger.error(f"Error al seleccionar privacidad: {e}")
            raise