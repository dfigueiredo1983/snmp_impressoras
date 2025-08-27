from django.contrib import admin

from .models import Printer, PrinterStatusBW, PrinterStatusColor

# Register models in admin site
admin.site.register(Printer)
admin.site.register(PrinterStatusBW)
admin.site.register(PrinterStatusColor)

