import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from apscheduler.schedulers.blocking import BlockingScheduler
from snmp_scheduler.job import collect_printer_data

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone='America/Sao_Paulo')

    # Executar a cada 10 minutos
    scheduler.add_job(collect_printer_data, 'interval', minutes=10)
    # scheduler.add_job(collect_printer_data, 'interval', seconds=5)

    print("Scheduler iniciado. Coletando dados SNMP a cada 10 minutos.")
    scheduler.start()
