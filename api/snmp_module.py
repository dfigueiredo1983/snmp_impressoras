from easysnmp import Session, EasySNMPTimeoutError, EasySNMPError

def snmp_printer_bw(hostname: str):
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

def snmp_printer_color(hostname: str):
    try:
        # Crie a sessão SNMP (comunidade "public" é padrão para leitura)
        session = Session(hostname, community='public', version=2)

        # OIDs base da Printer MIB
        DESCRIPTION_OID = "1.3.6.1.2.1.43.11.1.1.6.1"
        UNIT_OID        = "1.3.6.1.2.1.43.11.1.1.7.1"
        MAXCAPACITY_OID = "1.3.6.1.2.1.43.11.1.1.8.1"
        LEVEL_OID       = "1.3.6.1.2.1.43.11.1.1.9.1"
        PAGE_PRINTER    = "1.3.6.1.2.1.43.10.2.1.4.1.1"

        # Consulta todas as tabelas
        descriptions = session.walk(DESCRIPTION_OID)
        units        = session.walk(UNIT_OID)
        maxcaps      = session.walk(MAXCAPACITY_OID)
        levels       = session.walk(LEVEL_OID)
        page_printer = session.get(PAGE_PRINTER).value

        # Monta dicionários indexados pelo sufixo
        def make_dict(snmp_list):
            return {int(i): x.value for i, x in enumerate(snmp_list)}

        desc_map = make_dict(descriptions)
        unit_map = make_dict(units)
        max_map  = make_dict(maxcaps)
        level_map= make_dict(levels)

        # print("=== Suprimentos da Sharp MX3100N ===")
        for idx, name in desc_map.items():
            level = int(level_map.get(idx, -1))
            unit  = int(unit_map.get(idx, -1))
            maxc  = int(max_map.get(idx, -1))

            if level == -2:
                status = "Desconhecido"
            elif unit == 19:  # percent
                status = f"{level}%"
            elif maxc > 0 and level >= 0:
                # calcula % se não estiver em porcentagem
                status = f"{(level/maxc)*100:.1f}%"
            else:
                status = str(level)

            # print(f"[{idx:2}] {name:<30} -> {status}")

        return {
            # 'ip-printer': hostname,
            'status': 'online',
            'page_printer': page_printer,
            'toner_printer_cyan': level_map[0],
            'toner_printer_magenta': level_map[1],
            'toner_printer_yellow': level_map[2],
            'toner_printer_black': level_map[3],

            'unit_printer_cyan': level_map[5],
            'unit_printer_magenta': level_map[6],
            'unit_printer_yellow': level_map[7],
            'unit_printer_black': level_map[8],
        }

    except (EasySNMPTimeoutError, EasySNMPError, Exception) as e:
        return {
            'status': f'erro: {str(e)}',
            # 'page-printer': int(pages.value),
            'toner_printer_cyan': None,
            'toner_printer_magenta': None,
            'toner_printer_yellow': None,
            'toner_printer_black': None,

            'unit_printer_cyan': None,
            'unit_printer_magenta': None,
            'unit_printer_yellow': None,
            'unit_printer_black': None,
        }
