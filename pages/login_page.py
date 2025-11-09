from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_option = "a.link-text-menu:text('Log in')"
        self.username_input = "input[name='username']"  # o usa placeholder si aplica
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.credential_error_message = "div.notification-light.notification-message-light-error:not(.inactive) p"


    def open_login(self):
        """Desde la home, hace clic en el enlace Login."""
        self.click(self.login_option)

    def login(self, username: str, password: str):
        """Llena los campos y hace clic en iniciar sesión."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def login_is_displayed(self) -> bool:
        """Verifica si el botón de login está visible."""
        return self.is_visible(self.login_button)

    def view_error_message(self, timeout=5000) -> bool:
        """Devuelve True si el mensaje de error es visible y tiene texto."""
        try:
            self.page.locator(self.credential_error_message).wait_for(timeout=timeout, state="visible")
            text = self.page.locator(self.credential_error_message).inner_text().strip()
            return text != ""
        except:
            return False