from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'printers', views.PrinterViewSet)
router.register(r'printer-statuses', views.PrinterStatusViewSet)
router.register(r'printers-detail', views.PrinterDetailViewSet, basename='printer-detail')


urlpatterns = [
    path('', views.impressoras_view, name='counter_view'),
    path('', include(router.urls))
]
