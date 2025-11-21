import pytest
import json
import time
from utils.helpers import screenshot_path
from pages.new_project_page import NewProjectPage
from pages.type_project_page import TypeProjectPage
from pages.timeline_project_page import TimeLineProjectPage
from utils.logger import setup_logger

logger = setup_logger("test_dashboard.log", level=20)

# Cargar JSON
with open("data/tc_edit_project.json", "r", encoding="utf-8") as f:
    edit_project_cases = json.load(f)

# Aplanar los casos y agregar IDs
flattened_cases = []
for category, cases in edit_project_cases.items():
    for case in cases:
        flattened_cases.append(
            pytest.param(category, case, id=f"{category}-{case['id']}")
        )

@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.parametrize("category, case", flattened_cases)
def test_edit_project_cases(projects_page, page, create_one_project, category, case, delete_project_by_name):
    projects = projects_page
    timeline = TimeLineProjectPage(page)

    # Crear proyecto base para editar
    base_name = f"Base-{case['id']}"
    create_one_project(base_name, "Descripción inicial")

    # Datos de edición
    new_name = case["input"]["name"]
    new_description = case["input"]["description"]
    privacy = case["input"]["privacy"]
    expected = case["expected"]

    accepted_changes = False
    is_xfail = expected in ["error_invalid_characters"]

    try:
        # Ir al proyecto y abrir edición
        timeline.go_to_projects()
        projects.click_project(base_name)
        time.sleep(1)
        timeline.edit_project(new_name,new_description)  # método que abre el modal de edición

        # Llenar formulario de edición
        # timeline.set_privacy(privacy)
        timeline.save_changes()
        time.sleep(1)

        accepted_changes = timeline.success_notification()

        if expected == "success":
            assert accepted_changes, f"FALLO: El proyecto '{case['id']}' no fue actualizado"
            logger.info(f"OK Proyecto editado correctamente: {base_name} -> {new_name}")
            
        elif expected == "error_required_field":
            errors = timeline.get_required_field_errors_edit()
            assert errors is not None, "FALLO: No se mostró error de campo requerido"
            logger.info(f"OK Required fields error detectado")
        
        elif expected == "error_invalid_characters":
            assert not accepted_changes, f"FALLO: Proyecto editado con caracteres inválidos -> {new_name}"
            logger.info(f"OK Proyecto no editado por caracteres invalidos: {new_name}")
            
    except AssertionError as e:
        if expected == "error_invalid_characters" and accepted_changes:
            path = screenshot_path(f"{case['id']}_edit_project")
            page.screenshot(path=path)
            logger.error(str(e))
            # Si era XFAIL, lo marcamos aquí
            if is_xfail:
                pytest.xfail(f"Se esperaba fallo: {case['id']} - {case['title']}")
            else:
                raise
        else:
            raise
    finally:
        delete_project_by_name(base_name)
        delete_project_by_name(new_name)

@pytest.mark.functional
@pytest.mark.regression
def test_change_privacy(delete_project_by_name, projects_page, create_one_project):
    timeline = TimeLineProjectPage(projects_page.page)
    
    project_name = "Privacy test"
    create_one_project(project_name, "Descripción inicial")
    projects = projects_page
    try:
        #ESCENARIO PUBLIC -> PRIVATE
        timeline.change_privacy("private")
        timeline.save_changes()
        time.sleep(1)
        assert timeline.success_notification()
        timeline.go_to_projects()
        projects.is_project_private(project_name)

        # #ESCENARIO PRIVATE -> PUBLIC
        projects.click_project(project_name)
        timeline.change_privacy("public")
        timeline.save_changes()
        time.sleep(1)
        assert timeline.success_notification()
        timeline.go_to_projects()
        assert not projects.is_project_private(project_name)

    finally:
        delete_project_by_name(project_name)


