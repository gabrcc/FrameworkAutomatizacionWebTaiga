import pytest
from pages.new_project_page import NewProjectPage
from pages.type_project_page import TypeProjectPage
from pages.timeline_project_page import TimeLineProjectPage
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO


@pytest.mark.functional
@pytest.mark.regression
def test_create_n_projects(projects_page, create_projects,n=7):
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
            assert project in displayed_projects, (f"El proyecto '{project}' no aparece en la lista de proyectos")
            logger.info(f"Proyecto '{project}' verificado correctamente la lista de proyectos")

        logger.info("Todos los proyectos creados aparecen correctamente en la lista de proyectos")

    except AssertionError as e:
        path = f"reports/screenshots/test_create_two_projects_fail.png"
        projects_page.page.screenshot(path=path)
        logger.error(f"Fallo en la verificación de proyectos: {e}")
        raise

@pytest.mark.parametrize("case_category", [
    "valid_cases",
    # "boundary_cases",
    # "invalid_cases",
    # "privacy_cases",
    # "special_cases"
])
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.prueba
def test_project_creation_cases(delete_project_by_name, projects_page,project_creation_cases, case_category, page):
    cases = project_creation_cases[case_category]
    projects = projects_page
    new_project = NewProjectPage(page)
    type_project = TypeProjectPage(page)
    timeline = TimeLineProjectPage(page)

    for case in cases:
        name = case["input"]["name"]
        description = case["input"]["description"]
        privacy = case["input"]["privacy"]
        expected = case["expected"]

        print(f"▶ Ejecutando {case['id']} - {case['title']}")

        # # Paso 1: New Project → seleccionar Kanban
        projects.go_to_projects()
        projects.click_new_project()
        type_project.select_kanban()

        # # Paso 2: llenar el formulario y enviar
        new_project.fill_form(name, description)
        new_project.set_privacy(privacy)
        new_project.submit_form()

        # Validar según lo esperado
        if expected == "success":
            timeline.go_to_projects()
            projects.wait_for_project(name)
            displayed = projects.get_project_names()
            try:
                assert name in displayed, f"FALLO: El Proyecto '{name}' no fue creado"
                logger.info(f"OK Proyecto creado: {name}")

                if privacy == "private":
                    try:
                        assert projects.is_project_private, f"No se encontro el icono de proyecto privado en '{name}'"
                        logger.info(f"Icono proyecto privado presente en {name}")
                    except AssertionError as e:
                        logger.error(str(e))
                        raise
                    

            except AssertionError as e:
                logger.error(str(e))
                raise

        elif expected == "error_required_field":
            error = new_project.get_error_message()
            try:
                assert error is not None, "FALLO: No apareció el error de campo requerido"
                logger.info("OK Error requerido detectado")
            except AssertionError as e:
                logger.error(str(e))
                raise

        elif expected == "error_max_length":
            error = new_project.get_error_message()
            try:
                assert "maximum" in error.lower(), "FALLO: No apareció error por longitud"
                logger.info("OK Error de longitud detectado")
            except AssertionError as e:
                logger.error(str(e))
                raise

        elif expected == "error_invalid_characters":
            error = new_project.get_error_message()
            try:
                assert "invalid" in error.lower(), "FALLO: No apareció error por caracteres inválidos"
                logger.info("OK Error por caracteres inválidos detectado")
            except AssertionError as e:
                logger.error(str(e))
                raise

        elif expected == "error_name_exists":
            error = new_project.get_error_message()
            try:
                assert "exists" in error.lower() or "ya existe" in error.lower(), "FALLO: No apareció error de nombre duplicado"
                logger.info("OK Error de nombre duplicado detectado")
            except AssertionError as e:
                logger.error(str(e))
                raise

        elif expected == "canceled_creation":
            new_project.cancel_creation()
            projects.go_to()
            displayed = projects.get_project_names()
            try:
                assert name not in displayed, "FALLO: El proyecto se creó aunque debía cancelarse"
                logger.info("OK Cancelación detectada correctamente")
            except AssertionError as e:
                logger.error(str(e))
                raise

        
        delete_project_by_name(name)

        