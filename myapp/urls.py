from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('pdf/', views.generate_pdf, name="generate_pdf"),
    path('xls/', views.generate_xls, name="generate_xls"),
]