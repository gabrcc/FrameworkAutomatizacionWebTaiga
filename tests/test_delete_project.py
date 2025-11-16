from pages.projects_page import ProjectsPage
import pytest
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO

def test_delete_all_projects(projects_page, delete_all_projects):
    """
    Test para eliminar todos los proyectos visibles en el dashboard.
    Usa el fixture `delete_all_projects` para limpiar todos los proyectos.
    Luego verifica que no haya proyectos en el dashboard.
    """
    projects = projects_page
    projects.go_to_projects()
    delete_all_projects()
    remain_projects = projects.get_project_names()
    logger.info(f"Proyectos restantes: {len(remain_projects)} -> {remain_projects}")
    assert len(remain_projects) == 0
    assert projects.is_first_project_message_visible(), \
        "Aun quedan proyectos existentes(El mensaje 'Create your first project' no aparece)"
