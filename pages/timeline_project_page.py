from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class TimeLineProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.projects_button = "a.dropdown-project-list-projects[title='Projects']"
        self.view_all_projects_option = 'a.see-more-projects-btn[tg-nav="projects"]' 
        self.settings_link = page.locator("use[href='#settings']")
        self.delete_project_link = page.locator("a.delete-project[title='Delete this project']")
        self.close_cookie_btn = page.locator("cookie-warning a.close")
        self.confirm_delete_button = page.locator("button.btn-confirm.js-confirm",has_text="Yes, I'm really sure")
        self.cancel_delete_button = page.get_by_role("button", name="Cancel")

    def go_to_projects(self):
        self.click(self.projects_button)
        self.click(self.view_all_projects_option)

    def delete_project(self, project_name: str):
        """Elimina un proyecto por su nombre desde la lista de Projects"""
        if self.close_cookie_btn.is_visible():
            self.close_cookie_warning()
            
        try:
            self.settings_link.wait_for(state="visible", timeout=10000)
            self.settings_link.click()
            self.delete_project_link.wait_for(state="visible", timeout=10000)
            self.delete_project_link.click()
            logger.info(f"Click en boton delete del proyecto {project_name}")
        except Exception as e:
            logger.error(f"No se pudo eliminar el proyecto '{project_name}': {e}")
            raise

    def confirm_delete(self):
        """Confirma la eliminación de un proyecto"""
        try:
            self.confirm_delete_button.click()
            logger.info("Confirmar eliminar de proyecto")
        except Exception as e:
            logger.error(f"No se pudo confirmar la eliminación del proyecto: {e}")
            raise

    def cancel_delete(self):
        try:
            # Espera a que el modal de eliminación esté visible
            self.page.locator("div.lightbox-delete-project.open").wait_for(
                state="visible", timeout=8000
            )

            # Localiza el botón cancel dentro del modal
            cancel_btn = self.page.locator("div.lightbox-delete-project.open button.js-cancel")

            cancel_btn.wait_for(state="visible", timeout=5000)
            cancel_btn.click()

            logger.info("Cancelación de eliminación ejecutada correctamente")
        except Exception as e:
            logger.error(f"No se pudo cancelar la eliminación del proyecto: {e}")
            raise
