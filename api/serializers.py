from rest_framework import serializers
from . models import Printer, PrinterStatus

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ['id', 'ip', 'location', 'model']

class PrinterStatusSerializer(serializers.ModelSerializer):
    printer = serializers.PrimaryKeyRelatedField(queryset=Printer.objects.all())

    class Meta:
        model = PrinterStatus
        fields = [
            'id', 'printer', 'status', 'page_printer',
            'toner_printer', 'unit_printer', 'created_at'
        ]
        read_only_fields = ['created_at']

class PrinterStatusInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterStatus
        exclude = ['printer']  # já estará implícito

class PrinterDetailSerializer(serializers.ModelSerializer):
    statuses = PrinterStatusInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Printer
        fields = ['id', 'ip', 'location', 'model', 'statuses']
