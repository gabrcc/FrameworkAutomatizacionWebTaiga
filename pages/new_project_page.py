from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger
from playwright.sync_api import expect
import re

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
                logger.info("Click en PUBLIC")
                self.public_label.click()
                logger.info("Click en PRIVATE")
                self.private_label.click()
                logger.info("Click en PUBLIC")
                self.public_label.click()
                logger.info("Privacidad alternada (toggle realizado)")
            else:
                logger.error(f"Valor de privacidad inválido: {privacy}")
        except Exception as e:
            logger.error(f"Error al seleccionar privacidad: {e}")
            raise

    def get_required_field_errors(self):
        """Devuelve lista de todos los mensajes 'This value is required.' visibles."""
        errors = self.page.locator("div.error-text:has-text('This value is required.')")
        count = errors.count()
        messages = []
        for i in range(count):
            messages.append(errors.nth(i).inner_text().strip())
        return messages
    
    def submit_load_state(self):
        """
        Verifica que el botón entró en estado 'loading'
        (caso esperado cuando el nombre excede el límite o hay error).
        """
        try:
            # 1. El botón debe tener la clase loading
            expect(self.submit_button).to_have_class(re.compile("loading"))

            # 2. Debe existir el spinner
            spinner = self.submit_button.locator("img.loading-spinner")
            expect(spinner).to_be_visible()

            logger.info("OK -> El botón entró en estado LOADING correctamente.")
            return True
        except Exception as e:
            logger.error(f"ERROR -> El botón NO entró en estado loading. {e}")
            return False