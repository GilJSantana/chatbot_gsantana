#!/bin/sh

# Sair imediatamente se um comando falhar
set -e

# Executa o comando principal do contêiner (passado pelo docker-compose)
echo "Iniciando a aplicação..."
exec "$@"
