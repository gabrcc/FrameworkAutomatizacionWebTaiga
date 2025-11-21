from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger
from playwright.sync_api import expect
import time

logger = setup_logger("timeline_project.log", level=20)  # INFO


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
        self.edit_name_input = page.locator("input#project-name")
        self.edit_description_input = page.locator("textarea#project-description")
        self.save_button = page.locator("button[title='Save']")
        self.public_label = page.locator("label[for='public-project']")
        self.private_label = page.locator("label[for='private-project']")
        self.success_notification_msg = page.locator("div.notification-message-success")
        self.project_info = page.locator("h1 .project-link .project-name")
        self.private_icon = page.locator("svg.icon-private")

    def go_to_projects(self):
        self.click(self.projects_button)
        self.click(self.view_all_projects_option)

    def open_settings(self):
        if self.close_cookie_btn.is_visible():
            self.close_cookie_warning()
        try:
            self.settings_link.wait_for(state="visible", timeout=10000)
            self.settings_link.click()
            logger.info("Click en settings")
        except Exception as e:
            logger.error(f"No se pudo abrir settings': {e}")
            raise

    def delete_project(self, project_name: str):
        """Elimina un proyecto por su nombre desde la lista de Projects"""
        if self.close_cookie_btn.is_visible():
            self.close_cookie_warning()
            
        try:
            # self.settings_link.wait_for(state="visible", timeout=10000)
            # self.settings_link.click()
            self.open_settings()
            self.delete_project_link.wait_for(state="visible", timeout=10000)
            self.delete_project_link.click()
            logger.info(f"Click en boton delete del proyecto {project_name}")
        except Exception as e:
            logger.error(f"No se pudo eliminar el proyecto '{project_name}': {e}")
            raise

    def confirm_delete(self, project_name: str):
        """Confirma la eliminación de un proyecto"""
        try:
            self.confirm_delete_button.click()
            logger.info("Confirmar eliminar de proyecto")
        except Exception as e:
            logger.error(f"No se pudo confirmar la eliminación del proyecto {project_name}: {e}")
            raise

    def save_changes(self):
        """Guarda los cambios realizados en el modal de edición"""
        try:
            self.save_button.wait_for(state="visible", timeout=10000)
            self.save_button.click()
            logger.info("Cambios guardados correctamente")
        except Exception as e:
            logger.error(f"No se pudo guardar los cambios: {e}")
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

    def edit_project(self, name: str, description: str):
        """Abre el modal de edición de un proyecto"""
        if self.close_cookie_btn.is_visible():
            self.close_cookie_warning()
            
        try:
            self.settings_link.wait_for(state="visible", timeout=10000)
            self.settings_link.click()
            
            # Limpiar y escribir el nombre
            self.edit_name_input.clear()
            self.edit_name_input.fill(name)

            # Limpiar y escribir la descripción
            self.edit_description_input.clear()
            self.edit_description_input.fill(description)


        except Exception as e:
            logger.error(f"No se pudo editar el proyecto: {e}")
            raise

    def set_privacy(self, privacy: str):
        """Define privacy: public, private o toggle."""
        try:
            if privacy == "public":
                expect(self.public_label).to_be_visible(timeout=5000)
                expect(self.public_label).to_be_enabled(timeout=5000)
                self.public_label.click()
                logger.info("Privacidad seleccionada: PUBLIC")
            elif privacy == "private":
                expect(self.private_label).to_be_visible(timeout=5000)
                expect(self.private_label).to_be_enabled(timeout=5000)
                self.private_label.click()
                logger.info("Privacidad seleccionada: PRIVATE")
            elif privacy == "toggle":
                for label in [self.public_label, self.private_label, self.public_label]:
                    expect(label).to_be_visible(timeout=5000)
                    expect(label).to_be_enabled(timeout=5000)
                    label.click()
                logger.info("Privacidad alternada (toggle realizado)")
            else:
                logger.error(f"Valor de privacidad inválido: {privacy}")
        except Exception as e:
            logger.error(f"Error al seleccionar privacidad: {e}")
            raise
    
    def success_notification(self) -> bool:
        """Devuelve True si el mensaje de éxito es visible."""
        try:
            # # Primero espera que aparezca (en caso de que no se haya renderizado aún)
            # expect(self.success_toast).to_be_visible(timeout=5000)
            # # Luego espera que desaparezca
            # expect(self.success_toast).not_to_be_visible(timeout=5000)
            return self.success_notification_msg.is_visible(timeout=3000)
            # return True
        except:
            return False
        
    def access_project_info(self):
        """Click en el icono del proyecto para ver su info"""
        try:
            self.project_info.click()
            logger.info("Click en el icono del proyecto para ver su info")
        except Exception as e:
            logger.error(f"No se pudo acceder a la info del proyecto: {e}")
            raise
    
    def is_project_private(self) -> bool:
        """
        Retorna True si el proyecto tiene el ícono de privado visible.
        """
        try:
            # Espera a que el ícono aparezca o desaparezca
            return self.private_icon.is_visible(timeout=5000)
        except:
            return False
        
    def get_required_field_errors_edit(self):
        """Devuelve una lista de todos los mensajes 'This value is required.' visibles en el formulario de edición."""
        errors = self.page.locator("li.checksley-required.required:has-text('This value is required.')")
        count = errors.count()

        messages = []
        for i in range(count):
            messages.append(errors.nth(i).inner_text().strip())

        return messages
    
    def change_privacy(self, privacy: str):
        """Define privacy: public, private o toggle."""
        self.open_settings()
        try:

            if privacy == "public":
                self.public_label.click()
                logger.info("Privacidad -> PUBLIC")

            elif privacy == "private":
                self.private_label.click()
                logger.info("Privacidad -> PRIVATE")

        except Exception as e:
            logger.error(f"Error cambiando privacidad: {e}")
            raise

