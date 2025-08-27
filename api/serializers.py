from rest_framework import serializers
from . models import Printer, PrinterStatusBW, PrinterStatusColor
from .pagination import PrinterStatusPagination

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = "__all__"
        # fields = ['id', 'ip', 'location', 'model', 'serial']

class PrinterStatusBWSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterStatusBW
        fields = "__all__"

class PrinterStatusColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterStatusColor
        fields = "__all__"

# class PrinterWithStatusSerializer(serializers.ModelSerializer):
#     statuses = serializers.SerializerMethodField()

#     class Meta:
#         model = Printer
#         fields = ['id', 'ip', 'location', 'model', 'serial', 'statuses']

#     def get_statuses(self, obj):
#         request = self.context.get('request')
#         # print(f'Request: {request}')
#         queryset = obj.statuses.all().order_by('-created_at')
#         paginator = PrinterStatusPagination()
#         page = paginator.paginate_queryset(queryset, request)
#         serializer = PrinterStatusSerializer(page, many=True)
#         return {
#             'count': queryset.count(),
#             'next': paginator.get_next_link(),
#             'previous': paginator.get_previous_link(),
#             'results': serializer.data
#         }












# # class PrinterStatusInlineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PrinterStatus
#         exclude = ['printer']  # já estará implícito

# class PrinterDetailSerializer(serializers.ModelSerializer):
#     # statuses = PrinterStatusInlineSerializer(many=True, read_only=True)

#     # class Meta:
#     #     model = Printer
#     #     fields = ['id', 'serial', 'location', 'model', 'statuses']

#     statuses = serializers.SerializerMethodField()

#     class Meta:
#         model = Printer
#         fields = ['id', 'serial', 'location', 'model', 'statuses']
#         # fields = ['id', 'serial', 'location']
#         # fields = ['id', 'serial', 'location', 'model', 'statuses']

#     def get_statuses(self, obj):
#         print(f'Obj: ', obj)


#         return list(obj.statuses.values(
#             'page_printer', 
#             # 'id', 'status', 'page_printer', 'toner_printer', 'unit_printer', 'created_at'

#         ))

#         # return []



