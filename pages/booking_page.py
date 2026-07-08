"""Page Object de la pantalla de reserva (booking) de cal.diy.

Mismo patrón que LoginPage: localizadores como atributos de clase y acciones
con nombre de negocio (reservar, texto_mensaje, ...).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingPage:
    TITULO = (By.ID, "titulo-booking")
    NOMBRE = (By.ID, "nombre")
    FECHA = (By.ID, "fecha")
    BTN_RESERVAR = (By.ID, "btn-reservar")
    MENSAJE = (By.ID, "mensaje")
    ERROR = (By.ID, "error")
    LISTA = (By.CSS_SELECTOR, "#lista-citas li")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.url)
        return self

    def titulo(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TITULO)).text

    def reservar(self, nombre, fecha):
        campo_nombre = self.driver.find_element(*self.NOMBRE)
        campo_nombre.clear()
        campo_nombre.send_keys(nombre)

        campo_fecha = self.driver.find_element(*self.FECHA)
        campo_fecha.clear()
        campo_fecha.send_keys(fecha)

        # Espera explícita: hasta que el botón sea clicable, luego clic.
        self.wait.until(EC.element_to_be_clickable(self.BTN_RESERVAR)).click()

    def texto_mensaje(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MENSAJE)).text

    def texto_error(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR)).text

    def cantidad_citas(self):
        return len(self.driver.find_elements(*self.LISTA))
