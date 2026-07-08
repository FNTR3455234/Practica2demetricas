"""Pruebas data-driven del login inválido con @pytest.mark.parametrize.

Una sola función genera 4 pruebas en el reporte (una por fila): cubre casos de
ERROR (credenciales malas) y de FRONTERA (campos vacíos). Para agregar otro
caso basta con añadir una línea a la lista.
"""

import pytest

from pages.login_page import LoginPage


@pytest.mark.parametrize("email, password, mensaje", [
    ("admin@example.com", "malisima",  "Contrasena incorrecta"),      # error
    ("nadie@example.com", "Cal1234!",  "Usuario no existe"),          # error
    ("",                  "Cal1234!",  "El correo es obligatorio"),   # frontera
    ("admin@example.com", "",          "La contrasena es obligatoria"),  # frontera
])
def test_login_invalido(driver, base_url_login, email, password, mensaje):
    login = LoginPage(driver, base_url_login).abrir()
    login.iniciar_sesion(email, password)
    assert mensaje in login.texto_error()
