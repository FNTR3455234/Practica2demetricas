# Práctica 2 — QA del proyecto integrador: **cal.diy**

Aseguramiento de la calidad del repositorio de la Unidad 1
([`calcom/cal.diy`](https://github.com/calcom/cal.diy), plataforma de
agendamiento open-source) aplicando **Selenium (E2E)** y **SonarQube
(análisis estático + cobertura)**.

> **Enfoque.** cal.diy es una app muy extensa (Next.js + tRPC + Prisma + Postgres),
> inviable de levantar y probar E2E dentro del tiempo del examen. Por eso este
> proyecto **reproduce sus dos flujos reales — login y reserva de cita (booking) —
> en páginas HTML de demo locales y autocontenidas** (`app/`), sin servidor ni
> internet. La técnica (Page Objects, esperas explícitas, análisis estático,
> cobertura, quality gate) es idéntica a la que se aplicaría al repo real, y es la
> que evalúa la rúbrica.
>
> Además, para que **SonarQube analice código real del repositorio** (y no solo
> las pruebas), se incluye en `packages/lib/` un subconjunto de **módulos reales
> (acortados) de cal.diy en TypeScript**, respetando su ruta original. Así el
> análisis es multi-lenguaje (Python + TypeScript) sobre código del proyecto de
> la Unidad 1. Ver [`packages/lib/README.md`](packages/lib/README.md).

## Estructura

```
(raíz del repositorio)
  app/
    login.html              # demo: login de cal.diy (validación asíncrona)
    booking.html            # demo: reservar cita (validación asíncrona)
  pages/
    login_page.py           # Page Object #1 (login)
    booking_page.py         # Page Object #2 (booking)
    utils.py                # helpers con issues INTENCIONALES para SonarQube
  packages/lib/             # módulos REALES (acortados) de cal.diy en TypeScript
    slugify.ts  text.ts  random.ts  array.ts  notEmpty.ts
    getSafeRedirectUrl.ts  isOutOfBounds.ts   (código del repo a analizar)
  tests/
    conftest.py             # fixtures (driver, base_url_*) y hook de captura
    test_login.py           # login exitoso
    test_login_invalido.py  # data-driven @parametrize (4 casos)
    test_booking.py         # booking: válido + frontera + error (4 casos)
    test_utils.py           # unit tests de utils.py (cobertura)
  sonarqube/                # scripts para levantar y analizar con SonarQube
  sonar-project.properties  # config del scanner (con cobertura conectada)
  pytest.ini
  requirements.txt
  .github/workflows/pruebas.yml   # Bonus: CI en cada push
```

## Requisitos

- Python 3.10+
- Google Chrome (Selenium 4 descarga el driver solo con *Selenium Manager*).
- Docker Desktop (solo para la Parte B, SonarQube).

## Instalación

```powershell
# desde la raíz del repositorio
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
```

---

## Parte A — Selenium (35 pts)

### Ejecutar las pruebas

```powershell
pytest                 # todas (abre Chrome; 12 casos)
pytest -v              # con detalle
pytest tests/test_booking.py::test_reserva_valida
$env:HEADLESS = "1"; pytest    # sin ventana (Windows); Linux/Mac: HEADLESS=1 pytest
```

### Reporte HTML (suite en verde)

```powershell
pytest --html=reporte.html --self-contained-html
```
Abre `reporte.html` → captura con toda la suite en verde.

### Qué cubre (rúbrica)

| Requisito | Dónde |
|---|---|
| Estructura `pages/` + `tests/` + `conftest.py` con fixture del driver | `tests/conftest.py` (fixture `driver`) |
| ≥2 Page Objects con localizadores y métodos de negocio | `pages/login_page.py`, `pages/booking_page.py` |
| ≥5 pruebas (válidas, frontera, error) con `WebDriverWait`; **sin `time.sleep`** | `test_login*`, `test_booking` (12 casos con parametrize) |
| ≥1 prueba data-driven `@pytest.mark.parametrize` | `test_login_invalido.py`, `test_utils.py` |
| Reporte HTML (`pytest-html`) en verde | `reporte.html` |

Las esperas explícitas son necesarias porque las demos validan con un
`setTimeout` (~500–600 ms) que simula la llamada de red de cal.diy: `time.sleep`
sería *flaky*, `WebDriverWait` es estable.

---

## Parte B — SonarQube (40 pts)

### 1. Generar la cobertura (pytest-cov)

```powershell
pytest --cov=pages --cov-report=xml --html=reporte.html --self-contained-html
```
Genera `coverage.xml` (lo consume Sonar) → captura el **% de Coverage**.

### 2. Analizar con SonarQube

Sigue [`sonarqube/README.md`](sonarqube/README.md):

```powershell
./sonarqube/01_verificar.ps1
./sonarqube/02_levantar.ps1
# genera token en http://localhost:9000  (My Account → Security)
$env:SONAR_TOKEN = "sqp_tu_token"
./sonarqube/03_analizar.ps1
```
Tablero: `http://localhost:9000/dashboard?id=caldiy-pruebas`

### 3. Las 5 dimensiones (captura del tablero)

Reporta el rating de: **Reliability, Security, Maintainability, Coverage,
Duplications**.

### 4. Issues sembrados a propósito (analizar ≥3, corregir ≥2)

`pages/utils.py` incluye tres hallazgos reales para interpretar y corregir:

| # | Tipo | Dimensión | Descripción | Línea aprox. |
|---|---|---|---|---|
| 1 | Vulnerability | Security | Token embebido `API_TOKEN = "cal_live_..."` | ~19 |
| 2 | Bug | Reliability | `int(os.environ.get("TIMEOUT"))` → `TypeError` si no existe | ~24 |
| 3 | Code Smell | Maintainability | `if n%2==0: return True else return False` | ~29 |

**Correcciones sugeridas (antes/después) — corrige al menos 2:**

*Issue 1 — Security*
```python
# ANTES
API_TOKEN = "cal_live_9f8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d"
# DESPUÉS
API_TOKEN = os.environ.get("CAL_API_TOKEN", "")
```

*Issue 2 — Reliability*
```python
# ANTES
valor = os.environ.get("TIMEOUT")
return int(valor)
# DESPUÉS
return int(os.environ.get("TIMEOUT", "10"))
```

*Issue 3 — Maintainability*
```python
# ANTES
if n % 2 == 0:
    return True
else:
    return False
# DESPUÉS
return n % 2 == 0
```

Tras corregir, vuelve a correr `./sonarqube/03_analizar.ps1` y captura el
**antes/después** (los issues desaparecen y suben los ratings).

**Además, en el código real de cal.diy (`packages/lib/`) Sonar encontrará más
hallazgos reales** que puedes analizar/explicar (no es obligatorio corregirlos):

| Archivo | Hallazgo típico | Dimensión |
|---|---|---|
| `random.ts` | `Math.random()` para generar cadenas → aleatoriedad no segura | Security Hotspot |
| `getSafeRedirectUrl.ts` | reasignación del parámetro `url` | Maintainability |
| `text.ts` | número mágico `148` en `truncateOnWord` | Maintainability |
| `slugify.ts` | complejidad cognitiva alta / `@ts-ignore` | Maintainability |

Esto te da **muchos más de 3 issues** entre Python (`pages/utils.py`) y
TypeScript (`packages/lib/`), reforzando el criterio de análisis.

### 5. Quality Gate (Passed/Failed y por qué)

Usa el Quality Gate por defecto (**Sonar way**). En el tablero, la franja
superior indica **Passed** o **Failed**. Típicamente:
- **Failed** en el primer análisis → por *Security Hotspots/Vulnerabilities*
  abiertos y/o *Coverage on New Code* por debajo del umbral (80%).
- **Passed** tras corregir los issues y con la cobertura conectada.

Indica en el PDF cuál obtuviste y la causa concreta que muestra el gate.

---

## Parte C — Demostración y evidencias (25 pts)

### Demostración en vivo (15)
1. `pytest -v` en vivo → mostrar la suite en verde.
2. Navegar el tablero de SonarQube y **explicar un issue** (p. ej. el token
   embebido: por qué es una vulnerabilidad y cómo se corrige).

### Documento de evidencias (10)
PDF con **capturas numeradas**. Checklist sugerido:

1. Estructura de carpetas del proyecto.
2. `pytest -v` con los 12 casos en verde.
3. `reporte.html` (pytest-html) en verde.
4. Comando `pytest --cov` mostrando el % de Coverage.
5. Tablero de SonarQube (vista general).
6. Las 5 dimensiones con sus ratings.
7. Lista de issues (≥3) con tipo/severidad/regla/línea.
8. Antes/después de las 2 correcciones.
9. % de Coverage en el tablero.
10. Quality Gate (Passed/Failed) y su motivo.
11. (Bonus) Ejecución de GitHub Actions en verde.

### Aportes por integrante

| Integrante | Matrícula | Aportes |
|---|---|---|
| _Felipe Antonio Rodríguez Díaz_ | _up240423_ | _Desarrollo del código junto con el repo._ |
| _Ángel Germán Correa Benítez_ | _up240077_ | _Documento y corregir issues._ |
| _Samuel Guadalupe Reyes García_ | _up240516_ | _Correr los comandos y hacer el video._ |
| _Erick Luna Espinosa_ | _up240801_ | _Hacer el video y tomar las capturas de pantalla._ |

### Breve análisis de la deuda técnica
_(2–3 líneas: qué issues encontró Sonar, cuáles se corrigieron, qué deuda
queda y su impacto en mantenibilidad/seguridad.)_

---

## Bonus (+5) — CI con GitHub Actions

[`.github/workflows/pruebas.yml`](.github/workflows/pruebas.yml) corre la suite
(headless) y sube `reporte.html` + `coverage.xml` como artefactos **en cada
push**. Captura una ejecución en verde desde la pestaña **Actions**.

---

## Credenciales de la demo

- **Login** — usuario válido: `admin@example.com` · contraseña válida: `Cal1234!`
- **Booking** — nombre + fecha `AAAA-MM-DD` (debe ser `>= 2026-01-01`).

Cualquier otra combinación dispara los mensajes de error que verifican las
pruebas de frontera y de error.
