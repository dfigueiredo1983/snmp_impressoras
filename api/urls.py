from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'printers', views.PrinterViewSet, basename='printers')
# router.register(r'printersChart', views.PrinterChartViewSet, basename='printersChart')

urlpatterns = [
    path('', views.impressoras_view, name='counter_view'),
    path('chart', views.PrinterChartView.as_view(), name='chart_view'),
    path('', include(router.urls)),
]
