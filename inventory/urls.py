# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sklad/', views.sklad, name='sklad'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('supply/', views.supply, name='supply'),
    
    # Поставщики
    path('add-supplier/', views.add_supplier, name='add_supplier'),
    path('edit-supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('delete-supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    
    # Товары
    path('add-product/', views.add_product, name='add_product'),
    path('decrease-product/<int:product_id>/', views.decrease_product, name='decrease_product'),
]