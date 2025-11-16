import pytest
from pages.projects_page import ProjectsPage
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


@pytest.mark.functional
@pytest.mark.regression
def test_create_n_projects(projects_page, create_projects,n=3):
    """
    Test para crear N proyectos usando el fixture `create_projects`
    y verificar que aparecen en la lista del Dashboard.
    """
    
    try:
        # Crear N proyectos
        project_names = create_projects(n)

        projects = projects_page
        # Obtener los nombres de los proyectos 
        
        displayed_projects = projects.get_project_names()
        logger.info(f"Proyectos: {displayed_projects}")

        # Verificar que todos los proyectos creados estén en la lista
        for project in project_names:
            assert project in displayed_projects, f"El proyecto '{project}' no aparece en la lista de proyectos"
            logger.info(f"Proyecto '{project}' verificado correctamente la lista de proyectos")

        logger.info("Todos los proyectos creados aparecen correctamente en la lista de proyectos")

    except AssertionError as e:
        path = f"reports/screenshots/test_create_two_projects_fail.png"
        projects_page.page.screenshot(path=path)
        logger.error(f"Fallo en la verificación de proyectos: {e}")
        raise
