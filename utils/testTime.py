import os
import sys
import time
import django

from django.test.client import RequestFactory
from rest_framework.request import Request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura o Django se estiver fora do manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printer.settings")
django.setup()

from rest_framework.renderers import JSONRenderer
from api.models import PrinterStatus, Printer
from api.serializers import PrinterStatusSerializer, PrinterWithStatusSerializer

print('Printer Status')
start = time.time()
data = PrinterStatusSerializer(PrinterStatus.objects.all()[:50000], many=True).data
print('Serialização: ', time.time() - start)

start = time.time()
JSONRenderer().render(data)
print('JSON dump: ', time.time() - start)


print('Printer Detail')

# Criando um objeto de requisição HTTP para teste
factory = RequestFactory()

# Simula uma requisição GET para a URL desejada 
http_request = factory.get('/api/printers-with-history/1/')

# Criando um objeto de Request do DRF a partir da requisição HTTP
# Request: <rest_framework.request.Request: GET '/api/printers-with-history/1/'>
request = Request(http_request)
print(f'Request: {request}')


start = time.time()
data = PrinterWithStatusSerializer(
    Printer.objects.all()[:50000],
    many=True,
    context = {
        'request': request # contexto para a requisição
    }
).data
print('Serialização: ', time.time() - start)

start = time.time()
JSONRenderer().render(data)
print('JSON dump: ', time.time() - start)




