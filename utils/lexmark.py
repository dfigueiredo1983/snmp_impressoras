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
            # 'ip-printer': hostname,
            'status': 'online',
            'page-printer': int(pages.value),
            'toner-printer': int(toner.value)/250,
            'unit-printer': int(image.value)/1000,
        }

    except (EasySNMPTimeoutError, EasySNMPError, Exception) as e:
        return {
            'status': f'erro: {str(e)}',
            'page-printer': None,
            'toner-printer': None,
            'unit-printer': None,
        }
    


def snmp_context():
    context = {}

    printer_list = [
                    '10.44.0.100',
                    '10.44.0.102',
                    '10.44.0.109',
                    '10.44.0.116',
                    '10.44.0.119',
                    '10.44.0.123']
    
    for printer in printer_list:
        # adicinando elementos ao dicionário context com chave printer
        context[printer] = snmp_printer(printer)

    return context

if __name__ == '__main__':
    printer_ip = ['10.44.0.116',
                  '10.44.0.102',
                  '10.44.0.119',
                  '10.44.0.100',
                  '10.44.0.109',
                  '10.44.0.123']
    for printer in printer_ip:
        snmp_printer(printer)
        print()
