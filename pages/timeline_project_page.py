from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


class TimeLineProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.projects_button = "a.dropdown-project-list-projects[title='Projects']"
        self.view_all_projects_option = 'a.see-more-projects-btn[tg-nav="projects"]' 

    def go_to_projects(self):
        self.click(self.projects_button)
        self.click(self.view_all_projects_option)

