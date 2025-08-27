import os
import django
import logging
from datetime import datetime

# Configura o Django se estiver fora do manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printer.settings")
django.setup()

from api.models import Printer, PrinterStatusBW, PrinterStatusColor
from api.snmp_module import snmp_printer_bw, snmp_printer_color

# Configurar o Logger
log_path = os.path.join(os.path.dirname(__file__), "snmp_collect.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
)

def collect_printer_data():
    printer_list = [
        '10.44.0.90',
        '10.44.0.100',
        '10.44.0.102',
        '10.44.0.109',
        '10.44.0.114', # color
        '10.44.0.116',
        '10.44.0.119',
        '10.44.0.123',
    ]

    for hostname in printer_list:
        # print(hostname)
        try:
            if hostname != '10.44.0.114':
                info = snmp_printer_bw(hostname)  # ← deve retornar dict como esperado

                printer_obj, printer_created = Printer.objects.get_or_create(ip=hostname)
                print(f'{hostname} - Info: {info} - {printer_created}')


                if info:
                    if 'model' in info and info['model']:
                        printer_obj.model = info['model']
                    if 'location' in info and info['location']:
                        printer_obj.location = info['location']
                    if 'serial' in info and info['serial']:
                        printer_obj.serial = info['serial']

                printer_obj.save()


                PrinterStatusBW.objects.create(
                    printer=printer_obj,
                    status=info['status'],
                    page_printer=info['page_printer'],
                    toner_printer=info['toner_printer'],
                    unit_printer=info['unit_printer']
                )
                logging.info(f"[{hostname}] Dados coletados com sucesso")

            else:
                info = snmp_printer_color(hostname)  # ← deve retornar dict como esperado

                printer_obj, printer_created = Printer.objects.get_or_create(ip=hostname, tipo="COLOR")
                print(f'{hostname} - Info: {info} - {printer_created}')

                PrinterStatusColor.objects.create(
                    printer=printer_obj,
                    status=info['status'],
                    page_printer=info['page_printer'],

                    toner_printer_cyan=info['toner_printer_cyan'],
                    toner_printer_magenta=info['toner_printer_magenta'],
                    toner_printer_yellow=info['toner_printer_yellow'],
                    toner_printer_black=info['toner_printer_black'],

                    unit_printer_cyan=info['unit_printer_cyan'],
                    unit_printer_magenta=info['unit_printer_magenta'],
                    unit_printer_yellow=info['unit_printer_yellow'],
                    unit_printer_black=info['unit_printer_black'],
                )
                logging.info(f"[{hostname}] Dados coletados com sucesso")


        except Exception as e:
            logging.error(f"[{hostname}] Erro na coleta SNMP: {e}")
