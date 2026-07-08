"""Pruebas unitarias de pages/utils.py.

No usan navegador: son rápidas y su objetivo es generar COBERTURA medible sobre
el módulo pages/utils.py, que luego SonarQube lee desde coverage.xml.
"""

import pytest

from pages.utils import es_par, normaliza_fecha, formatea_cita


@pytest.mark.parametrize("n, esperado", [
    (2, True),
    (4, True),
    (3, False),
    (0, True),
    (-1, False),
])
def test_es_par(n, esperado):
    assert es_par(n) is esperado


def test_normaliza_fecha_valida():
    assert normaliza_fecha("  2026-08-15 ") == "2026-08-15"


def test_normaliza_fecha_invalida():
    with pytest.raises(ValueError):
        normaliza_fecha("15/08/2026")


def test_formatea_cita():
    assert formatea_cita("  Ana  ", "2026-08-15") == "Ana — 2026-08-15"
