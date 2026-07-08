# Practica 2 - Levantar el servidor SonarQube y esperar a que responda
# Uso:  ./sonarqube/02_levantar.ps1

Write-Host "== Levantando SonarQube Community ==" -ForegroundColor Yellow

# Si ya existe el contenedor, reusarlo
$existe = (& docker ps -a --filter "name=sonarqube" --format "{{.Names}}" 2>$null)
if ($existe -eq "sonarqube") {
    Write-Host "El contenedor 'sonarqube' ya existe. Arrancandolo..." -ForegroundColor Cyan
    & docker start sonarqube | Out-Null
} else {
    & docker run -d --name sonarqube -p 9000:9000 sonarqube:community | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[X] No se pudo crear el contenedor. Revisa Docker." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Esperando a que el tablero responda en http://localhost:9000 ..." -ForegroundColor Cyan
Write-Host "(la primera vez puede tardar 1-2 minutos)"

$listo = $false
for ($i = 1; $i -le 60; $i++) {
    Start-Sleep -Seconds 5
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:9000/api/system/status" -UseBasicParsing -TimeoutSec 5
        if ($r.Content -match '"status"\s*:\s*"UP"') { $listo = $true; break }
    } catch { }
    Write-Host ("  ... intento {0}/60" -f $i)
}

if ($listo) {
    Write-Host ""
    Write-Host "[OK] SonarQube esta ARRIBA: http://localhost:9000" -ForegroundColor Green
    Write-Host "     Usuario: admin   Contrasena: admin  (te pedira cambiarla)" -ForegroundColor Green
    Write-Host "     Luego genera un token y continua con  ./sonarqube/03_analizar.ps1" -ForegroundColor Cyan
} else {
    Write-Host "[!] No respondio aun. Revisa:  docker logs sonarqube  (suele ser falta de RAM)." -ForegroundColor Red
}
