"""Prueba E2E del login exitoso de cal.diy usando el Page Object."""

from pages.login_page import LoginPage


def test_login_exitoso(driver, base_url_login):
    login = LoginPage(driver, base_url_login).abrir()
    login.iniciar_sesion("admin@example.com", "Cal1234!")
    assert "Bienvenido" in login.texto_saludo()
