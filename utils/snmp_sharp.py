from easysnmp import Session

PRINTER_IP = '10.44.0.114'
COMMUNITY = 'public'
VERSION = 2

# Sessão SNMP - para conexão com a impressora
session = Session(hostname=PRINTER_IP, community=COMMUNITY, version=VERSION)

# OIDs
DESCRIPTION_OID = "1.3.6.1.2.1.43.11.1.1.6.1"
UNIT_OID        = "1.3.6.1.2.1.43.11.1.1.7.1"
MAXCAPACITY_OID = "1.3.6.1.2.1.43.11.1.1.8.1"
LEVEL_OID       = "1.3.6.1.2.1.43.11.1.1.9.1"

# Consulta todas as tabelas
descriptions = session.walk(DESCRIPTION_OID)
units        = session.walk(UNIT_OID)
maxcaps      = session.walk(MAXCAPACITY_OID)
levels       = session.walk(LEVEL_OID)

# Monta dicionários indexados pelo sufixo
def make_dict(snmp_list):
    return {int(i): x.value for i, x in enumerate(snmp_list)}

desc_map = make_dict(descriptions)
unit_map = make_dict(units)
max_map  = make_dict(maxcaps)
level_map= make_dict(levels)

print(f'desc_map: {desc_map}')
print(f'unit_map: {unit_map}')
print(f'max_map: {max_map}')
print(f'levevl_map: {level_map}')


print("=== Suprimentos da Sharp MX3100N ===")
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

    print(f"[{idx:2}] {name:<30} -> {status}")




