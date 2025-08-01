from django.shortcuts import render
from utils.lexmark import snmp_context

from rest_framework import viewsets
from .models import Printer, PrinterStatus
from .serializers import PrinterSerializer, PrinterStatusSerializer, PrinterDetailSerializer

# Create your views here.
def impressoras_view(request):
    raw_context = snmp_context()
    printer_list = []

    for ip, info in raw_context.items():
        item = {
            'ip': ip,
            'status': info['status'],
            'page_printer': info['page-printer'],
            'toner_printer': info['toner-printer'],
            'unit_printer': info['unit-printer'],
        }
        printer_list.append(item)

    return render(request, 'api/list.html', {'printers': printer_list})

class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

class PrinterStatusViewSet(viewsets.ModelViewSet):
    queryset = PrinterStatus.objects.all().order_by('-created_at')
    serializer_class = PrinterStatusSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

class PrinterDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterDetailSerializer
