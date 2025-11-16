from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger
from playwright.sync_api import expect
import time


logger = setup_logger("test_dashboard.log", level=20)  # INFO

class ProjectsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.new_project_button = page.locator("a.create-project-btn[title='New project']")
        self.project_image_link = "a.list-itemtype-project-image"
        self.project_card = page.locator("li.list-itemtype-project")
        self.project_title_link = page.locator("a.project-title")
        self.project_description = page.locator("div.home-project.tg-scope p.project-card-description")
        self.project_list_locator = page.locator("li.list-itemtype-project")  # Cada proyecto
        self.project_list_container = page.locator("div.project-list")     # Contenedor scrollable
        self.create_your_first_project = page.locator("div[ng-if='!vm.projects.size'] h2:text('Create your first project')")
        self.view_all_projects_option = page.locator('a.see-more-projects-btn[tg-nav="projects"]') #'a.see-more-projects-btn[title="View all projects"]'

    def go_to_projects(self):
        self.navigate("https://tree.taiga.io/projects/")
        self.page.wait_for_load_state("networkidle")

    def click_new_project(self):
        """Hace clic en el botón 'New project'"""
        try:
            self.new_project_button.nth(1).click()
            logger.info("Se hizo clic en 'New project'")
        except Exception as e:
            logger.error(f"No se pudo hacer clic en 'New project': {e}")
            raise
            
    def get_project_names(self):
        """Lista de nombres de proyectos"""
        logger.info(f"   Proyectos:{self.project_title_link.all_inner_texts()}")
        return self.project_title_link.all_inner_texts()
    
    def wait_for_project(self, project_name: str, timeout: int = 10000):
        """Espera hasta que un proyecto con nombre project_name aparezca"""
        try:
            # locator = self.page.locator(f"{self.project_title_link}:has-text('{project_name}')")
            locator = self.project_title_link.locator(f"text={project_name}").first
            expect(locator).to_be_visible(timeout=timeout)
            logger.info(f"Proyecto '{project_name}' visible")
        except Exception as e:
            logger.error(f"El proyecto '{project_name}' no apareció: {e}")
            raise
