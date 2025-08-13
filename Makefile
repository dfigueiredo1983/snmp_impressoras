COMPOSE=docker COMPOSE
FRONTEND_DIR=frontend
BACKEND_DIR=backend

help: 
	@echo	"Comandos disponíveis:"
	@echo	"run scheduler"
	@echo	"run backend"
	@echo	"run frontend"
	@echo	"run docker compose"


scheduler:
	python snmp_scheduler/run_scheduler.py

backend:
	source /venv/bin/activate
	python manage.py runserver 0.0.0.0:8585

frontend:
	cd $(FRONTEND_DIR) && npm install
	cd $(FRONTEND_DIR) && npm run dev


