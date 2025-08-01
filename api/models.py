from django.db import models

# Create your models here.
class Printer(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.ip} - {self.status}'

class PrinterStatus(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=100)
    page_printer = models.PositiveIntegerField()
    toner_printer = models.CharField(max_length=100)
    unit_printer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.printer.ip} - {self.create_at.strftime("%Y-%m-%d %H:%M:%S")}'
