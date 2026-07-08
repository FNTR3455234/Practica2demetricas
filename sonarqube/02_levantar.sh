#!/usr/bin/env bash
# Practica 2 - Levantar el servidor SonarQube y esperar a que responda (Linux/Mac)
echo "== Levantando SonarQube Community =="

if [ "$(docker ps -a --filter name=sonarqube --format '{{.Names}}')" = "sonarqube" ]; then
  echo "El contenedor 'sonarqube' ya existe. Arrancandolo..."
  docker start sonarqube >/dev/null
else
  docker run -d --name sonarqube -p 9000:9000 sonarqube:community >/dev/null || {
    echo "[X] No se pudo crear el contenedor."; exit 1; }
fi

echo "Esperando a que responda http://localhost:9000 (puede tardar 1-2 min)..."
listo=0
for i in $(seq 1 60); do
  sleep 5
  if curl -s http://localhost:9000/api/system/status 2>/dev/null | grep -q '"status":"UP"'; then
    listo=1; break
  fi
  echo "  ... intento $i/60"
done

if [ "$listo" = "1" ]; then
  echo ""
  echo "[OK] SonarQube ARRIBA: http://localhost:9000"
  echo "     Usuario: admin   Contrasena: admin  (te pedira cambiarla)"
  echo "     Genera un token y continua con  ./sonarqube/03_analizar.sh"
else
  echo "[!] No respondio. Revisa:  docker logs sonarqube  (suele ser falta de RAM)."
fi
