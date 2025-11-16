from playwright.sync_api import expect
from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_title = "div.home-wrapper h1"
        self.working_on_empty = "div.working-on-empty p"
        self.watching_empty = "div.watching-empty p"
        self.no_projects_message = "section.projects-empty p"
        self.projects_list = "div.home-project.tg-scope"
        self.project_name = "div.home-project.tg-scope h3.project-card-name a.project-title"
        self.project_description = "div.home-project.tg-scope p.project-card-description"
        self.manage_projects_button = "a.see-more-projects-btn[title='Manage projects']"
        self.new_project_button = "a.create-project-button"
        self.projects_button = "a.dropdown-project-list-projects[title='Projects']"
        self.view_all_projects_option = page.locator('a.see-more-projects-btn[tg-nav="projects"]') #'a.see-more-projects-btn[title="View all projects"]'

         
    def get_dashboard_title(self):
        return self.get_text(self.dashboard_title)

    def get_working_on_message(self):
        return self.get_text(self.working_on_empty)

    def get_watching_message(self):
        return self.get_text(self.watching_empty)

    def get_no_projects_message(self, timeout=5000):
        """Devuelve el mensaje cuando no hay proyectos. Espera hasta que el mensaje sea visible."""
        locator = self.page.locator(self.no_projects_message)
        try:
            expect(locator).to_be_visible(timeout=timeout)
            return locator.inner_text()
        except TimeoutError:
            # El mensaje no apareció en el tiempo esperado
            return None

    def wait_for_projects_or_no_message(self, timeout=10000):
        """
        Espera a que haya al menos un proyecto visible o que aparezca
        el mensaje 'no projects'.
        """
        try:
            # Espera a que al menos un proyecto sea visible
            self.page.wait_for_selector(self.projects_list, state="visible", timeout=timeout)
        except TimeoutError:
            # Si no hay proyectos visibles, espera el mensaje de "no projects"
            try:
                self.page.wait_for_selector(self.no_projects_message, state="visible", timeout=timeout)
            except TimeoutError:
                logger.warning("Ni proyectos ni mensaje de 'no projects' aparecieron en el dashboard")
    

    def click_manage_projects(self):
        self.click(self.manage_projects_button)

    def is_new_project_visible(self):
        """Verifica si el botón 'New project' está visible"""
        return self.page.locator(self.new_project_button).is_visible()
    
    def click_new_project(self):
        self.click(self.new_project_button)

    def wait_for_project(self, project_name: str, timeout: int = 10000):
        """Espera hasta que un proyecto con nombre project_name aparezca en el dashboard"""
        try:
            locator = self.page.locator(f"{self.project_name}:has-text('{project_name}')")
            expect(locator).to_be_visible(timeout=timeout)
            logger.info(f"Proyecto '{project_name}' visible en el dashboard")
        except Exception as e:
            logger.error(f"El proyecto '{project_name}' no apareció en el dashboard: {e}")
            raise

    def project_count(self):
        """Devuelve la cantidad de proyectos visibles"""
        locator = self.page.locator(self.project_name)
        count = locator.count()
        logger.info(f"Cantidad de proyectos: {count}")
        return count
    
    def is_new_project_visible(self):
        """Verifica si el botón 'New project' está visible"""
        return self.page.locator(self.new_project_button).is_visible()
    
    def is_manage_projects_visible(self):
        """Verifica si el botón 'Manage projects' está visible"""
        return self.page.locator(self.manage_projects_button).is_visible()