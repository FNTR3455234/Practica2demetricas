# Practica 2 - Verificacion de prerrequisitos para SonarQube
# Uso:  ./sonarqube/01_verificar.ps1

Write-Host "== Verificacion de prerrequisitos (SonarQube) ==" -ForegroundColor Yellow

# 1. Docker instalado
$dockerVersion = (& docker --version 2>$null)
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK ] $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "[X  ] Docker no encontrado. Instala Docker Desktop." -ForegroundColor Red
}

# 2. Daemon de Docker corriendo
& docker info > $null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK ] Docker daemon activo" -ForegroundColor Green
} else {
    Write-Host "[X  ] Docker no esta corriendo. Abre Docker Desktop (icono verde)." -ForegroundColor Red
}

# 3. Puerto 9000 libre
$en9000 = Get-NetTCPConnection -LocalPort 9000 -State Listen -ErrorAction SilentlyContinue
if ($en9000) {
    Write-Host "[!  ] Puerto 9000 EN USO (PID $($en9000.OwningProcess)). Cierra ese proceso." -ForegroundColor Red
} else {
    Write-Host "[OK ] Puerto 9000 libre" -ForegroundColor Green
}

# 4. Python disponible
$py = (& python --version 2>&1)
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK ] $py" -ForegroundColor Green
} else {
    Write-Host "[!  ] Python no encontrado (no es bloqueante para levantar Sonar)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Si todo esta en [OK], continua con:  ./sonarqube/02_levantar.ps1" -ForegroundColor Cyan
exit 0
