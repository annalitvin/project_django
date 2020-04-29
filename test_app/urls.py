from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_profile', views.get_profile, name='get_profile'),
    path('get_libs', views.get_lib, name='get_libs'),
    path('get_avg_wh', views.get_avg_wh, name='get_avg_wh'),
    path('get_astronauts', views.get_astronauts, name='get_astronauts'),
    path('get_password', views.get_password, name='get_password'),
    path('get_customers', views.get_customers, name='get_customers'),
    path('get_customers_number', views.get_customers_number, name='get_customers_number'),
    path('get_company_rev', views.get_company_rev, name='get_company_rev'),
    path('get_invoices', views.get_invoices, name='get_invoices'),
]
