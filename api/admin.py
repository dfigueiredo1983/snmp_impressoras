from django.contrib import admin

from .models import Printer, PrinterStatus

# Register models in admin site
admin.site.register(Printer)
admin.site.register(PrinterStatus)

