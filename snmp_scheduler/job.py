import os
import django
import logging
from datetime import datetime

# Configura o Django se estiver fora do manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printer.settings")
django.setup()

from api.models import Printer, PrinterStatus
from api.snmp_module import snmp_printer

# Configurar o Logger
log_path = os.path.join(os.path.dirname(__file__), "snmp_collect.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
)

def collect_printer_data():
    printer_list = [
        '10.44.0.100',
        '10.44.0.102',
        '10.44.0.109',
        '10.44.0.116',
        '10.44.0.119',
        '10.44.0.123',
    ]

    for hostname in printer_list:
        print(hostname)
        try:
            info = snmp_printer(hostname)  # ← deve retornar dict como esperado
            print(f'Info: {info}')

            printer, _ = Printer.objects.get_or_create(ip=hostname)

            PrinterStatus.objects.create(
                printer=printer,
                status=info['status'],
                page_printer=info['page-printer'],
                toner_printer=info['toner-printer'],
                unit_printer=info['unit-printer']
            )

            logging.info(f"[{hostname}] Dados coletados com sucesso")

        except Exception as e:
            logging.error(f"[{hostname}] Erro na coleta SNMP: {e}")