import json
import pytest
from utils.helpers import screenshot_path
from utils.logger import setup_logger

logger = setup_logger("test_login", log_file="test_login.log")


# Cargar credenciales
with open("data/login_data.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)
invalid_creds = credentials["invalid_credentials"]
valid_creds = credentials["valid_credentials"]


@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("cred", valid_creds)
def test_login_valid_credentials(login_page, cred, base_url):
    login_page.navigate(base_url)
    login_page.open_login()
    login_page.login(cred["username/email"], cred["password"])
    login_page.page.wait_for_url("https://tree.taiga.io/")
    
    try:
        assert not login_page.login_is_displayed()
        assert "Home - Taiga" in login_page.page.title()
        logger.info(f"Log in con credenciales validas exitoso")
    
    except AssertionError:
        path = screenshot_path(f"login_valid_{cred['description']}")
        login_page.page.screenshot(path=path)
        logger.error(f"Fallo en log in con credenciales validas ")
        raise


# Parametrizar con todos los casos invalid_credentials
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("cred", invalid_creds)
def test_login_invalid_credentials(login_page, cred, base_url):
    login_page.navigate(base_url)
    login_page.open_login()
    login_page.login(cred["username/email"], cred["password"])

    try:
        assert login_page.view_error_message(), f"Error no mostrado para {cred['description']}, \n user/email: {cred['username']}\n password: {cred['password']}"
    except AssertionError:
        path = screenshot_path(f"login_invalid_{cred['description']}")
        login_page.page.screenshot(path=path)
        raise

# Test Login edge cases (campos vacíos)
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize("user", ["edge_cases"])
def test_login_edge_cases(login_page, credentials, user, base_url):
    for cred in credentials[user]:
        login_page.navigate(base_url)
        login_page.open_login()
        login_page.login(cred["username/email"], cred["password"])

        # Verifica que los campos y botón sigan visibles
        try:
            assert login_page.page.locator(login_page.username_input).is_visible()
            assert login_page.page.locator(login_page.password_input).is_visible()
            assert login_page.page.locator(login_page.login_button).is_visible()

            # Validación nativa HTML (campos requeridos)
            username_invalid = login_page.page.locator(login_page.username_input).evaluate("el => !el.checkValidity()")
            password_invalid = login_page.page.locator(login_page.password_input).evaluate("el => !el.checkValidity()")
            assert username_invalid or password_invalid, "Los campos vacíos deberían ser inválidos"

        except AssertionError:
            path = screenshot_path(f"login_edge_{cred['description'].replace(' ', '_')}")
            login_page.page.screenshot(path=path)
            raise
