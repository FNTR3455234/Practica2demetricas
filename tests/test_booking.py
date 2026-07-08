"""Pruebas E2E del flujo de reserva (booking) de cal.diy.

Cubre un caso VÁLIDO, uno de ERROR de negocio (fecha en el pasado), uno de
FRONTERA (fecha vacía) y uno de ERROR de validación (formato inválido). Todas
usan esperas explícitas a través del Page Object; no hay time.sleep.
"""

from pages.booking_page import BookingPage


def test_reserva_valida(driver, base_url_booking):
    booking = BookingPage(driver, base_url_booking).abrir()
    booking.reservar("Ana López", "2026-08-15")
    assert "Cita reservada para 2026-08-15" in booking.texto_mensaje()
    assert booking.cantidad_citas() == 1


def test_reserva_fecha_pasada(driver, base_url_booking):
    booking = BookingPage(driver, base_url_booking).abrir()
    booking.reservar("Ana López", "2020-01-01")
    assert "pasado" in booking.texto_error()
    assert booking.cantidad_citas() == 0


def test_reserva_sin_fecha(driver, base_url_booking):
    booking = BookingPage(driver, base_url_booking).abrir()
    booking.reservar("Ana López", "")
    assert "La fecha es obligatoria" in booking.texto_error()


def test_reserva_formato_invalido(driver, base_url_booking):
    booking = BookingPage(driver, base_url_booking).abrir()
    booking.reservar("Ana López", "15/08/2026")
    assert "Formato de fecha invalido" in booking.texto_error()
