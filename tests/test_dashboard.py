import pytest
from utils.helpers import screenshot_path
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO

@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
def test_dashboard_title(dashboard_page):
    """Verifica que el dashboard se cargue y tenga el título correcto"""
    try:
        title = dashboard_page.get_dashboard_title()
        assert "Projects Dashboard" in title
        logger.info("Dashboard cargado correctamente con título correcto")
    except AssertionError:
        path = screenshot_path("dashboard_title_fail")
        dashboard_page.page.screenshot(path=path)
        logger.error("Fallo al cargar título del dashboard")
        raise

@pytest.mark.functional
@pytest.mark.regression
def test_working_on_message(dashboard_page):
    """Verifica el mensaje 'Working on' cuando no hay tareas"""
    try:
        msg = dashboard_page.get_working_on_message()
        assert "It feels empty" in msg
        logger.info("Mensaje 'Working on' correcto")
    except AssertionError:
        path = screenshot_path("dashboard_working_on_fail")
        dashboard_page.page.screenshot(path=path)
        logger.error("Fallo en mensaje 'Working on'")
        raise

@pytest.mark.functional
@pytest.mark.regression
def test_project_list(dashboard_page):
    """Verifica que haya proyectos o muestra el mensaje de lista vacía"""
    dashboard_page.wait_for_projects_or_no_message(timeout=5000)
    count = dashboard_page.project_count()
    
    if count > 0:
        assert count > 0
        print("Proyectos listados correctamente")
    else:
        msg = dashboard_page.get_no_projects_message()
        assert msg == "You don't have any project yet"
        print("Mensaje de lista vacía mostrado correctamente")

@pytest.mark.functional
@pytest.mark.regression
def test_project_action_button(dashboard_page):
    """
    Verifica que:
    - Si no hay proyectos, se muestre el botón 'New project'.
    - Si hay uno o más proyectos, se muestre 'Manage projects'.
    """
    try:
        dashboard_page.wait_for_projects_or_no_message(timeout=5000)
        count = dashboard_page.project_count()
        logger.info(f"Cantidad de proyectos detectados: {count}")

        if count == 0:
            assert dashboard_page.is_new_project_visible(), "El botón 'New project' no está visible cuando no hay proyectos."
            logger.info("Botón 'New project' visible correctamente cuando no hay proyectos.")
        else:
            assert dashboard_page.is_manage_projects_visible(), "El botón 'Manage projects' no está visible cuando hay proyectos."
            logger.info(f"Botón 'Manage projects' visible correctamente (se encontraron {count} proyecto/s).")

    except AssertionError as e:
        path = screenshot_path("project_action_button_fail")
        dashboard_page.page.screenshot(path=path)
        logger.error(f"Falla en verificación del botón de acción de proyectos: {e}")
        raise