import json
import time
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.projects_page import ProjectsPage
from pages.new_project_page import NewProjectPage
from pages.type_project_page import TypeProjectPage
from pages.timeline_project_page import TimeLineProjectPage
import time
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Cambia a True para No ver navegador
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)

@pytest.fixture(scope="session")
def credentials():
    """Lee las credenciales del JSON una sola vez."""
    with open("data/login_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture()
def log_in_success(base_url, login_page, credentials):
    """Inicia sesión con la cuenta válida (primera del JSON)."""
    valid_user = credentials["valid_credentials"][0]
    login_page.navigate(base_url)
    login_page.open_login()
    login_page.login(valid_user["username/email"], valid_user["password"])

    login_page.page.wait_for_url("https://tree.taiga.io/")
    yield login_page

@pytest.fixture()
def dashboard_page(log_in_success):
    """Devuelve la página de dashboard con sesión iniciada."""
    return DashboardPage(log_in_success.page)

@pytest.fixture()
def projects_page(log_in_success):
    """Devuelve la página de Projects con sesión iniciada."""
    return ProjectsPage(log_in_success.page)

@pytest.fixture
def create_projects(projects_page,page):
    """
    Fixture para crear N proyectos desde Projects.
    Usa los Page Objects ya instanciados en projects_page.
    """
    def _create_projects(n=1):
        logger.info(f"Creando {n} proyectos desde el Projects...")

        projects = projects_page
        new_project = NewProjectPage(page)
        type_project = TypeProjectPage(page)
        timeline_project = TimeLineProjectPage(page)


        created_projects = []

        for i in range(n):
            project_name = f"TestProject_{i+1}"
            project_description = f"Descripción del proyecto {i+1}"
            logger.info(f"Creando proyecto {i+1}: {project_name}")

            # Paso 1: New Project → seleccionar Kanban
            projects.go_to_projects()
            projects.click_new_project()
            type_project.select_kanban()

            # Paso 2: llenar el formulario y enviar
            new_project.fill_form(name=project_name, description=project_description)
            new_project.submit_form()
            timeline_project.go_to_projects()
            projects.wait_for_project(project_name)

            logger.info(f"Proyecto '{project_name}' creado correctamente")
            created_projects.append(project_name)


        logger.info(f"Todos los proyectos creados: {created_projects}")
        return created_projects


    return _create_projects


# @pytest.fixture
# def delete_all_projects(dashboard_page, page):
#     """
#     Fixture que devuelve una función para eliminar todos los proyectos visibles.
#     """
#     timeline = TimeLineProjectPage(page)
#     projects = ProjectsPage(page)

#     def _delete_all():
#         # dashboard_page.go_to_projects()
#         project_names = projects.get_project_names()

#         for name in project_names:
#             project_names = projects.get_project_names()
#             projects.click_project(name)  
#             timeline.delete_project(name)  
#             timeline.confirm_delete()
#             dashboard_page.go_to_projects()
#             projects.click_view_all_projects()

#         time.sleep(3)
#         projects.first_proyect_option()
#         logger.info("Se eliminaron todos los proyectos")

#     return _delete_all
