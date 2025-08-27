from django.shortcuts import render
from utils.lexmark import snmp_context

from django.db.models import Avg, IntegerField
from django.db.models.functions import TruncHour, Round, Cast

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Printer, PrinterStatusBW, PrinterStatusColor
from .serializers import PrinterSerializer, PrinterStatusBW, PrinterStatusColor
from .pagination import PrinterStatusPagination

# Create your views here.
def impressoras_view(request):
    raw_context = snmp_context()
    printer_list = []

    for ip, info in raw_context.items():
        if ip == '10.44.0.114':
            # print(f'IP: {ip}')
            # print(f'info: {info}')
            item = {
                'ip': ip,
                'status': info['status'],
                'page_printer': info['page_printer'],
                'toner_printer_cyan': info['toner_printer_cyan'],
                'toner_printer_magenta': info['toner_printer_magenta'],
                'toner_printer_yellow': info['toner_printer_yellow'],
                'toner_printer_black': info['toner_printer_black'],
           
                'unit_printer_cyan': info['unit_printer_cyan'],
                'unit_printer_magenta': info['unit_printer_magenta'],
                'unit_printer_yellow': info['unit_printer_yellow'],
                'unit_printer_black': info['unit_printer_black'],
            }
        else:
            # print(f'IP: {ip}')
            item = {
                'ip': ip,
                'status': info['status'],
                'page_printer': info['page_printer'],
                'toner_printer': info['toner_printer'],
                'unit_printer': info['unit_printer'],
            }
        printer_list.append(item)

    return render(request, 'api/list.html', {'printers': printer_list})

class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

class PrinterChartView(APIView):

    def get(self, request):
        data = []

        # print('PrinterChartView')

        for printer in Printer.objects.all():
            printer_list = str(printer).split('-')
            # print(f'printer_list: {printer_list}')

            if printer_list[0].strip() == '10.44.0.114':
                # print(f'Colorida PrinterChartView')
                qs = (
                    printer.color_statuses
                    .annotate(hour=TruncHour('created_at'))
                    .values('hour')
                    .annotate(
                        avg_toner_cyan=Cast(Round(Avg('toner_printer_cyan')), IntegerField()),
                        avg_toner_magenta=Cast(Round(Avg('toner_printer_magenta')), IntegerField()),
                        avg_toner_yellow=Cast(Round(Avg('toner_printer_yellow')), IntegerField()),
                        avg_toner_black=Cast(Round(Avg('toner_printer_black')), IntegerField()),

                        avg_unit_cyan=Cast(Round(Avg('unit_printer_cyan')), IntegerField()),
                        avg_unit_magenta=Cast(Round(Avg('unit_printer_magenta')), IntegerField()),
                        avg_unit_yellow=Cast(Round(Avg('unit_printer_yellow')), IntegerField()),
                        avg_unit_black=Cast(Round(Avg('unit_printer_black')), IntegerField()),
                        total_pages=Cast(Round(Avg('page_printer')), IntegerField())
                    )
                    .order_by('hour')
                )

                # print(f'QS - color: {qs}')

                data.append({
                    "printer": {
                        "ip": printer_list[0].strip(),
                        "location": printer_list[1].strip() if len(printer_list) > 1 else None,
                        "model": printer_list[2].strip() if len(printer_list) > 1 else None,
                        "serial": printer_list[3].strip() if len(printer_list) > 1 else None,
                    },
                    "statuses": list(qs)
                })
            else:
                qs = (
                    printer.bw_statuses
                    .annotate(hour=TruncHour('created_at'))
                    .values('hour')
                    .annotate(
                        avg_toner_black=Cast(Round(Avg('toner_printer')), IntegerField()),
                        avg_unit_black=Cast(Round(Avg('unit_printer')), IntegerField()),
                        total_pages=Cast(Round(Avg('page_printer')), IntegerField())
                    )
                    .order_by('hour')
                )

                data.append({
                    "printer": {
                        "ip": printer_list[0].strip(),
                        "location": printer_list[1].strip() if len(printer_list) > 1 else None,
                        "model": printer_list[2].strip() if len(printer_list) > 1 else None,
                        "serial": printer_list[3].strip() if len(printer_list) > 1 else None,
                    },
                    "statuses": list(qs)
                })
        return Response(data)



# class PrinterChartViewSet(viewsets.ModelViewSet):
#     queryset = Printer.objects.all()
#     serializer_class = PrinterSerializer

#     print(f'PrinterChartViewSet')

#     # @action(detail=False, methods=['get'])
#     # def statuses_chart(self, request, pk=None):
#     #     """Retorna os dados agragados de TODAS as impressoras"""

#     #     data = []

#     #     for printer in self.get_queryset():
#     #         printer_list = str(printer).split('-')

#     #         # print(f'Printer view: {printer_list}')

#     #         if printer_list[0] == '10.44.0.114':
#     #             print(f'Colorida CharViewSet')
#     #             qs = (
#     #                 printer.color_statuses
#     #                 .annotate(hour=TruncHour('created_at'))
#     #                 .values('hour')
#     #                 .annotate(
#     #                     avg_toner_cyan=Cast(Round(Avg('toner_printer_cyan')), IntegerField()),
#     #                     # avg_toner=Cast(Round(Avg('toner_printer')), IntegerField()),
#     #                     # avg_toner=Cast(Round(Avg('toner_printer')), IntegerField()),
#     #                     # avg_toner=Cast(Round(Avg('toner_printer')), IntegerField()),

#     #                     # avg_unit=Cast(Round(Avg('unit_printer')), IntegerField()),
#     #                     # avg_unit=Cast(Round(Avg('unit_printer')), IntegerField()),
#     #                     # avg_unit=Cast(Round(Avg('unit_printer')), IntegerField()),
#     #                     # avg_unit=Cast(Round(Avg('unit_printer')), IntegerField()),
#     #                     total_pages=Cast(Round(Avg('page_printer')), IntegerField())
#     #                 )
#     #                 .order_by('hour')
#     #             )

#     #             print(f'QS - color: {qs}')

#     #             data.append({
#     #                 "printer": {
#     #                     "ip": printer_list[0].strip(),
#     #                     "location": printer_list[1].strip() if len(printer_list) > 1 else None,
#     #                     "model": printer_list[2].strip() if len(printer_list) > 1 else None,
#     #                     "serial": printer_list[3].strip() if len(printer_list) > 1 else None,
#     #                 },
#     #                 "statuses": list(qs)
#     #             })
#     #         else:
#     #             qs = (
#     #                 printer.bw_statuses
#     #                 .annotate(hour=TruncHour('created_at'))
#     #                 .values('hour')
#     #                 .annotate(
#     #                     avg_toner=Cast(Round(Avg('toner_printer')), IntegerField()),
#     #                     avg_unit=Cast(Round(Avg('unit_printer')), IntegerField()),
#     #                     total_pages=Cast(Round(Avg('page_printer')), IntegerField())
#     #                 )
#     #                 .order_by('hour')
#     #             )

#     #             data.append({
#     #                 "printer": {
#     #                     "ip": printer_list[0].strip(),
#     #                     "location": printer_list[1].strip() if len(printer_list) > 1 else None,
#     #                     "model": printer_list[2].strip() if len(printer_list) > 1 else None,
#     #                     "serial": printer_list[3].strip() if len(printer_list) > 1 else None,
#     #                 },
#     #                 "statuses": list(qs)
#     #             })
#     #     return Response(data)


# # class PrinterStatusViewSet(viewsets.ReadOnlyModelViewSet):
# #     serializer_class = PrinterStatusSerializer
# #     pagination_class = PrinterStatusPagination

# #     def get_queryset(self):
# #         printer_id = self.request.query_params.get('printer')
# #         if printer_id:
# #             return PrinterStatus.objects.filter(printer_id=printer_id).order_by('-created_at')
# #         return PrinterStatus.objects.all().order_by('-created_at')
    

# # class PrinterDetailWithHistoryViewSet(viewsets.ReadOnlyModelViewSet):
# #     queryset = Printer.objects.prefetch_related('statuses')
# #     serializer_class = PrinterWithStatusSerializer
