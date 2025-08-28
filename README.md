# Configurar a aplicação

# Backend
sudo apt update
sudo apt install -y build-essential python3-dev libsnmp-dev snmp

# Criar o ambiente virtuaL
sudo apt install python3.XX-venv
python3 -m venv venv



# Rodar o pip
pip insat












# Ver OID das máquinas
snmpwalk -v2c -c public 192.168.0.100

# Descobrir pacotes que faltam
apt-file search net-snmp-config

