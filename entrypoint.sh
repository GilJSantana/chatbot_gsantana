#!/bin/sh

# Sair imediatamente se um comando falhar
set -e

# Esperar o banco de dados estar pronto
echo "Aguardando o banco de dados..."
sleep 5

# 1. Cria as tabelas do banco de dados
echo "Inicializando o banco de dados (criando tabelas)..."
python manage.py init-db

# 2. Tenta criar o usuário administrador inicial.
echo "Tentando criar o usuário administrador inicial..."
# CORREÇÃO: Usa o novo comando 'create-user' com a flag '--admin'.
# As variáveis de ambiente são usadas para os argumentos.
# Usamos '|| true' para que o script não pare se o usuário já existir.
python manage.py create-user $TEST_ADMIN_USERNAME $TEST_ADMIN_EMAIL --admin || true

# 3. Executa o comando principal do contêiner (passado pelo docker-compose)
echo "Iniciando a aplicação..."
exec "$@"
