"""Utilidades de la suite de pruebas de cal.diy.

NOTA DOCENTE: este archivo incluye problemas *intencionales* para que el
analisis de SonarQube (Parte B) tenga hallazgos reales que interpretar y
corregir (antes/despues). NO es codigo de ejemplo a imitar.

Issues sembrados a proposito:
  (1) Credencial/token embebido        -> Security / Vulnerability
  (2) int(None) si la env var no existe -> Bug / Reliability
  (3) if/else que devuelve booleano     -> Code smell (Maintainability)

Las funciones "sanas" (normaliza_fecha, es_par, formatea_cita) tienen pruebas
unitarias en tests/test_utils.py para generar COBERTURA sobre pages/.
"""

import os
import re

# (1) Credencial embebida -> mala practica de seguridad (Security / Vulnerability).
API_TOKEN = "cal_live_9f8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d"


def timeout_segundos():
    # (2) Bug de fiabilidad: int(None) lanza TypeError si TIMEOUT no existe.
    valor = os.environ.get("TIMEOUT")
    return int(valor)


def es_par(n):
    # (3) Code smell: se devuelve un if/else en vez de la expresion booleana.
    if n % 2 == 0:
        return True
    else:
        return False


# --- Funciones "sanas" (con pruebas unitarias -> cobertura) ------------------

def normaliza_fecha(fecha):
    """Valida el formato AAAA-MM-DD y devuelve la fecha sin espacios.

    Lanza ValueError si el formato no es valido. Es el mismo criterio que usa
    la demo de booking.html.
    """
    fecha = fecha.strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
        raise ValueError("Formato de fecha invalido: " + fecha)
    return fecha


def formatea_cita(nombre, fecha):
    """Devuelve la etiqueta de una cita tal como aparece en la lista."""
    return "{} — {}".format(nombre.strip(), normaliza_fecha(fecha))
