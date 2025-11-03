import os
import sqlite3
import subprocess
import zipfile

from django.conf import settings
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Faz backup do banco (SQLite/Postgres/MySQL), compacta e remove backups antigos"

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-days',
            type=int,
            default=7,
            help="Número de dias para manter o backup (default: 7)"
        )

    def handle(self, *args, **options):
        db_conf = settings.DATABASES['default']
        engine = db_conf['ENGINE']
        backup_dir = os.path.join(settings.BASE_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # raw_backup_file = os.path.join(backup_dir, f"db_{timestamp}.sql")
        raw_backup_file = None
        # zip_backup_file = f"{raw_backup_file}.zip"
        zip_backup_file = None

        self.stdout.write(f"Iniciando o backup do banco ({engine})...")

        # ---SQLITE ---
        if 'sqlite' in engine:
            db_path = db_conf['NAME']
            raw_backup_file = os.path.join(backup_dir, f"db_{timestamp}.sqlite3")
            zip_backup_file = f"{raw_backup_file}.zip"

            con = sqlite3.connect(db_path)
            bck = sqlite3.connect(raw_backup_file)
            with bck:
                con.backup(bck)

            bck.close()
            con.close()

        # --- POSTGRES ---
        elif 'postgresql' in engine:
            user = db_conf.get('USER', '')
            password = db_conf.get('PASSWORD', '')
            host = db_conf.get('HOST', 'localhost')
            port = str(db_conf.get('PORT', 5432))
            name = db_conf['NAME']

            raw_backup_file = os.path.join(backup_dir, f"db_{timestamp}.sql")
            zip_backup_file = f"{raw_backup_file}.zip"

            env = os.environ.copy()
            if password:
                env['PGPASSWORD'] = password

            cmd = [
                "pg_dump",
                "-h", host,
                "-p", port,
                "-U", user,
                "-F", "p", # formato plain SQL
                name,
            ]

            with open(raw_backup_file, "w") as f:
                subprocess.run(cmd, stdout=f, env=env, check=True)

        # --- MYSQL/MARIADB ---
        elif 'mysql' in engine:
            user = db_conf.get('USER', '')
            password = db_conf.get('PASSWORD', '')
            host = db_conf.get('HOST', 'localhost')
            port = str(db_conf.get('PORT', 5432))
            name = db_conf['NAME']

            raw_backup_file = os.path.join(backup_dir, f"db_{timestamp}.sql")
            zip_backup_file = f"{raw_backup_file}.zip"

            cmd = [
                "mysqldump",
                "-h", host,
                "-P", port,
                "-u", user,
                f"--password={password}",
                name,
            ]

            with open(raw_backup_file, "w") as f:
                subprocess.run(cmd, stdout=f, check=True)

        else:
            self.stdout.write(self.style.ERROR(f"Engine não suportada: {engine}"))
            return
        
        # Compactar em ZIP
        with zipfile.ZipFile(zip_backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(raw_backup_file, os.path.basename(raw_backup_file))

        # Remover o arquivo original não compactadao
        os.remove(raw_backup_file)
        self.stdout.write(self.style.SUCCESS(f"Backup criado: {zip_backup_file}"))

        # Remover backups antigos
        keep_days = options['keep_days']
        cutoff = datetime.now() - timedelta(days=keep_days)

        for filename in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff:
                    os.remove(file_path)
                    self.stdout.write(f"Removido backup antigo: {file_path}")

        self.stdout.write(self.style.SUCCESS("Rotina de backup finalizada com sucesso."))



