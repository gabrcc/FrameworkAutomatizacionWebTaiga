import json
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.base_page import BasePage
import time
import os
from dotenv import load_dotenv

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
    login_page.login(valid_user["email"], valid_user["password"])

    login_page.page.wait_for_url("https://tree.taiga.io/")
    yield login_page
