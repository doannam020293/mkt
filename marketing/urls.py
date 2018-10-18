from django.urls import path

from . import views

urlpatterns = [
    path('down', views.get_mkt_file, name='get_mkt_file'),
    path('test', views.test, name='test'),
]