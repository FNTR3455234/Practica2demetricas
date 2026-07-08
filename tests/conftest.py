"""Fixtures y hooks compartidos por todas las pruebas (pytest).

- `driver`: abre y cierra Chrome (con yield = preparación / limpieza).
- `base_url_login` / `base_url_booking`: URLs file:// de las páginas de demo.
- Hook de captura: guarda un PNG cuando una prueba falla.

Modo headless (sin ventana, útil en CI):  HEADLESS=1 pytest
"""

import os
import pathlib

import pytest
from selenium import webdriver


def _demo_uri(nombre_html):
    # Ruta a una página de demo, convertida a URL file:// (multiplataforma).
    pagina = pathlib.Path(__file__).resolve().parents[1] / "app" / nombre_html
    return pagina.as_uri()


@pytest.fixture
def base_url_login():
    return _demo_uri("login.html")


@pytest.fixture
def base_url_booking():
    return _demo_uri("booking.html")


@pytest.fixture
def driver():
    opciones = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS"):
        opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1920,1080")

    d = webdriver.Chrome(options=opciones)  # Selenium Manager baja el driver
    d.implicitly_wait(5)
    yield d          # aquí se ejecuta la prueba
    d.quit()         # se ejecuta al terminar, siempre


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda una captura de pantalla cuando una prueba falla."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            driver.save_screenshot(f"fallo_{item.name}.png")
