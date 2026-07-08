#!/usr/bin/env bash
# Practica 2 - Ejecutar el analisis del proyecto con el SonarScanner (Linux)
# Uso:
#   export SONAR_TOKEN="sqp_tu_token"
#   ./sonarqube/03_analizar.sh

if [ -z "${SONAR_TOKEN}" ]; then
  echo "[X] Falta el token. Genera uno en el tablero (My Account > Security) y:"
  echo '    export SONAR_TOKEN="sqp_tu_token"'
  exit 1
fi

# Correr desde la raiz del proyecto (carpeta padre de este script)
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ" || exit 1
echo "== Analizando $RAIZ =="

docker run --rm --network host -v "$RAIZ:/usr/src" \
  -e SONAR_HOST_URL=http://localhost:9000 \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  sonarsource/sonar-scanner-cli

if [ $? -eq 0 ]; then
  echo ""
  echo "[OK] Analisis enviado. Abre el tablero:"
  echo "     http://localhost:9000/dashboard?id=caldiy-pruebas"
else
  echo "[X] El scanner fallo. Revisa el token y que el servidor este arriba."
fi
