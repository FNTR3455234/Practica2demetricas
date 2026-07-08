"""Page Object de la pantalla de login de cal.diy.

Concentra los localizadores y las acciones de la pantalla de login en un solo
lugar. Las pruebas solo llaman métodos con nombre de negocio (iniciar_sesion,
texto_saludo, ...) y no conocen los `id` del HTML.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # Localizadores: atributos de clase, viven en un solo sitio.
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    BOTON = (By.ID, "btn-login")
    SALUDO = (By.ID, "saludo")
    ERROR = (By.ID, "error")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.url)
        return self

    def iniciar_sesion(self, email, password):
        campo_email = self.driver.find_element(*self.EMAIL)
        campo_email.clear()
        campo_email.send_keys(email)

        campo_password = self.driver.find_element(*self.PASSWORD)
        campo_password.clear()
        campo_password.send_keys(password)

        # Espera explícita: hasta que el botón sea clicable, luego clic.
        self.wait.until(EC.element_to_be_clickable(self.BOTON)).click()

    def texto_saludo(self):
        # Espera a que el saludo sea visible (aparece tras el retardo AJAX).
        return self.wait.until(
            EC.visibility_of_element_located(self.SALUDO)).text

    def texto_error(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR)).text
