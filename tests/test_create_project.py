import pytest
import time
import json
from utils.helpers import screenshot_path
from pages.new_project_page import NewProjectPage
from pages.type_project_page import TypeProjectPage
from pages.timeline_project_page import TimeLineProjectPage
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)  # INFO

# Cargar credenciales
with open("data/tc_create_project.json", "r", encoding="utf-8") as f:
    create_project_cases = json.load(f)


## Aplanar los casos y agregar IDs
flattened_cases = []
for category, cases in create_project_cases.items():
    for case in cases:
        flattened_cases.append(
            pytest.param(category, case, id=f"{category}-{case['id']}")
        )


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


@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.parametrize("category, case", flattened_cases)
def test_project_creation_cases(delete_project_by_name, projects_page, page, create_one_project, category, case):
    projects = projects_page
    new_project = NewProjectPage(page)
    type_project = TypeProjectPage(page)
    timeline = TimeLineProjectPage(page)

    name = case["input"]["name"]
    description = case["input"]["description"]
    privacy = case["input"]["privacy"]
    expected = case["expected"]

    print(f"Ejecutando {case['id']} - {case['title']}")

    # Marcar ciertos casos como xfail
    # if expected in ["error_name_exists", "error_invalid_characters"]:
    #     pytest.xfail(f"Se espera fallo: {case['id']} - {case['title']}")
    is_xfail = expected in ["error_name_exists", "error_invalid_characters"]


    # Paso 1: New Project → seleccionar Kanban
    projects.go_to_projects()
    projects.click_new_project()
    type_project.select_kanban()

    # Paso 2: llenar el formulario y enviar
    new_project.fill_form(name, description)
    new_project.set_privacy(privacy)
    new_project.submit_form()

    try:
        # Validación según lo esperado
        if expected == "success":
            timeline.go_to_projects()
            projects.wait_for_project(name)
            displayed = projects.get_project_names()
            assert name in displayed, f"FALLO: El Proyecto '{name}' no fue creado"
            logger.info(f"OK Proyecto creado: {name}")

            if privacy == "private":
                assert projects.is_project_private, f"No se encontró el icono de proyecto privado en '{name}'"
                logger.info(f"Icono proyecto privado presente en {name}")

        elif expected == "error_required_field":
            required_field_errors = new_project.get_required_field_errors()
            assert required_field_errors is not None, "FALLO: No apareció el error de campo requerido"
            logger.info("OK Error valor requerido detectado")

        elif expected == "error_max_length":
            lock_submit = new_project.submit_load_state()
            assert lock_submit, "FALLO: Se creó el proyecto a pesar del límite de caracteres"
            logger.info("OK Proyecto no creado, problema de longitud detectado")

        elif expected == "error_invalid_characters":
            timeline.go_to_projects()
            displayed = projects.get_project_names()
            assert name not in displayed, "FALLO: Se creó proyecto a pesar de tener solo caracteres inválidos"
            logger.info("OK Proyecto no creado, caracteres inválidos detectado")

        elif expected == "error_name_exists":
            # Crear proyecto duplicado usando fixture
            time.sleep(1)
            project_to_duplicate = create_one_project(name, description)
            timeline.go_to_projects()
            displayed = projects.get_project_names()
            project_count = displayed.count(name)
            assert project_count == 1, "FALLO: Se creó proyecto duplicado"
            logger.info("OK Proyecto no creado, nombre duplicado detectado")
            delete_project_by_name(project_to_duplicate)

    except AssertionError as e:
        page.wait_for_timeout(2000)
        path = screenshot_path(f"{case['id']}_creacion_proyecto")
        projects.page.screenshot(path=path)
        logger.error(str(e))
        # Si era XFAIL, lo marcamos aquí
        if is_xfail:
            pytest.xfail(f"Se esperaba fallo: {case['id']} - {case['title']}")
        else:
            raise


    finally:
        # Eliminar proyecto creado si existe
        delete_project_by_name(name)

