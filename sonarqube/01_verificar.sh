#!/usr/bin/env bash
# Practica 2 - Verificacion de prerrequisitos para SonarQube (Linux/Mac)
echo "== Verificacion de prerrequisitos (SonarQube) =="

if docker --version >/dev/null 2>&1; then
  echo "[OK ] $(docker --version)"
else
  echo "[X  ] Docker no encontrado."
fi

if docker info >/dev/null 2>&1; then
  echo "[OK ] Docker daemon activo"
else
  echo "[X  ] Docker no esta corriendo. Inicia el servicio de Docker."
fi

if command -v ss >/dev/null 2>&1 && ss -ltn 2>/dev/null | grep -q ':9000'; then
  echo "[!  ] Puerto 9000 EN USO."
else
  echo "[OK ] Puerto 9000 libre"
fi

if python3 --version >/dev/null 2>&1; then
  echo "[OK ] $(python3 --version)"
else
  echo "[!  ] Python3 no encontrado (no bloqueante para levantar Sonar)."
fi

echo ""
echo "Si todo esta en [OK], continua con:  ./sonarqube/02_levantar.sh"
