from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sklad/', views.sklad, name='sklad'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('supply/', views.supply, name='supply'),
]
