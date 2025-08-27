#! /bin/bash
# shedbang - #! caminho_bash

PROJECT_DIR="/home/daniel/disis/snmp-impressoras"

VENV_DIR="$PROJECT_DIR/venv"
FRONTEND_DIR="$PROJECT_DIR/frontend"
SCHEDULER_DIR="$PROJECT_DIR/snmp_scheduler"

cd "$PROJECT_DIR" || exit

echo "Iniciando a aplicação"

echo "Ativando o ambiente virtual"
source "$VENV_DIR/bin/activate"

# Função para matar os processos filhos ao sair
cleanup() {
    echo "⏹ Encerrando todos os serviços..."
    kill $BACKEND_PID $SCHEDULER_PID $FRONTEND_PID 2>/dev/null
    wait
    echo "✅ Todos os serviços foram finalizados!"
    exit 0
}
trap cleanup INT TERM  # Captura Ctrl+C (SIGINT) e kill normal (SIGTERM)

echo "Iniciando o ambiente virtual - backend"
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8585 > backend.log 2>&1 &  # 👈 roda em background
BACKEND_PID=$!


cd "$SCHEDULER_DIR" || exit
echo "Iniciando o scheduler"
python run_scheduler.py > scheduler.log 2>&1 & # 👈 roda em background
SCHEDULER_PID=$!

cd "$FRONTEND_DIR" || exit
echo "Iniciando o frontend"
npm run dev > frontend.log 2>&1 &  # 👈 roda em background
FRONTEND_PID=$!

echo "✅ Todos os serviços foram iniciados!"
wait  # mantém o script ativo até que os processos terminem



