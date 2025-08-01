from .models import Printer, PrinterStatus
from easysnmp import Session, EasySNMPTimeoutError, EasySNMPError

def snmp_printer(hostname: str):
    try:
        # Crie a sessão SNMP (comunidade "public" é padrão para leitura)
        session = Session(hostname, community='public', version=2)

        # Obtenha número de páginas impressas (exemplo de OID genérico)
        pages_oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'  # total de páginas impressas
        toner_oid = '1.3.6.1.2.1.43.11.1.1.9.1.1'  # nível de toner (preto)
        image_oid = '1.3.6.1.2.1.43.11.1.1.9.1.2'  # (Exemplo, varia por modelo)

        # Consulte as OIDs
        pages = session.get(pages_oid)
        toner = session.get(toner_oid)
        image = session.get(image_oid)

        return {
            'printer': 'printer',
            'status': 'online',
            'page-printer': int(pages.value),
            'toner-printer': int(toner.value)/250,
            'unit-printer': int(image.value)/1000,
        }

    except (EasySNMPTimeoutError, EasySNMPError, Exception) as e:
        return {
            'printer': 'printer',
            'status': f'erro: {str(e)}',
            'page-printer': None,
            'toner-printer': None,
            'unit-printer': None,
        }
    


# def snmp_printer():
#     context = {}

#     printer_list = [
#         '10.44.0.100',
#         '10.44.0.102',
#         '10.44.0.109',
#         '10.44.0.116',
#         '10.44.0.119',
#         '10.44.0.123'
#     ]
    
#     for ip in printer_list:
#         info = snmp_printer(ip)  # resultado: dict com status, page-printer, etc.
#         context[ip] = info

#         # Cria (ou recupera) a impressora
#         printer, _ = Printer.objects.get_or_create(ip=ip)

#         # Salva o status atual no histórico
#         PrinterStatus.objects.create(
#             printer=printer,
#             status=info['status'],
#             page_printer=info['page-printer'],
#             toner_printer=info['toner-printer'],
#             unit_printer=info['unit-printer']
#         )
    
#     return context



