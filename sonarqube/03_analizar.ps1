# Practica 2 - Ejecutar el analisis del proyecto con el SonarScanner (Windows/Mac)
# Uso:
#   $env:SONAR_TOKEN = "sqp_tu_token"
#   ./sonarqube/03_analizar.ps1

param(
    [string]$Token = $env:SONAR_TOKEN
)

if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "[X] Falta el token. Genera uno en el tablero (My Account > Security)" -ForegroundColor Red
    Write-Host '    y define:  $env:SONAR_TOKEN = "sqp_tu_token"' -ForegroundColor Red
    exit 1
}

# Correr el scanner desde la RAIZ del proyecto (carpeta padre de este script)
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz
Write-Host "== Analizando $raiz ==" -ForegroundColor Yellow

# En Windows/Mac el contenedor alcanza el host por host.docker.internal
& docker run --rm -v "${raiz}:/usr/src" `
    -e SONAR_HOST_URL=http://host.docker.internal:9000 `
    -e SONAR_TOKEN=$Token `
    sonarsource/sonar-scanner-cli

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Analisis enviado. Abre el tablero:" -ForegroundColor Green
    Write-Host "     http://localhost:9000/dashboard?id=caldiy-pruebas" -ForegroundColor Green
} else {
    Write-Host "[X] El scanner fallo. Revisa el token y que el servidor este arriba." -ForegroundColor Red
}
