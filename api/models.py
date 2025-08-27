from django.db import models

# Create your models here.
class Printer(models.Model):
    PRINTER_TYPES = (
        ("BW", "Preto e branco"),
        ("COLOR", "Colorida")
    )

    ip = models.GenericIPAddressField()
    location = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serial = models.CharField(max_length=100, unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=PRINTER_TYPES, default="BW")

    def __str__(self):
        return f'{self.ip} - {self.location} - {self.model} - {self.serial}'

# Classe base para printerStatus
class BasePrinterStatus(models.Model):
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True # não pode ser instanciada

class PrinterStatusBW(BasePrinterStatus):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='bw_statuses')
    page_printer = models.PositiveIntegerField()
    toner_printer = models.CharField(max_length=100)
    unit_printer = models.CharField(max_length=100)

    def __str__(self):
        return f'BW - {self.printer.ip} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'

class PrinterStatusColor(BasePrinterStatus):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='color_statuses')
    page_printer = models.PositiveIntegerField()
    toner_printer_cyan = models.CharField(max_length=100)
    toner_printer_magenta = models.CharField(max_length=100)
    toner_printer_yellow = models.CharField(max_length=100)
    toner_printer_black = models.CharField(max_length=100)

    unit_printer_cyan = models.CharField(max_length=100)
    unit_printer_magenta = models.CharField(max_length=100)
    unit_printer_yellow = models.CharField(max_length=100)
    unit_printer_black = models.CharField(max_length=100)

    def __str__(self):
        return f'COLOR - {self.printer.ip} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'

