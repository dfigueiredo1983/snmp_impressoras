from easysnmp import Session, EasySNMPTimeoutError, EasySNMPError

def snmp_printer(hostname: str):
    try:
        # Crie a sessão SNMP (comunidade "public" é padrão para leitura)
        session = Session(hostname, community='public', version=2)

        # Obtenha número de páginas impressas (exemplo de OID genérico)
        pages_oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'  # total de páginas impressas
        toner_oid = '1.3.6.1.2.1.43.11.1.1.9.1.1'  # nível de toner (preto)
        image_oid = '1.3.6.1.2.1.43.11.1.1.9.1.2'  # (Exemplo, varia por modelo)

        location_oid = '1.3.6.1.2.1.1.6.0'
        model_oid = '1.3.6.1.2.1.25.3.2.1.3.1'

        # Consulte as OIDs
        pages = session.get(pages_oid)
        toner = session.get(toner_oid)
        image = session.get(image_oid)
        location = session.get(location_oid)
        model = session.get(model_oid)

        print(f'Model: {model}')

        return {
            'printer': 'printer',
            'status': 'online',
            'page_printer': int(pages.value),
            'toner_printer': int(toner.value)/250,
            'unit_printer': int(image.value)/1000,
            'location': location.value,
            'model': " ".join(model.value.split()[:2]),
            'serial': model.value.split()[2],
        }

    except (EasySNMPTimeoutError, EasySNMPError, Exception) as e:
        return {
            'printer': 'printer',
            'status': f'erro: {str(e)}',
            'page_printer': None,
            'toner_printer': None,
            'unit_printer': None,
            'location': None,
            'model': None,
            'serial': None,
        }
    
if __name__ == '__main__':
    ip_printer = ['10.44.0.90',
                  '10.44.0.100',
                  '10.44.0.102',
                  '10.44.0.109',
                  '10.44.0.116',
                  '10.44.0.119',
                  '10.44.0.123',                  
                  ]
    for x in ip_printer:
        # print(x)
        response = snmp_printer(x)
        print(f'Resposta: {response}')
